from django.forms import ModelForm
from .models import *

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SemesterForm(ModelForm):
    class Meta:
        model = Semester
        fields = '__all__'



class CreateStudentForm(UserCreationForm):

    username = forms.CharField(max_length=7)
    firstname = forms.CharField(max_length=100)
    middlename = forms.CharField(max_length=100, required=False)
    lastname = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(max_length=100)
    phone = forms.CharField(max_length=15)
    branch = forms.CharField(max_length=3, widget=forms.Select(choices=BranchType))
    course = forms.CharField(max_length=6, widget=forms.Select(choices=CourseType))
    Year = forms.CharField(max_length=4, widget=forms.Select(choices=YearType))
    class Meta:
        model = User
        fields = ['username','email', 'password1','password2','firstname','middlename','lastname','phone','branch','course','Year',]


class UpdateStudent(ModelForm):
    class Meta:
        model = Student
        fields = ['roll','email','firstname','middlename','lastname','phone','Year','branch','course',]

class StudentEnquiryForm(ModelForm):
    class Meta:
        model = EnquiryForm
        fields = ['roll', 'name', 'email', 'branch', 'Enquiry']

class StudentEnquiryFormUpdate(ModelForm):
    class Meta:
        model = EnquiryForm
        fields = '__all__'

class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        fields = '__all__'


# for the uploading part for the registration
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


#  for the create semester automatically
class AutomateCreateSemester(ModelForm):
    class Meta:
        model = Automate_Create_Semester
        fields = '__all__'

#  for the fees part
class UploadFeesFileForm(forms.Form):
    month = forms.CharField(max_length=4, widget=forms.Select(choices=MonthType))
    file = forms.FileField()

#  for the user ppassword change
class ChangePasswordAdmin(forms.Form):
    New_Password = forms.CharField(min_length=8)
    Confirm_Password = forms.CharField(min_length=8)