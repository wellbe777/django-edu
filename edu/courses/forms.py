from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module, UserProfile, Review
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User


ModuleFormSet = inlineformset_factory(Course,
                                      Module,
                                      fields=['title',
                                              'description'],
                                      extra=2,
                                      can_delete=True)
                                      

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
        

class ChangeUserFnameLname(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        labels = {'first_name': 'First name', 'last_name': 'Last name'}


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class SearchForm(forms.Form):
    query = forms.CharField(
        label="Search",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'search-input', 'placeholder': 'Search...'})
    )
    

class EmailContactForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


#CHOICES = [('1','One Star'),('2','Two Stars'),('3','Three Stars'),('4','Four Stars'),('5','Five Stars'),]
RATE_CHOICES = (('1','One Star'), ('2','Two Stars'), ('3','Three Stars'), ('4','Four Stars'), ('5','Five Stars'))

class CourseReviewForm(forms.Form):
    #CHOICES = (('1','One Star'),('2','Two Stars'),('3','Three Stars'),('4','Four Stars'),('5','Five Stars'),)
    #course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput)
    #rate = forms.IntegerField(required=True)
    rate = forms.TypedChoiceField(label='Please rate this course', choices=RATE_CHOICES, widget=forms.RadioSelect, coerce=int, required=True)
    subject = forms.CharField(max_length = 100, required=False)
    comment = forms.CharField(max_length=300, widget=forms.Textarea, required=False)
