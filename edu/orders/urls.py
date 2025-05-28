from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
path('create/', views.order_create, name='order_create'),
path('mycourses/', views.OrdersCurrentUserView.as_view(), name='student_course_list'),
path('course/<int:pk>/', views.StudentCourseDetailView.as_view(), name='student_course_detail'),
path('course/<int:pk>/<module_id>/', views.StudentCourseDetailView.as_view(), name='student_course_detail_module'),
path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
path('unpaidorderlist/', views.OrdersUnpaidByUserListView.as_view(), name='unpaid_order_list'),
path('unpaidorderlist/order/<int:pk>/', views.OrdersByUserDetailView.as_view(), name='unpaid_order_detail'),
path('unpaidorder/<int:order_id>/', views.unpaid_order_process, name='unpaid_order_process'),
path('unpaidorder/<int:order_id>/deleted/', views.unpaid_order_delete, name='unpaid_order_delete'),
]
