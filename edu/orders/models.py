from django.db import models
from django.conf import settings
from courses.models import Course
from django.shortcuts import reverse
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)
    coupon = models.ForeignKey(Coupon, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'
        #f'Order {self.id}' + ' ' + self.user.first_name + ' ' + self.user.last_name + ' ' + self.user.email

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        t_cost = total_cost - total_cost * (self.discount / Decimal(100))
        return round(Decimal(t_cost), 2)
        #return sum(item.get_cost() for item in self.items.all())

    def get_absolute_url(self):
        """Returns the url to access a particular subject instance."""
        return reverse('courses:course_detail', args=[str(self.id)])


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    course = models.ForeignKey(Course,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    #quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.course.price   # self.quantity
