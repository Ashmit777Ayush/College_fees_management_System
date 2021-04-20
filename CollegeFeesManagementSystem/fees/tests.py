from django.test import TestCase

# Create your tests here.
from .models import *
from django.contrib.auth.models import User


class StudentUserTestCase(TestCase):
    def SetUpTestData(self):
        user = User.objects.create_user('1801033','ashmit.ayush@iiitg.ac.in','iiitgQ!1')
        Student.objects.create(user=user, roll=user.username, firstname='Ashmit',middlename='',lastname='Ayush',email=user.email, phone=7070772988, branch='CSE',course='B_Tech', Year='2018')

    def test_RollTest(self):
        student = Student.objects.get(roll='1801033')
        self.assertEqual(student.roll, '1801033')
    
    def test_FirstNameLabel(self):
        student = Student.objects.get(roll='1801033')
        field_label = student._meta.get_field('firstname').verbose_name
        self.assertEqual(field_label, 'First_Name')

