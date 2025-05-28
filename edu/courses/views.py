from rest_framework import generics
from django.shortcuts import render
from django.http import JsonResponse
from .models import Subject, Course, Module, Content, UserProfile, Category, Review
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet
from django.forms.models import modelform_factory
from django.apps import apps
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ChangeUserFnameLname, UserProfileForm, EmailContactForm, CourseReviewForm, SearchForm
from students.forms import CourseEnrollForm
from django.http import Http404
from django.core.mail import send_mail
from cart.forms import CartAddCourseForm
from django.utils import timezone
from django.db.models import Prefetch
from orders.models import Order, OrderItem
from django.http import HttpResponse
from django.db.models import Q, Avg
from django.core.cache import cache
from .serializers import CourseSerializer, SubjectSerializer, CategorySerializer
from django.template import Context, loader


class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class SubjectList(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer 

class SubjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    
class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer   

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


#def get_queryset(self):
    # you can use self.queryset or Category.objects.filter(any filter)
#    return self.queryset.filter(some filtering)


@login_required
def user_profile(request):
    #shipping_address_qs = Address.objects.filter(
    #    user=request.user, default=True, address_type='S').order_by('-id').last()
    #billing_address_qs = Address.objects.filter(
    #    user=request.user, default=True, address_type='B').order_by('-id').last()

    #context = {
    #    'shipping_address': shipping_address_qs,
    #    'billing_address': billing_address_qs
    #}
    question = Subject.objects.all()
    question_dict = {
        'question': question
    }

    return render(request, "profile.html", question_dict)

@login_required
def name_change_form(request):
    print("Request: ", request)
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        form = ChangeUserFnameLname(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            messages.success(request, "Your name was successfully changed")
    else:
        form = ChangeUserFnameLname()
    return render(request, 'user_name_change.html', {'form': form})


@login_required
def image_upload(request):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            user_profile.image = form.cleaned_data['image']
            user_profile.save()

            img_obj = form.instance
            return render(request, 'image_upload.html', {'form': form, 'img_obj': img_obj})
    else:
        form = UserProfileForm()
    return render(request, 'image_upload.html', {'form': form})


class CategoryListView(generic.ListView):
    model = Category
    template_name = 'home.html'

    #def get_queryset(self):
    #    return Category.objects.all()

    #def get_context_data(self, **kwargs):
            #context = super().get_context_data(**kwargs)  # CategoryListView,self
            #category = Category.objects.all()
            #subject = Subject.objects.all()
            #context['subjectitems'] = Subject.objects.all()
            #context['courseitems'] = Course.objects.all()
            #context['courseitems'] = Course.objects.filter(subject__category__isnull=False)
            #context['subjectitems'] = Subject.objects.filter(category__subject__isnull=False)
            #context['subjectitems'] = Subject.objects.filter(category__pk=self.kwargs['pk'])
            #context['course_sub_cat'] = Course.objects.order_by('subject_id')
            #return context
    
    #subjects = Subject.objects.select_related('category').all()

class AboutListView(generic.ListView):
    model = Category
    template_name = 'about.html'

class TeamListView(generic.ListView):
    model = Category
    template_name = 'team.html'

class ReviewsListView(generic.ListView):
    model = Category
    template_name = 'reviews.html'

class NotFoundListView(generic.ListView):
    model = Category
    template_name = '404.html'


class CourseMenuListView(generic.ListView):
    model = Course
    template_name = 'test.html'

    def get_queryset(self):
        return Course.objects.select_related('subject__category')


def category_menu(request):      # used with Django regroup
    categoryit = Category.objects.all() 
    #subjectitems = Subject.objects.all()  #filter(category__pk=request.pk)
    #courseitems = Course.objects.all()  
    #table2 = Subject.objects.select_related('category').all()
    return render(request, 'home.html', context={'categoryit':categoryit}) #,'subjectitems':subjectitems,'courseitems':courseitems})


class CategoryDetailView(generic.DetailView):
    model = Category
    # allows to use this name in template instead of object_list
    #context_object_name = 'category_detail'
    template_name = 'category_detail.html'


class SubjectListView(generic.ListView):
    model = Subject
    template_name = 'navbar.html'


class SubjectDetailView(generic.DetailView):
    model = Subject
    # allows to use this name in template instead of object_list
    #context_object_name = 'subject_detail'
    template_name = 'subject_detail.html'
    

class SubjectListView_P(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing orders for current user."""
    model = Subject
    # context_object_name = 'orders_list_by_user'
    template_name = 'profile.html'

    def get_queryset(self):
        return Subject.objects.all()

   
def subject_list(request):
    context = {
        'subjects': Subject.objects.all()
    }
    return render(request, "index.html", context)


class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview', 'price', 'image']
    success_url = reverse_lazy('courses:manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, generic.ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'

#    def get_queryset(self):
#        qs = super().get_queryset()
#        return qs.filter(owner=self.request.user) #p.381

class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'

class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'

class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course,
                             data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('courses:manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses',
                                  model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module,
                                       id=module_id,
                                       course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # new content
                Content.objects.create(module=self.module,
                                       item=obj)
            return redirect('courses:module_content_list', self.module.id)

        return self.render_to_response({'form': form,
                                        'object': self.obj})


class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content,
                                    id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('courses:module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)

        return self.render_to_response({'module': module})


class ModuleOrderView(CsrfExemptMixin,
                      JsonRequestResponseMixin,
                      View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id,
                   course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin,
                       JsonRequestResponseMixin,
                       View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id,
                       module__course__owner=request.user) \
                       .update(order=order)
        return self.render_json_response({'saved': 'OK'})


# done with cache
class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        subjects = cache.get('all_subjects')
        if not subjects:
            subjects = Subject.objects.annotate(total_courses=Count('course'))
            cache.set('all_subjects', subjects)                                 # cache subject object and their num of courses
        all_courses = Course.objects.annotate(total_modules=Count('modules'))       # was courses var before cache 
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            key = f'subject_{subject.id}_courses'
            courses = cache.get(key)
            if not courses:
                courses = all_courses.filter(subject=subject)                       # courses.filter(subject=subject)
                cache.set(key, courses)
        else:
            courses = cache.get('all_courses')
            if not courses:
                courses = all_courses
                cache.set('all_courses', courses)
        return self.render_to_response({'subjects': subjects,
                                        'subject': subject,
                                        'courses': courses})


'''
class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        subjects = Subject.objects.annotate(total_courses=Count('course'))
        courses = Course.objects.annotate(total_modules=Count('modules'))
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response({'subjects': subjects,
                                        'subject': subject,
                                        'courses': courses})
'''

class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['enroll_form'] = CourseEnrollForm(initial={'course':self.object})
        context['cart_course_form'] = CartAddCourseForm(initial={'course':self.object})
        return context


def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    cart_course_form = CartAddCourseForm()

    return render(request, 'courses/course/detail.html',
                  {'course': course, 'cart_course_form': cart_course_form})


class CourseSearchView(generic.ListView):
    model = Course
    #paginate_by = 10
    template_name = "search_courses_results.html"

    def get_queryset(self):
        query = self.request.GET.get('search_courses')
        print('Q: ', query)
        if not query:
            messages.add_message(self.request, messages.INFO, 'No Course Found. Try Again')
        else:
            object_list = Course.objects.filter(
                Q(title__icontains=query) | Q(price__icontains=query)
            )
            if not object_list:
                messages.add_message(self.request, messages.INFO, 'No Course Found. Try Again')
            else:
                return object_list


# ajax course search suggestions start -----
def search_view(request):
    form = SearchForm()
    return render(request, 'search.html', {'form': form})
    
def suggestion_info(request, slug):
    item = get_object_or_404(Course, slug=slug)

    # Redirect authenticated users directly to the detail page
    #if request.user.is_authenticated:
    #    return redirect(item.get_absolute_url())

    return render(request, 'suggestion_info.html', {'item': item})
  
def search_suggestions(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        query = request.GET.get('query', '').strip()
        
        # Fetch matching objects and store them as a list of dictionaries
        results = Course.objects.filter(title__icontains=query).values('title', 'slug')[:10]
        
        # Construct JSON response correctly
        suggestions = [{'title': item['title'], 'url': f"/suggestion-info/{item['slug']}/"} for item in results]

        return JsonResponse({'suggestions': suggestions})
    
    return JsonResponse({'suggestions': []})
# ajax course search suggestions end -----

# email contact form       
def contact(request):
    if request.method == 'POST':
        form = EmailContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = f"{cd['subject']}"
            message = f"{cd['name']} from EDU written: {cd['message']}"
            email = f"{cd['email']}"
            send_mail(subject, message, email, ['wellsalgorithm@gmail.com'])
            messages.success(request, "Your message was successfully sent")
            form = EmailContactForm()
            #sent = True

    else:
        form = EmailContactForm()
    return render(request, 'contact.html', {'form': form}) #'sent': sent

def success(request):
    return render(request, 'message_sent.html')


class CourseRateDetaillView(generic.DetailView):
    model = Course
    template_name = 'courses/course/detail_for_review.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #course = self.get_object()
        #context['enroll_form'] = CourseEnrollForm(initial={'course':self.object})
        context['course_review_form'] = CourseReviewForm(initial={'course':self.object})  #{'course':self.object}
        return context


@login_required
def review_course(request, pk):
    if request.method == 'POST':
        form = CourseReviewForm(request.POST)
        print('PK: ', pk)
        course = Course.objects.get(id=pk)
        if form.is_valid():
            rate = form.cleaned_data['rate']
            subject = form.cleaned_data['subject']
            comment = form.cleaned_data['comment']
        try:
            rated_course = Review.objects.get(user_id=request.user, course_id=pk)
            if rated_course:
                course_review = Review(
                    id=rated_course.id,
                    user=request.user,
                    course_id=rated_course.course_id,
                    rate=rate,
                    subject=subject,
                    comment=comment,
                    updated=timezone.now())
                course_review.save(update_fields=['rate', 'subject', 'comment', 'updated'])
                messages.success(request, "You updated this course rating")
        except Review.DoesNotExist:
            course_review = Review(
                    user=request.user,
                    course=course,
                    rate=rate,
                    subject=subject,
                    comment=comment)
            course_review.save()
            messages.success(request, "You rated this course")
    else:
        messages.info(request, "Please rate this course")
        form = CourseReviewForm()
    reviewed_course = Review.objects.get(user_id=request.user, course_id=pk)
    
    return render(request, 'courses/course/rated_course.html', {'form': form, 'reviewed_course': reviewed_course})


def course_detail_review(request, pk):
    course_detail_review = Course.objects.get(id=pk)
    review = Review.objects.filter(course = course_detail_review)
    
    return render(request, 'courses/course/course_rating_detail.html', {'course_detail_review':course_detail_review, 'review':review})


def courses_count_and_best(request):      
    #sub_for_cat = Category.objects.annotate(subject_count=Count('subject'))
    #course_for_sub = Subject.objects.annotate(cor_count=Count('course'))
    course = Course.objects.all()
    review = Review.objects.filter(course__in=course)
    course_cnt = Category.objects.annotate(course_count=Count('subject__course'))
    student_cnt = Course.objects.annotate(student_count=Count('students'))
    #course_cnt_enum = enumerate(course_cnt)
    #print('Review: ', review)
    #print('Student count: ', student_cnt)

    return render(request, 'home.html', context={'course_cnt':course_cnt, 'review':review, 'student_cnt':student_cnt})


class OrdersUnpaidByUserListView(LoginRequiredMixin, generic.ListView):
    model = Order
    # context_object_name = 'orders_list_by_user'
    template_name = 'profile.html'
    #paginate_by = 10

    #def get_queryset(self):
    #    return Order.objects.filter(user=self.request.user, paid=False).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uid = self.request.user
        context['paidorders'] = Order.objects.filter(user=self.request.user, paid=True).order_by('-created')
        context['unpaidorders'] = Order.objects.filter(user=self.request.user, paid=False).order_by('-created')
        return context




