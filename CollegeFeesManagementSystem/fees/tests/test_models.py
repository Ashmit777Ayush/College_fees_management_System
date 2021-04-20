from django.test import TestCase

# Create your tests here.
from fees.models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class StudentUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('1801033','ashmit.ayush@iiitg.ac.in','iiitgQ!1')
        Student.objects.create(user=user, roll=user.username, firstname='Ashmit',middlename='',lastname='Ayush',email=user.email, phone=7070772988, branch='CSE',course='B_Tech', Year='2018')

    def test_RollTest(self):
        student = Student.objects.get(roll='1801033')
        self.assertEqual(student.roll, '1801033')

    def test_branch(self):
        student = Student.objects.get(roll='1801033')
        self.assertNotEqual(student.branch, 'ECE')
        self.assertEqual(student.branch, 'CSE')
    
    def test_FirstNameLabel(self):
        student = Student.objects.get(roll='1801033')
        field_label = student._meta.get_field('firstname').verbose_name
        self.assertEqual(field_label, 'First_Name')

    def test_str(self):
        student = Student.objects.get(roll='1801033')
        str_student = '{}'.format(1801033)
        self.assertEqual(str(student), str_student)

    def test_datecreated(self):
        student = Student.objects.get(roll='1801033')
        self.assertTrue(student.datecreated)


class SemetserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('1801033','ashmit.ayush@iiitg.ac.in','iiitgQ!1')
        cls.student1 = Student.objects.create(user=user, roll=user.username, firstname='Ashmit',middlename='',lastname='Ayush',email=user.email, phone=7070772988, branch='CSE',course='B_Tech', Year='2018')
        Semester.objects.create(roll=cls.student1,semestertype='first', monsoon_wintertype='Monsoon',Year=2018,tution_fee=100000,hostel_fee=12500)

    def test_hostel_fee(self):
        sem = Semester.objects.get(id='1')
        sem_hostel_fee = '12500'
        self.assertEquals(sem.hostel_fee, sem_hostel_fee)
        self.assertNotEquals(sem.hostel_fee, '12600')

    def test_roll(self):
        sem = Semester.objects.get(id='1')
        self.assertEquals(sem.roll.roll, '1801033')
        self.assertNotEquals(sem.roll.roll, '1801032')


    def test_year_label(self):
        sem = Semester.objects.get(id='1')
        field_label = sem._meta.get_field('Year').verbose_name
        self.assertEqual(field_label, 'Year')
        self.assertNotEqual(field_label, 'year')


    def test_datecreated(self):
        sem = Semester.objects.get(id='1')
        self.assertTrue(sem.datecreated)


        
class EnquiryTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.enq1 = EnquiryForm.objects.create(roll='1801032', name='Ashmit Ayush',email="ashmit.ayush@iiitg.ac.in",branch='CSE',Enquiry='testing the enquiry')
        cls.enq2 = EnquiryForm.objects.create(roll='1801033', name='Akash Kapil',email="cancrushon@gmail.com",branch='CSE',Enquiry='testing the enquiry form again')



    def test_roll(self):
        enq1 = EnquiryForm.objects.get(id='1')
        enq2 = EnquiryForm.objects.get(id='2')
        self.assertEqual(enq1.roll,'1801032')
        self.assertNotEqual(enq2.roll,'1801032')

    # as enquiry must be there so testing for the enquiry in the enquiry form
    def test_Enquiry(self):
        enq1 = EnquiryForm.objects.get(id='1')
        enq2 = EnquiryForm.objects.get(id='2')
        self.assertTrue(enq1.Enquiry)
        self.assertTrue(enq2.Enquiry)

    def test_email(self):
        enq1 = EnquiryForm.objects.get(id='1')
        enq2 = EnquiryForm.objects.get(id='2')
        self.assertNotEqual(enq1.email, 'cancrushon@gmail.com')
        self.assertEqual(enq1.email, 'ashmit.ayush@iiitg.ac.in')
        self.assertEqual(enq2.email, 'cancrushon@gmail.com')


    def test_datecreated(self):
        enq1 = EnquiryForm.objects.get(id='1')
        self.assertTrue(enq1.datecreated)



class AnnouncementTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Announcement.objects.create(Subject='Fees DeadLine', Query='Deadline is 12 th off April 2021', Status='Normal', Show='Show')

    def test_Query(self):
        ann_1 = Announcement.objects.get(id='1')
        self.assertTrue(ann_1.Query)

    def test_subject(self):
        ann_1 = Announcement.objects.get(id='1')
        field_label = ann_1._meta.get_field('Subject').verbose_name
        self.assertEqual(field_label, 'Subject')
        self.assertEqual(ann_1.Subject, 'Fees DeadLine')
        self.assertNotEqual(ann_1.Subject, 'Fees new DeadLine')
        

    def test_show(self):
        ann_1 = Announcement.objects.get(id='1')
        field_label = ann_1._meta.get_field('Show').verbose_name
        self.assertEqual(field_label, 'Show')
        field_label = ann_1._meta.get_field('Show').verbose_name
        self.assertEqual(field_label, 'Show')
        self.assertEqual(ann_1.Show, 'Show')
        self.assertNotEqual(ann_1.Show, 'Remove')

        

    def test_datecreated(self):
        ann1 = Announcement.objects.get(id='1')
        self.assertTrue(ann1.datecreated)


class RegisterFileTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        RegisterFile.objects.create(title='testing', uploaded_file='first.csv',roll_no='1801032,1801012',email='aspking.ash.aa@gmail.com akash.kapil@gmail.com', password='iiitgQ!1 iiitgQ!1')

    def test_file(self):
        reg1 = RegisterFile.objects.get(id=1)
        self.assertTrue(reg1.uploaded_file)

    def test_title(self):
        reg1 = RegisterFile.objects.get(id=1)
        field_label = reg1._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Title')
        self.assertEqual(reg1.title, 'testing')

    def test_email_sent(self):
        reg1 = RegisterFile.objects.get(id=1)
        self.assertEqual(reg1.email_sent, 'NO')
        self.assertNotEqual(reg1.email_sent, 'YES')
        

    def test_datecreated(self):
        reg1 = RegisterFile.objects.get(id='1')
        self.assertTrue(reg1.datecreated)


class Automate_Create_SemesterTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Automate_Create_Semester.objects.create(semestertype='first',monsoon_wintertype='Monsoon', Year='2018', branch='CSE', course='B_Tech', tution_fee=100000, hostel_fee=12500)

    def test_semestertype(self):
        a1 = Automate_Create_Semester.objects.get(id=1)
        field_label = a1._meta.get_field('semestertype').verbose_name
        self.assertEqual(field_label, 'Semester_type')
        self.assertEqual(a1.semestertype, 'first')

    def test_monsoon_wintertype(self):
        a1 = Automate_Create_Semester.objects.get(id=1)
        field_label = a1._meta.get_field('monsoon_wintertype').verbose_name
        self.assertEqual(field_label, 'Monsoon_or_Winter')
        self.assertEqual(a1.monsoon_wintertype, 'Monsoon')
        self.assertNotEqual(a1.monsoon_wintertype, 'Winter')


    def test_course(self):
        a1 = Automate_Create_Semester.objects.get(id=1)
        self.assertEqual(a1.course, 'B_Tech')
        self.assertNotEqual(a1.course, 'M_Tech')


    def test_hostel_fee(self):
        a1 = Automate_Create_Semester.objects.get(id=1)
        self.assertEqual(a1.hostel_fee, '12500')

    def test_branch(self):
        a1 = Automate_Create_Semester.objects.get(id=1)
        self.assertEqual(a1.branch, 'CSE')
        self.assertNotEqual(a1.branch, 'ECE')

    def test_tuition(self):
        a1 = Automate_Create_Semester.objects.get(id=1)
        self.assertEqual(a1.tution_fee, '100000')
        self.assertNotEqual(a1.tution_fee, '1000')


    def test_datecreated(self):
        a1 = Automate_Create_Semester.objects.get(id='1')
        self.assertTrue(a1.datecreated)
