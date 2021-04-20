from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Student)
admin.site.register(Semester)
admin.site.register(EnquiryForm)
admin.site.register(Announcement)
admin.site.register(Automate_Create_Semester)
admin.site.register(RegisterFile)