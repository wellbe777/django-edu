from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('courses/', views.CourseList.as_view(), name='course_lst'),
    path('courses/<int:pk>/', views.CourseDetail.as_view(), name='course_det'),
    path('subjects/', views.SubjectList.as_view(), name='subject_lst'),
    path('subjects/<int:pk>/', views.SubjectDetail.as_view(), name='subject_det'),
    path('categories/', views.CategoryList.as_view(), name='category_lst'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category_det'), 
    path('modules/', views.ModuleList.as_view(), name='module_lst'),
    path('modules/<int:pk>/', views.ModuleDetail.as_view(), name='module_det'),    
]
