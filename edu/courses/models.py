from django.db import models
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.shortcuts import reverse
from django.template.loader import render_to_string
from django.db.models import Avg, Count
from django.utils.translation import gettext_lazy as _
#from parler.models import TranslatableModel, TranslatedFields


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

def course_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/course_<id>/<filename>
    return 'course_{0}/{1}'.format(instance.course.id, filename)


class Category(models.Model):
    title = models.CharField(_('category title'), max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def countsubjects(self):
        #course_cnt = Course.objects.filter(subject__category).all()   #aggregate(count=Count('id'))
        subject_cnt = Subject.objects.annotate(total_subjects=Count('subject'))
        cnt=0
        if subject_cnt["count"] is not None:
            cnt = int(subject_cnt["count"])
        return cnt

    def get_absolute_url(self):
        """Returns the url to access a particular category instance."""
        return reverse('courses:category-detail', args=[str(self.id)])


class Subject(models.Model):
    category = models.ForeignKey(Category,
                                on_delete=models.CASCADE)
    title = models.CharField(_('subject title'), max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['category']   # 'title'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a particular subject instance."""
        return reverse('courses:subject-detail', args=[str(self.id)])


class Course(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                on_delete=models.CASCADE)  #related_name='courses',
    title = models.CharField(_('course title'), max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, through='StudentCourses',
                                      related_name='courses_joined', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(default='no_image.png',
                              upload_to='images')
    hours = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    class Meta:
        ordering = ['title']  #  title -created
        # index_together = (('id', 'slug'),)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def averagereview(self):
        review = Review.objects.filter(course=self).aggregate(average=Avg('rate'))
        avg=0
        if review["average"] is not None:
            avg=float(review["average"])
        return avg

    def countreview(self):
        reviews = Review.objects.filter(course=self).aggregate(count=Count('id'))
        cnt=0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a particular course instance."""
        return reverse('courses:course_detail', kwargs={'slug': self.slug}) #args=[str(self.id)]

    def get_suggestion_url(self):
        return f"/suggestion-info/{self.slug}/"


class StudentCourses(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    #class Meta:
        #verbose_name_plural = 'Ordered Items'
        #unique_together = ['order', 'orderitem']


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    def __str__(self):
        return f'{self.order}. {self.title}'

    class Meta:
        ordering = ['order']


class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in':(
                                     'text',
                                     'video',
                                     'image',
                                     'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string(f'courses/content/{self._meta.model_name}.html',
                                {'item': self})

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)
    image = models.ImageField(default='default.png',
                              upload_to=user_directory_path)

    def __str__(self):
        # return self.user.username
        return f'{self.user.username} UserProfile'


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length = 100, null=True, blank=True)
    comment = models.TextField(max_length=300, null=True, blank=True)
    rate = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    #class Meta:
    #    unique_together = ['user', 'course']

    def __str__(self):
        return str(self.id)
