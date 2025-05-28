from rest_framework import serializers
from .models import Category, Subject, Course, Module, Content, UserProfile, Review

        
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'owner', 'subject', 'title', 'slug', 'overview', 'created', 'students', 'price', 'image', 'hours')
        

class SubjectSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(source='course_set', many=True, read_only=True)
    
    class Meta:
        model = Subject
        fields = ('id', 'title', 'slug', 'category_id', 'courses')


class CategorySerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(source='subject_set', many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ('title', 'slug', 'subjects')
        #depth = 3
