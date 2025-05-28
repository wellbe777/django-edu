from django.contrib import admin
from .models import Category, Subject, Course, Module, UserProfile, Review
from django.contrib.auth.models import User
#from django.contrib.auth.admin import UserAdmin

# use memcache admin index site
admin.site.index_template = 'memcache_status/admin_index.html'

#class UserCustomAdmin(admin.UserAdmin):
#    list_display = ['id', 'username','email', 'first_name', 'last_name', 'last_login', 'groups', 'is_staff']

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'id', 'email', 'first_name', 'last_name', 'group', 'is_staff', 'is_superuser']
    def group(self, user):
        return ' '.join([g.name for g in user.groups.all()])
        
    list_filter = ['groups__name', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name']	
	#groups = []
    	#for group in user.groups.all():
        #   groups.append(group.name)
    	#return ' '.join(groups)
    	#group.short_description = 'Group'
    	
admin.site.unregister(User) 
admin.site.register(User, CustomUserAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created', 'hours', 'price', 'image']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
    

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'subject', 'comment', 'rate', 'created', 'updated']
    list_filter = ['rate', 'created']
    search_fields = ['course', 'rate', 'user']
