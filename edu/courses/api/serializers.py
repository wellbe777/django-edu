from rest_framework import serializers
from ..models import Category, Subject, Course, Module, Content, UserProfile, Review

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'order', 'title', 'description']

        
class CourseSerializer(serializers.HyperlinkedModelSerializer):
    #module_name = ModuleSerializer(source='modules', many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='api:course_det')
    
    class Meta:
        model = Course
        #fields = ('id', 'owner', 'subject', 'title', 'slug', 'overview', 'created', 'students', 'price', 'image', 'hours', 'module_name')
        fields = ('title', 'url',)
        
class CourseDetailSerializer(serializers.ModelSerializer):
    #module_name = ModuleSerializer(source='modules', many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = ('id', 'owner', 'subject', 'title', 'slug', 'overview', 'created', 'students', 'price', 'image', 'hours')

    
class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    #courses = CourseSerializer(source='course_set', many=True, read_only=True)
    #courses = serializers.HyperlinkedRelatedField(source='course_set', many=True, read_only=True, view_name='api:course_det')
    url = serializers.HyperlinkedIdentityField(view_name='api:subject_det')
    
    class Meta:
        model = Subject
        fields = ('title', 'url',)
        
class SubjectDetailSerializer(serializers.HyperlinkedModelSerializer):
    course_title = serializers.StringRelatedField(source='course_set', many=True, read_only=True)
    course_url = serializers.HyperlinkedRelatedField(source='course_set', many=True, read_only=True, view_name='api:course_det')
    
    class Meta:
        model = Subject
        fields = ('title', 'course_title', 'course_url',)

# 1 - category with its url
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    #subjects = SubjectSerializer(source='subject_set', many=True, read_only=True)
    #subjects = serializers.HyperlinkedRelatedField(source='subject_set', many=True, read_only=True, view_name='api:subject_det')
    url = serializers.HyperlinkedIdentityField(view_name='api:category_det')
        
    class Meta:
        model = Category
        fields = ('title', 'url',)
        #depth = 3

# 2 - subject for category from 1 with its url
class CategoryDetailSerializer(serializers.HyperlinkedModelSerializer):
    subject_title = serializers.StringRelatedField(source='subject_set', many=True, read_only=True)
    subject_url = serializers.HyperlinkedRelatedField(source='subject_set', many=True, read_only=True, view_name='api:subject_det')
    
    class Meta:
        model = Category
        fields = ('title', 'subject_title', 'subject_url',)   #'slug', , 'id', 'title', 'subjects'
        #exclude = ('slug', 'title', 'subjects')


class ItemRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.render()

        
class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)
    
    class Meta:
        model = Content
        fields = ['order', 'item']

