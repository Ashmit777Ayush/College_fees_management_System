import django_filters
from .models import *

from django_filters import DateFilter
from django.forms import DateInput

class StudentFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = ['roll', 'email']

class EnquiryFilter(django_filters.FilterSet):
    start = DateFilter(label = 'Start_date', field_name = 'datecreated', lookup_expr = 'gte', widget=DateInput(attrs={'type': 'date'}))
    end = DateFilter(label = 'End_date', field_name = 'datecreated', lookup_expr = 'lte', widget=DateInput(attrs={'type': 'date'}) )
    # end_date = DateFilter(field_name = 'date_created', lookup_expr = 'lte')
    class Meta:
        model = EnquiryForm
        fields = ['roll', 'start', 'end', 'Enquiry_status']



class AnnouncementFilter(django_filters.FilterSet):
    start = DateFilter(label = 'Start_date', field_name = 'datecreated', lookup_expr = 'gte', widget=DateInput(attrs={'type': 'date'}))
    end = DateFilter(label = 'End_date', field_name = 'datecreated', lookup_expr = 'lte', widget=DateInput(attrs={'type': 'date'}))
    # end_date = DateFilter(field_name = 'date_created', lookup_expr = 'lte')
    class Meta:
        model = Announcement
        fields = ['start', 'end', 'Status', 'Show']


class RegisteredDetails(django_filters.FilterSet):
    start = DateFilter(label = 'Start_date', field_name = 'datecreated', lookup_expr='gte', widget=DateInput(attrs={'type':'date'}))
    end = DateFilter(label='End_date', field_name='datecreated', lookup_expr='lte',widget=DateInput(attrs={'type' :'date'}))

    class Meta:
        model = RegisterFile
        fields = ['start', 'end']