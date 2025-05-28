from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from courses.models import Course
from .cart import Cart
from .forms import CartAddCourseForm
from coupons.forms import CouponApplyForm


@require_POST
def cart_add(request, course_id):
    cart = Cart(request)
    course = get_object_or_404(Course, id=course_id)
    form = CartAddCourseForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(course=course,
                 override_quantity=cd['override']) #quantity=cd['quantity'],
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, course_id):
    cart = Cart(request)
    course = get_object_or_404(Course, id=course_id)
    cart.remove(course)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddCourseForm(initial={'quantity': item['quantity'],
                                                                   'override': True})
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/detail.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form})
