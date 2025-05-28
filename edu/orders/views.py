from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from .models import OrderItem, Order
from courses.models import Course, Module, StudentCourses
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from .tasks import order_created
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages



@login_required
def order_create(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user 
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
               
            for item in cart:
                course = item['course']
                OrderItem.objects.create(order=order, course=item['course']) 
                course.students.add(request.user)
                #StudentCourses.objects.create(user=request.user, course=item['course']) 
                # clear the cart
                cart.clear()
                # launch asynchronous task (run Celery in different shell: celery -A edu worker -l info)
                order_created.delay(order.id)
                # set the order in the session
                request.session['order_id'] = order.id
                # redirect for payment
            return redirect(reverse('payment:process'))
            #return render(request, 'orders/order/created.html', {'order': order})   
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})   


class OrdersUnpaidByUserListView(LoginRequiredMixin, ListView):
    model = Order
    # context_object_name = 'orders_list_by_user'
    template_name = 'orders/order/unpaid_order_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, paid=False).order_by('-created')


class OrdersByUserDetailView(LoginRequiredMixin, DetailView):
    """Generic class-based view listing items for current order of current user."""
    model = Order
    template_name = 'orders/order/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ordid = self.object.pk
        context['orderitems'] = OrderItem.objects.filter(
            order__user=self.request.user, order_id=ordid)
        return context

class OrdersPaidByUserDetailView(LoginRequiredMixin, DetailView):
    """Generic class-based view listing items for current order of current user."""
    model = Order
    template_name = 'orders/order/paid_order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ordid = self.object.pk
        context['paidorderitems'] = OrderItem.objects.filter(
            order__user=self.request.user, order_id=ordid)
        return context

@login_required
def unpaid_orders(request, order_id):
    order = get_object_or_404(Order, id=order_id, paid=False)
    orderitems = OrderItem.objects.filter(order=order, order__user=request.user)    
    return render(request, 'orders/order/unpaid_order_list.html', {'orderitems': orderitems})


@login_required
def unpaid_order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    orderitems = OrderItem.objects.filter(order=order, order__user=request.user) 
    print("Order: ", order)
    print("Orderitems: ", orderitems)
    for item in orderitems:
        course = item.course
        print("Course ID: ", course.id)
        course.students.remove(request.user)   
        #Course.objects.filter(id=course.id).update(student=None)
    order.delete()
    return render(request, 'orders/order/unpaid_order_deleted.html', {'orderitems': orderitems})


@login_required
def unpaid_order_process(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    orderitems = OrderItem.objects.filter(order=order, order__user=request.user)
    if order:
        request.session['order_id'] = order.id
        return redirect(reverse('payment:process'))
    return render(request, 'orders/order/process_unpaid_order.html', {'orderitems': orderitems})


class OrdersCurrentUserView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'mycourses/ordered_courses.html'
    # paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # OrdersCurrentUserView,self
        uid = self.request.user
        context['orderitems'] = OrderItem.objects.filter(
            order__user=self.request.user, order__paid=True).order_by('order_id')
        context['unpaidorderitems'] = OrderItem.objects.filter(
            order__user=self.request.user, order__paid=False).order_by('order_id')
        return context


class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'orders/order/course/course_detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paid_courses = OrderItem.objects.filter(order__user=self.request.user.id, order__paid=True) 
        course = self.get_object()
        print('Course object ID: ', course.id)
        for m in paid_courses:
            print('Paid object ID: ', m.course_id)
            if course.id == m.course_id:       
                print('After if course object ID: ', course.id, ' Paid object ID: ', m.course_id)
                if 'module_id' in self.kwargs:
                # get current module
                    context['module'] = course.modules.get(
                                        id=self.kwargs['module_id'])
                else:
                    # get first module
                    context['module'] = course.modules.all().first()   #[0]
                    print(context)
                return context
        else:
            raise Http404('Sorry. You did not pay for this course.')


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})

    