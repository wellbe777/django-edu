from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    #path('', views.CourseList.as_view(), name='course_lst'),
    #path('<int:pk>/', views.CourseDetail.as_view(), name='course_det'),
    #path('subjects/', views.SubjectList.as_view(), name='subject_list'),
    #path('subjects/<int:pk>/', views.SubjectDetail.as_view(), name='subject_det'),
    #path('categories/', views.CategoryList.as_view(), name='category_lst'),
    #path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category_det'),
    
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('suggestion-info/<slug:slug>/', views.suggestion_info, name='suggestion_info'),
    path('search-results/', views.CourseSearchView.as_view(), name='search_results'),
    #path('', views.category_menu, name='category-list'),
    #path('', views.CategoryListView.as_view(), name='category_list'),
    path('about/', views.AboutListView.as_view(), name='about'),
    path('team/', views.TeamListView.as_view(), name='team'),
    path('reviews/', views.ReviewsListView.as_view(), name='reviews'),
    path('404/', views.NotFoundListView.as_view(), name='404'),
    path('contact/', views.contact, name='contact'),
    path('', views.courses_count_and_best, name='courses_count'),
    path('corcount/', views.courses_count_and_best, name='courses_count'),
    
    path('category/<slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    #path('', views.SubjectListView.as_view(), name='subject_list'),
    #path('accounts/profile/', views.SubjectListView_P.as_view(), name='account-profile'),
    path('accounts/profile/', views.OrdersUnpaidByUserListView.as_view(), name='account-profile'),
    path('accounts/profile/name-change/', views.name_change_form, name='name-change'),
    path('accounts/profile/imageupload/', views.image_upload, name='image-upload'),
    path('subject/<slug>/', views.SubjectDetailView.as_view(), name='subject-detail'),
    #path('accounts/profile/', user_profile, name='account-profile')
    path('mine/', views.ManageCourseListView.as_view(), name='manage_course_list'),
    path('create/', views.CourseCreateView.as_view(), name='course_create'),
    path('<pk>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
    path('<pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    path('<pk>/module/', views.CourseModuleUpdateView.as_view(), name='course_module_update'),
    path('module/<int:module_id>/content/<model_name>/create/', views.ContentCreateUpdateView.as_view(), name='module_content_create'),
    path('module/<int:module_id>/content/<model_name>/<id>/', views.ContentCreateUpdateView.as_view(), name='module_content_update'),
    path('content/<int:id>/delete/', views.ContentDeleteView.as_view(), name='module_content_delete'),
    path('module/<int:module_id>/', views.ModuleContentListView.as_view(), name='module_content_list'),
    path('module/order/', views.ModuleOrderView.as_view(), name='module_order'),
    path('content/order/', views.ContentOrderView.as_view(), name='content_order'),
    path('subject/<slug:subject>/', views.CourseListView.as_view(), name='course_list_subject'),
    
    path('course/<int:pk>/', views.CourseRateDetaillView.as_view(), name='course_rate_detail'),
    
    path('course/<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    #path('course/<slug:slug>/', views.course_detail, name='course_detail'), 
    
    #path('course/<int:pk>/', views.CourseRateDetaillView.as_view(), name='course_rate_detail'),
    
    path('course_review/course/<int:pk>/', views.review_course, name='course_review'), 
    
    path('course_ratings/course/<int:pk>/', views.course_detail_review, name='course_detail_review'), 
    
]
