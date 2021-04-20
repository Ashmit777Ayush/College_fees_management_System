from django.test import TestCase

from fees.forms import *
from django.core.files.uploadedfile import SimpleUploadedFile



class StudentEnquiryFormTest(TestCase):
    def test_valid(self):
        form = StudentEnquiryForm(data={'roll':'1801032','name':'AShmit','email':'a@gmail.com','branch':'CSE','Enquiry':'xgy'})
        self.assertTrue(form.is_valid())

    def test_not_error_valid(self):
        form = StudentEnquiryForm(data={'roll':'1801032','name':'AShmit','email':'a@gmail.com','branch':'CSE','Enquiry':'xgy'})
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_enquiry_not_valid(self):
        form = StudentEnquiryForm(data={'roll':'1801032','name':'AShmit','email':'a@gmail.com','branch':'CSE','Enquiry':''})
        self.assertFalse(form.is_valid())

    def test_roll_not_valid(self):
        form = StudentEnquiryForm(data={'roll':'','name':'AShmit','email':'a@gmail.com','branch':'CSE','Enquiry':'fff'})
        self.assertFalse(form.is_valid())

    def test_error(self):
        form = StudentEnquiryForm(data={'roll':'','name':'AShmit','email':'a@gmail.com','branch':'CSE','Enquiry':'fff'})
        self.assertTrue(form.errors)


class StudentEnquiryFormUpdateTestCase(TestCase):
    def test_valid(self):
        form = StudentEnquiryFormUpdate(data={'roll':'1801032','name':'AShmit','email':'a@gmail.com','branch':'CSE','Enquiry':'hghfgwgf','Enquiry_status':'Yes'})
        self.assertTrue(form.is_valid())


    def test_not_error_valid(self):
        form = StudentEnquiryFormUpdate(data={'roll':'1801032','name':'AShmit','email':'a@gmail.com','branch':'CSE','Enquiry':'hghfgwgf','Enquiry_status':'Yes'})
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_enquiry_not_valid(self):
        form = StudentEnquiryFormUpdate(data={'roll':'1801032','name':'AShmit','email':'a@gmail.com','branch':'CSE','Enquiry':'','Enquiry_status':'Yes'})
        self.assertFalse(form.is_valid())

    def test_error_not_valid(self):
        form = StudentEnquiryFormUpdate(data={'roll':'1801032','name':'AShmit','email':'a@gmail.com','branch':'CSE','Enquiry':'','Enquiry_status':'Yes'})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

class AnnouncementFormTestCase(TestCase):
    def test_valid(self):
        form = AnnouncementForm(data={'Subject':'test','Query':'test','Status':'Normal','Show':'Show'})
        self.assertTrue(form.is_valid())

    def test_not_error_valid(self):
        form = AnnouncementForm(data={'Subject':'test','Query':'test','Status':'Normal','Show':'Show'})
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_Subject_not_valid(self):
        form = AnnouncementForm(data={'Subject':'','Query':'test','Status':'Normal','Show':'Show'})
        self.assertFalse(form.is_valid())

    def test_error_not_valid(self):
        form = AnnouncementForm(data={'Subject':'','Query':'test','Status':'Normal','Show':'Show'})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)


class UploadFileFormTestCase(TestCase):

    def test_not_valid(self):
        form = UploadFileForm(data={'title':'', 'file':'first.csv'})
        self.assertFalse(form.is_valid())

        
    def test_error_not_valid(self):
        form = UploadFileForm(data={'title':'', 'file':'first.csv'})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

class AutomateCreateSemesterTestCase(TestCase):
    def test_valid(self):
        form = AutomateCreateSemester(data={'semestertype':'first','monsoon_wintertype':'Monsoon','Year':'2018','branch':'CSE','course':'B_Tech'})
        self.assertTrue(form.is_valid())

    def test_not_error_valid(self):
        form = AutomateCreateSemester(data={'semestertype':'first','monsoon_wintertype':'Monsoon','Year':'2018','branch':'CSE','course':'B_Tech'})
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_not_valid(self):
        form = AutomateCreateSemester(data={'semestertype':'first','monsoon_wintertype':'','Year':'2018','branch':'CSE','course':'B_Tech'})
        self.assertFalse(form.is_valid())

    def test_error_not_valid(self):
        form = AutomateCreateSemester(data={'semestertype':'first','monsoon_wintertype':'','Year':'2018','branch':'CSE','course':'B_Tech'})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

class ChangePasswordAdminTestCase(TestCase):
    def test_Valid(self):
        form = ChangePasswordAdmin(data={'New_Password':'iiitgQ!1','Confirm_Password':'iiitgQ!1'})
        self.assertTrue(form.is_valid())

    def test_not_error_Valid(self):
        form = ChangePasswordAdmin(data={'New_Password':'iiitgQ!1','Confirm_Password':'iiitgQ!1'})
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_not_Valid(self):
        form = ChangePasswordAdmin(data={'New_Password':'iiitgQ!1','Confirm_Password':''})
        self.assertFalse(form.is_valid())

    def test_error_not_Valid(self):
        form = ChangePasswordAdmin(data={'New_Password':'iiitgQ!1','Confirm_Password':''})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)


class UploadFeesFileFormTestCase(TestCase):
    def test_not_valid(self):
        form = UploadFeesFileForm(data={'month':'', 'file':'first.csv'})
        self.assertFalse(form.is_valid())

    def test_error(self):
        form = UploadFeesFileForm(data={'month':'', 'file':'first.csv'})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)


class CreateStudentFormTestCase(TestCase):
    def test_valid(self):
        form = CreateStudentForm(data={'username':'1801022','email':'aspking.ash.aa@gmail.com','password1':'iiitgQ!1','password2':'iiitgQ!1','firstname':'ashmit','middlename':'a','lastname':'lop','phone':'7070772988','branch':'CSE','course':'Phd','Year':'2018'})
        self.assertTrue(form.is_valid())

    def test_no_error_valid(self):
        form = CreateStudentForm(data={'username':'1801022','email':'aspking.ash.aa@gmail.com','password1':'iiitgQ!1','password2':'iiitgQ!1','firstname':'ashmit','middlename':'a','lastname':'lop','phone':'7070772988','branch':'CSE','course':'Phd','Year':'2018'})
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_not_valid(self):
        form = CreateStudentForm(data={'username':'','email':'aspking.ash.aa@gmail.com','password1':'iiitgQ!1','password2':'iiitgQ!1','firstname':'ashmit','middlename':'a','lastname':'lop','phone':'7070772988','branch':'CSE','course':'Phd','Year':'2018'})
        self.assertFalse(form.is_valid())

    def test_error_not_valid(self):
        form = CreateStudentForm(data={'username':'','email':'aspking.ash.aa@gmail.com','password1':'iiitgQ!1','password2':'iiitgQ!1','firstname':'ashmit','middlename':'a','lastname':'lop','phone':'7070772988','branch':'CSE','course':'Phd','Year':'2018'})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)