from django.http import response
from django.test import TestCase

# Create your tests here.
from fees.models import *
from fees.views import *
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import random, datetime


# admin home page       '/'
class ViewAdminHomeTestCase(TestCase):
    def setUp(self):
        admin = User.objects.create_user('admin','aspking.ash.aa@gmail.com', 'admin')
        Group.objects.get_or_create(name='admin')
        Group.objects.get_or_create(name='student')
        grp = Group.objects.get(name='admin')
        admin.groups.add(grp)
        admin.save()



        # creating students
        for x in range(10):
            name = 'student_{}'.format(x)
            mail = 'aspking.ash.aa@gmail{}.com'.format(x)
            student = User.objects.create_user('180103{}'.format(x), mail,'iiitgQ!1')
            grp = Group.objects.get(name='student')
            student.groups.add(grp)
            student.save()
            
            branch_ = ['CSE','ECE']
            course_ = ['B_Tech', 'M_Tech', 'Phd']
            Year_ = ['2018', '2019', '2020', '2022']
            Student.objects.create(
                user = student,
                roll = '180103{}'.format(x),
                email = mail,
                firstname = name,
                middlename = '',
                lastname = '',
                phone = '707077298{}'.format(x),
                branch = random.choices(branch_)[0],
                course = random.choices(course_)[0],
                Year = random.choices(Year_)[0],
            )

        # print(random.choices(course_)[0])
    def test_without_login(self):
        response = self.client.get(reverse('home'))
        # print(response)
        self.assertTrue(response,'/login/?next=/')

    def test_with_login(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get(reverse('home'))
        # print(response)
        self.assertEqual(response.status_code,200)
        # self.assertTrue(response,302)
        response = self.client.get('/', {'roll':'','email':''})
        self.assertTrue(response)

    def test_login_page_user(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get(reverse('home'))
        self.assertEqual(str(response.context['user']),'admin')

    def test_login_template_used(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'fees/dashboard.html')

    # testing the number of students in the student data
    def test_number_student(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get(reverse('home'))
        self.assertEqual(len(response.context['students']), 10)
        # self.assertTrue(response.context['btech'],)

        # print(response.context['btech'])
        # print(response.context['mtech'])
        # print(response.context['phd'])
        # print(response.context['students'])
        # for x in response.context['students']:
        #     print(x.course)



    def test_count_course(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get(reverse('home'))
        self.assertTrue(response.context['btech'])
        self.assertTrue(response.context['mtech'])
        self.assertTrue(response.context['phd'])


    #  particular student data
    def test_student_data(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get('/students/1801032/')
        # print(response)
        self.assertEqual(response.status_code, 200)

    def test_student_data_template(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get('/students/1801032/')
        # print(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed((response, 'fees/students.html'))

    #  create semester of each student
    def test_create_semester_page(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get('/createSemester/1801032/')
        self.assertEqual(response.status_code, 200)
    
    def test_create_semester_page_template(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get('/createSemester/1801032/')
        self.assertTemplateUsed(response, 'fees/semester_tab_form.html')
    
    def test_create_semester_valid_form_submit(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get('/createSemester/1801032/')
        response = self.client.post('/createSemester/1801032/', {'roll' : '1801032','semestertype' : 'first','monsoon_wintertype' : 'Monsoon','Year' : datetime.datetime.now().year,'tution_fee' : 100000,'hostel_fee' : 10000,'mon_1' : 'Jul','mon_2' : 'Aug','mon_3' : 'Sept','mon_4' : 'Oct','mon_5' : 'Nov','mon_6' : 'Dec','total_payment': 0,'dues': 0})
        self.assertRedirects(response, '/students/1801032/')

    def test_create_semester_not_valid_form_submit(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get('/createSemester/1801032/')
        response = self.client.post('/createSemester/1801032/', {'roll' : '1801032','semestertype' : '','monsoon_wintertype' : 'Monsoon','Year' : datetime.datetime.now().year,'tution_fee' : 100000,'hostel_fee' : 10000,'mon_1' : 'Jul','mon_2' : 'Aug','mon_3' : 'Sept','mon_4' : 'Oct','mon_5' : 'Nov','mon_6' : 'Dec','total_payment': 0,'dues': 0})
        self.assertFormError(response, 'form', 'semestertype', 'This field is required.')

    #  for the update part of the semester
    def test_update_semester_valid(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get('/createSemester/1801032/')
        response = self.client.post('/createSemester/1801032/', {'roll' : '1801032','semestertype' : 'first','monsoon_wintertype' : 'Monsoon','Year' : datetime.datetime.now().year,'tution_fee' : 100000,'hostel_fee' : 10000,'mon_1' : 'Jul','mon_2' : 'Aug','mon_3' : 'Sept','mon_4' : 'Oct','mon_5' : 'Nov','mon_6' : 'Dec','total_payment': 0,'dues': 0})
        response = self.client.post('/updateSemester/1/', {'roll' : '1801032','semestertype' : 'first','monsoon_wintertype' : 'Monsoon','Year' : datetime.datetime.now().year,'tution_fee' : 100000,'hostel_fee' : 12500,'mon_1' : 'Jul','mon_2' : 'Aug','mon_3' : 'Sept','mon_4' : 'Oct','mon_5' : 'Nov','mon_6' : 'Dec','total_payment': 0,'dues': 0})
        self.assertRedirects(response, '/students/1801032/')

    def test_update_semester_template(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.post('/createSemester/1801032/', {'roll' : '1801032','semestertype' : 'first','monsoon_wintertype' : 'Monsoon','Year' : datetime.datetime.now().year,'tution_fee' : 100000,'hostel_fee' : 10000,'mon_1' : 'Jul','mon_2' : 'Aug','mon_3' : 'Sept','mon_4' : 'Oct','mon_5' : 'Nov','mon_6' : 'Dec','total_payment': 0,'dues': 0})
        response = self.client.get('/updateSemester/1/')
        self.assertTemplateUsed(response, 'fees/semester_tab_form.html')

    def test_delete_semester(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.post('/createSemester/1801032/', {'roll' : '1801032','semestertype' : 'first','monsoon_wintertype' : 'Monsoon','Year' : datetime.datetime.now().year,'tution_fee' : 100000,'hostel_fee' : 10000,'mon_1' : 'Jul','mon_2' : 'Aug','mon_3' : 'Sept','mon_4' : 'Oct','mon_5' : 'Nov','mon_6' : 'Dec','total_payment': 0,'dues': 0})
        response = self.client.get('/deleteSemester/1/')
        self.assertEqual(response.status_code, 200)

    def test_delete_semester_template(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.post('/createSemester/1801032/', {'roll' : '1801032','semestertype' : 'first','monsoon_wintertype' : 'Monsoon','Year' : datetime.datetime.now().year,'tution_fee' : 100000,'hostel_fee' : 10000,'mon_1' : 'Jul','mon_2' : 'Aug','mon_3' : 'Sept','mon_4' : 'Oct','mon_5' : 'Nov','mon_6' : 'Dec','total_payment': 0,'dues': 0})
        response = self.client.get('/deleteSemester/1/')
        self.assertTemplateUsed(response, 'fees/semester_tab_delete.html')

    def test_delete_semester_template_valid(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.post('/createSemester/1801032/', {'roll' : '1801032','semestertype' : 'first','monsoon_wintertype' : 'Monsoon','Year' : datetime.datetime.now().year,'tution_fee' : 100000,'hostel_fee' : 10000,'mon_1' : 'Jul','mon_2' : 'Aug','mon_3' : 'Sept','mon_4' : 'Oct','mon_5' : 'Nov','mon_6' : 'Dec','total_payment': 0,'dues': 0})
        response = self.client.post('/deleteSemester/1/')
        # print(response)
        self.assertRedirects(response,'/students/1801032/')
        # response = self.client.get('/deleteSemester/1/')
        # self.assertEqual(response.status_code, 200)

    #  rendering each sem data
    def test_student_each_sem(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.post('/createSemester/1801032/', {'roll' : '1801032','semestertype' : 'first','monsoon_wintertype' : 'Monsoon','Year' : datetime.datetime.now().year,'tution_fee' : 100000,'hostel_fee' : 10000,'mon_1' : 'Jul','mon_2' : 'Aug','mon_3' : 'Sept','mon_4' : 'Oct','mon_5' : 'Nov','mon_6' : 'Dec','total_payment': 0,'dues': 0})
        response = self.client.get('/student_each_sem/1/')
        self.assertEqual(response.status_code,200)

    def test_student_each_sem_template(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.post('/createSemester/1801032/', {'roll' : '1801032','semestertype' : 'first','monsoon_wintertype' : 'Monsoon','Year' : datetime.datetime.now().year,'tution_fee' : 100000,'hostel_fee' : 10000,'mon_1' : 'Jul','mon_2' : 'Aug','mon_3' : 'Sept','mon_4' : 'Oct','mon_5' : 'Nov','mon_6' : 'Dec','total_payment': 0,'dues': 0})
        response = self.client.get('/student_each_sem/1/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'fees/student_each_sem.html')

    # update
    def test_updateStudent(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get('/update_student/1801032/')
        self.assertEqual(response.status_code,200 )

    def test_updateStudent_template(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get('/update_student/1801032/')
        self.assertEqual(response.status_code,200 )
        self.assertTemplateUsed(response, 'fees/student_update.html')

    #  post of update    if all ok then it will reflect redirect otherise 200 as it is on the same page
    def test_updateStudent_post_valid(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get('/update_student/1801032/')
        self.assertEqual(response.status_code,200 )
        response = self.client.post('/update_student/1801032/', {'roll':'1801032', 'email':'aspking.ash.aa@gmail.com', 'firstname':'Ash', 'middlename':'', 'lastname':'', 'branch':'CSE', 'course':'M_Tech', 'Year':'2018','phone':'7070772988'})
        self.assertRedirects(response,'/students/1801032/')

    #  delete
    def test_delete_student(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get('/deleteStudent/1801032/')
        self.assertEqual(response.status_code,200)

    #  delete template
    def test_delete_student_template(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get('/deleteStudent/1801032/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'fees/delete_student.html')
    
    #  delete post
    def test_delete_student_post_valid(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get('/deleteStudent/1801032/')
        self.assertEqual(response.status_code,200)

        response = self.client.post('/deleteStudent/1801032/')
        self.assertRedirects(response, '/')

    #  change Password by the admin
    def test_changePasswordAdmin(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get('/changePasswordAdmin/1801032/')
        self.assertEqual(response.status_code,200)


    

    #  testing the search filter in home
    #  try to use the filtyer part in the end
    def test_filter_home(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get('/', {'roll':'1801032','email':''})
        self.assertEqual(response.status_code,200)
        self.assertTrue(response)
        # print(response.context['students'])
        self.assertEqual(len(response.context['students']),1)



class ViewAdminRegistrationTestCase(TestCase):
    def setUp(self):
        admin = User.objects.create_user('admin','aspking.ash.aa@gmail.com', 'admin')
        Group.objects.get_or_create(name='admin')
        Group.objects.get_or_create(name='student')
        grp = Group.objects.get(name='admin')
        admin.groups.add(grp)
        admin.save()

    # registration of student
    def test_registration_student_with_login(self):
        login = self.client.login(username='admin',password='admin')
        response = self.client.get('/registration/')
        self.assertEqual(response.status_code, 200)

    def test_not_login(self):
        response = self.client.get(reverse('registration'))
        self.assertTrue(response, '/login/?next=/registration/')

    def test_template_registration(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get(reverse('registration'))
        self.assertTemplateUsed(response, 'fees/registration.html')

    def test_form_registration(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get(reverse('registration'))
        # print(response.context['form'])
        self.assertTrue(response.context['form'])

    def test_form_registration_attributes(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.get(reverse('registration'))
        #  for the field parts
        #  checking the field attributes exists or not
        self.assertTrue(response.context['form'].fields)
        self.assertTrue(response.context['form'].fields['username'])
        self.assertTrue(response.context['form'].fields['email'])
        self.assertTrue(response.context['form'].fields['password1'])
        self.assertTrue(response.context['form'].fields['password2'])
        self.assertTrue(response.context['form'].fields['firstname'])
        self.assertTrue(response.context['form'].fields['middlename'])
        self.assertTrue(response.context['form'].fields['lastname'])
        self.assertTrue(response.context['form'].fields['phone'])
        self.assertTrue(response.context['form'].fields['branch'])
        self.assertTrue(response.context['form'].fields['course'])
        self.assertTrue(response.context['form'].fields['Year'])

    def test_form_post_valid(self):
        login = self.client.login(username = 'admin',password='admin')
        # response = self.client.get(reverse('registration'))
        #  try to give link not revese
        response = self.client.post('/registration/',  {'username':'1801032','email':'aspking.ash.aa@gmail.com','password1':'iiitgQ!1','password2':'iiitgQ!1','firstname':'Ashmit','middlename':'not','lastname':'last', 'branch':'CSE', 'course':'B_Tech', 'Year':'2018', 'phone':'7070772988',})
        self.assertEqual(response.status_code,302)
        self.assertRaisesMessage(response,'Student was successfully Registered 1801032')
        
    def test_form_post_redirects(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.post('/registration/',  {'username':'1801032','email':'aspking.ash.aa@gmail.com','password1':'iiitgQ!1','password2':'iiitgQ!1','firstname':'Ashmit','middlename':'not','lastname':'last', 'branch':'CSE', 'course':'B_Tech', 'Year':'2018', 'phone':'7070772988',})
        self.assertRedirects(response, reverse('registration'))
        response = self.client.get(reverse('home'))
        self.assertEqual(len(response.context['students']), 1)

    def test_form_post_not_valid(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.post('/registration/',  {'username':'','email':'aspking.ash.aa@gmail.com','password1':'iiitgQ!1','password2':'iiitgQ!1','firstname':'Ashmit','middlename':'not','lastname':'last', 'branch':'CSE', 'course':'B_Tech', 'Year':'2018', 'phone':'7070772988',})
        self.assertEqual(response.status_code,200)

    def test_form_not_valid_error(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.post('/registration/',  {'username':'','email':'aspking.ash.aa@gmail.com','password1':'iiitgQ!1','password2':'iiitgQ!1','firstname':'Ashmit','middlename':'not','lastname':'last', 'branch':'CSE', 'course':'B_Tech', 'Year':'2018', 'phone':'7070772988',})
        self.assertFormError(response, 'form', 'username', 'This field is required.')

    # testing student created or not
    def test_successfully_created(self):
        login = self.client.login(username = 'admin',password='admin')

        # before
        response = self.client.get(reverse('home'))
        self.assertEqual(len(response.context['students']), 0)

        #  now creating
        response = self.client.post('/registration/',  {'username':'1801032','email':'aspking.ash.aa@gmail.com','password1':'iiitgQ!1','password2':'iiitgQ!1','firstname':'Ashmit','middlename':'not','lastname':'last', 'branch':'CSE', 'course':'B_Tech', 'Year':'2018', 'phone':'7070772988',})
        self.assertRedirects(response, reverse('registration'))

        #  after creating
        response = self.client.get(reverse('home'))
        self.assertEqual(len(response.context['students']), 1)


#  login logout
class LoginLogoutTestCase(TestCase):
    def setUp(self):
        admin = User.objects.create_superuser('admin','aspking.ash.aa@gmail.com', 'admin')
        Group.objects.get_or_create(name='admin')
        Group.objects.get_or_create(name='student')
        grp = Group.objects.get(name='admin')
        admin.groups.add(grp)
        admin.save()



        # creating students
        for x in range(10):
            name = 'student_{}'.format(x)
            mail = 'aspking.ash.aa@gmail{}.com'.format(x)
            student = User.objects.create_user('180103{}'.format(x), mail,'iiitgQ!1')
            grp = Group.objects.get(name='student')
            student.groups.add(grp)
            student.save()
            
            branch_ = ['CSE','ECE']
            course_ = ['B_Tech', 'M_Tech', 'Phd']
            Year_ = ['2018', '2019', '2020', '2022']
            Student.objects.create(
                user = student,
                roll = '180103{}'.format(x),
                email = mail,
                firstname = name,
                middlename = '',
                lastname = '',
                phone = '707077298{}'.format(x),
                branch = random.choices(branch_)[0],
                course = random.choices(course_)[0],
                Year = random.choices(Year_)[0],
            )

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/login/', {'username':'1801032', 'password':'iiitgQ!1','checker':'student'})
        # print(response)
        response = self.client.get('/user/')
        self.assertEqual(response.status_code,200)

    def test_login_page_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'fees/index.html')
    
    # student login
    def test_student_login_valid(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        # login = self.client.login(username='1801032', password='iiitgQ!1')
        login = self.client.post('/login/', {'username':'1801032', 'password':'iiitgQ!1','checker':'student'})
        # print(login)
        response = self.client.get('/user/')
        self.assertEqual(response.status_code, 200)


    def test_student_login_not_valid(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        # login = self.client.login(username='1801032', password='iiitgQ!')
        login = self.client.post('/login/', {'username':'1801032', 'password':'iiitgQ!','checker':'student'})
        # print(login)
        response = self.client.get('/user/')
        self.assertNotEqual(response.status_code, 200)

    
    # wrong login id link
    def test_student_login_not_valid_link(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        # login = self.client.login(username='1801032', password='iiitgQ!')
        login = self.client.post('/login/', {'username':'1801032', 'password':'iiitgQ!','checker':'student'})
        # print(login)
        response = self.client.get('/user/')
        self.assertTrue(response, '/login/?next=/user/')

    # without login
    def test_student_without_login(self):
        response = self.client.get('/user/')
        # print(response)
        self.assertTrue(response, '/login/?next=/user/')

    #  after login accessing adminpage
    def test_student_login_admin_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        # login = self.client.login(username='1801032', password='iiitgQ!1')
        login = self.client.post('/login/', {'username':'1801032', 'password':'iiitgQ!1','checker':'student'})
        # print(login)
        response = self.client.get('/')
        self.assertNotEqual(response.status_code, 200)
        # print(response)

    # admin login
    def test_admin_login_valid(self):
        # login = self.client.login(username='admin', password='admin')
        login = self.client.post('/login/', {'username':'admin', 'password':'admin','checker':'admin'})
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # admin login not valid
    def test_admin_login_not_valid(self):
        # login = self.client.login(username='admin', password='admi')
        login = self.client.post('/login/', {'username':'admin', 'password':'admin1','checker':'admin'})
        response = self.client.get('/')
        self.assertNotEqual(response.status_code, 200)

    def test_admin_login_not_valid_link(self):
        # login = self.client.login(username='admin', password='admi')
        login = self.client.post('/login/', {'username':'admin', 'password':'admin1','checker':'admin'})
        response = self.client.get('/')
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(response, '/login/?next=/user/')


    # student logout
    def test_student_logout(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        # login = self.client.login(username='1801032', password='iiitgQ!1')
        login = self.client.post('/login/', {'username':'1801032', 'password':'iiitgQ!1','checker':'student'})
        response = self.client.get('/user/')
        self.assertEqual(response.status_code,200 )
        # ---------
        # logout = self.client.logout()
        logout = self.client.post('/logout/')
        response = self.client.get('/user/')
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(response, '/login/?next=/user/')
        # print(logout)
    
    # admin logout
    def test_admin_logout(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        # login = self.client.login(username='admin', password='admin')
        login = self.client.post('/login/', {'username':'admin', 'password':'admin','checker':'admin'})
        response = self.client.get('/')
        self.assertEqual(response.status_code,200 )
        # ---------
        # logout = self.client.logout()
        logout = self.client.post('/logout/')
        response = self.client.get('/')
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(response, '/login/?next=/user/')


#  testing for the student 
class StudentTestCase(TestCase):
    def setUp(self):
        admin = User.objects.create_superuser('admin','aspking.ash.aa@gmail.com', 'admin')
        Group.objects.get_or_create(name='admin')
        Group.objects.get_or_create(name='student')
        grp = Group.objects.get(name='admin')
        admin.groups.add(grp)
        admin.save()



        # creating students
        for x in range(10):
            name = 'student_{}'.format(x)
            mail = 'aspking.ash.aa@gmail{}.com'.format(x)
            student = User.objects.create_user('180103{}'.format(x), mail,'iiitgQ!1')
            grp = Group.objects.get(name='student')
            student.groups.add(grp)
            student.save()
            
            branch_ = ['CSE','ECE']
            course_ = ['B_Tech', 'M_Tech', 'Phd']
            Year_ = ['2018', '2019', '2020', '2022']
            Student.objects.create(
                user = student,
                roll = '180103{}'.format(x),
                email = mail,
                firstname = name,
                middlename = '',
                lastname = '',
                phone = '707077298{}'.format(x),
                branch = random.choices(branch_)[0],
                course = random.choices(course_)[0],
                Year = random.choices(Year_)[0],
            )
    # mainpage
    def test_student_userpage(self):
        login =self.client.login(username='1801032',password='iiitgQ!1')
        response = self.client.get('/user/')
        self.assertEqual(response.status_code,200)
        
    def test_student_userpage_template(self):
        login =self.client.login(username='1801032',password='iiitgQ!1')
        response = self.client.get('/user/')
        self.assertEqual(response.status_code,200)  
        self.assertTemplateUsed(response, 'fees/user.html')

    #  first create semester then check the data
    def test_student_userpage_data(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.post('/createSemester/1801032/', {'roll' : '1801032','semestertype' : 'first','monsoon_wintertype' : 'Monsoon','Year' : datetime.datetime.now().year,'tution_fee' : 100000,'hostel_fee' : 10000,'mon_1' : 'Jul','mon_2' : 'Aug','mon_3' : 'Sept','mon_4' : 'Oct','mon_5' : 'Nov','mon_6' : 'Dec','total_payment': 0,'dues': 0})
        self.client.logout()
        login =self.client.login(username='1801032',password='iiitgQ!1')
        response = self.client.get('/user/')
        self.assertTrue(response.context['student_data'])
        self.assertTrue(response.context['semester_tabs'])

    def test_user_student_each_sem(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.post('/createSemester/1801032/', {'roll' : '1801032','semestertype' : 'first','monsoon_wintertype' : 'Monsoon','Year' : datetime.datetime.now().year,'tution_fee' : 100000,'hostel_fee' : 10000,'mon_1' : 'Jul','mon_2' : 'Aug','mon_3' : 'Sept','mon_4' : 'Oct','mon_5' : 'Nov','mon_6' : 'Dec','total_payment': 0,'dues': 0})
        self.client.logout()
        login =self.client.login(username='1801032',password='iiitgQ!1')

        response = self.client.get('/user_student_each_sem/1/')
        self.assertEqual(response.status_code,200)

    def test_user_student_each_sem_template(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.post('/createSemester/1801032/', {'roll' : '1801032','semestertype' : 'first','monsoon_wintertype' : 'Monsoon','Year' : datetime.datetime.now().year,'tution_fee' : 100000,'hostel_fee' : 10000,'mon_1' : 'Jul','mon_2' : 'Aug','mon_3' : 'Sept','mon_4' : 'Oct','mon_5' : 'Nov','mon_6' : 'Dec','total_payment': 0,'dues': 0})
        self.client.logout()
        login =self.client.login(username='1801032',password='iiitgQ!1')

        response = self.client.get('/user_student_each_sem/1/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed((response, 'fees/user_student_each_sem.html'))

    def test_user_student_each_sem_data(self):
        login = self.client.login(username = 'admin',password='admin')
        response = self.client.post('/createSemester/1801032/', {'roll' : '1801032','semestertype' : 'first','monsoon_wintertype' : 'Monsoon','Year' : datetime.datetime.now().year,'tution_fee' : 100000,'hostel_fee' : 10000,'mon_1' : 'Jul','mon_2' : 'Aug','mon_3' : 'Sept','mon_4' : 'Oct','mon_5' : 'Nov','mon_6' : 'Dec','total_payment': 0,'dues': 0})
        self.client.logout()
        login =self.client.login(username='1801032',password='iiitgQ!1')

        response = self.client.get('/user_student_each_sem/1/')
        self.assertTrue(response.context['current_sem'])
        self.assertTrue(response.context['student_data'])



class AnnouncementTestCase(TestCase):
    def setUp(self):
        admin = User.objects.create_superuser('admin','aspking.ash.aa@gmail.com', 'admin')
        Group.objects.get_or_create(name='admin')
        Group.objects.get_or_create(name='student')
        grp = Group.objects.get(name='admin')
        admin.groups.add(grp)
        admin.save()



        # creating students
        for x in range(10):
            name = 'student_{}'.format(x)
            mail = 'aspking.ash.aa@gmail{}.com'.format(x)
            student = User.objects.create_user('180103{}'.format(x), mail,'iiitgQ!1')
            grp = Group.objects.get(name='student')
            student.groups.add(grp)
            student.save()
            
            branch_ = ['CSE','ECE']
            course_ = ['B_Tech', 'M_Tech', 'Phd']
            Year_ = ['2018', '2019', '2020', '2022']
            Student.objects.create(
                user = student,
                roll = '180103{}'.format(x),
                email = mail,
                firstname = name,
                middlename = '',
                lastname = '',
                phone = '707077298{}'.format(x),
                branch = random.choices(branch_)[0],
                course = random.choices(course_)[0],
                Year = random.choices(Year_)[0],
            )

            
    def test_announcement(self):
        login = self.client.login(username='admin', password='admin')
        response = self.client.get('/announcement/')
        self.assertEqual(response.status_code,200)

    def test_announcement_template(self):
        login = self.client.login(username='admin', password='admin')
        response = self.client.get('/announcement/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'fees/announcement.html')

    #  new announcement
    def test_create_announcement(self):
        login = self.client.login(username='admin', password='admin')
        response = self.client.get('/announcement_new/')
        self.assertEqual(response.status_code,200)

    def test_create_announcement_template(self):
        login = self.client.login(username='admin', password='admin')
        response = self.client.get('/announcement_new/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'fees/create_announcement.html')

    def test_create_announcement_valid(self):
        login = self.client.login(username='admin', password='admin')
        response =self.client.post('/announcement_new/', {'Subject':'first', 'Query':'testing', 'Status':'Normal', 'Show':'Show'})
        self.assertRedirects(response,'/announcement_new/')

    def test_create_announcement_not_valid(self):
        login = self.client.login(username='admin', password='admin')
        response =self.client.post('/announcement_new/', {'Subject':'', 'Query':'testing', 'Status':'Normal', 'Show':'Show'})
        self.assertFormError(response, 'form', 'Subject', 'This field is required.')

    def test_filter_announcement(self):
        login = self.client.login(username='admin', password='admin')
        response =self.client.post('/announcement_new/', {'Subject':'first', 'Query':'testing', 'Status':'Normal', 'Show':'Show'})
        response = self.client.get('/announcement/', {'start':'18-04-21','end':''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['announcements']),1)

    #  update/open announcement
    def test_open_announcement(self):
        login = self.client.login(username='admin', password='admin')
        response =self.client.post('/announcement_new/', {'Subject':'first', 'Query':'testing', 'Status':'Normal', 'Show':'Show'})
        response = self.client.get('/open_announcement/1/')
        self.assertEqual(response.status_code, 200)

    #  update/open announcement template
    def test_open_announcement_template(self):
        login = self.client.login(username='admin', password='admin')
        response =self.client.post('/announcement_new/', {'Subject':'first', 'Query':'testing', 'Status':'Normal', 'Show':'Show'})
        response = self.client.get('/open_announcement/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'fees/open_announcement.html')


    #  valid update
    def test_open_announcement(self):
        login = self.client.login(username='admin', password='admin')
        response =self.client.post('/announcement_new/', {'Subject':'first', 'Query':'testing', 'Status':'Normal', 'Show':'Show'})
        response = self.client.post('/open_announcement/1/', {'Subject':'first', 'Query':'testing', 'Status':'Urgent', 'Show':'Show'})
        self.assertRedirects(response,'/announcement/')


    #   student will see the announcements
    def test_student_announcement(self):
        login = self.client.login(username='1801032', password='iiitgQ!1')
        response = self.client.get('/announcement_student/')
        self.assertEqual(response.status_code, 200)

    def test_student_announcement_template(self):
        login = self.client.login(username='1801032', password='iiitgQ!1')
        response = self.client.get('/announcement_student/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed((response,'fees/announcement_student.html'))


# enquiry
class EnquiryTestCase(TestCase):
    def setUp(self):
        admin = User.objects.create_superuser('admin','aspking.ash.aa@gmail.com', 'admin')
        Group.objects.get_or_create(name='admin')
        Group.objects.get_or_create(name='student')
        grp = Group.objects.get(name='admin')
        admin.groups.add(grp)
        admin.save()
        # creating students
        for x in range(10):
            name = 'student_{}'.format(x)
            mail = 'aspking.ash.aa@gmail.com'.format(x)
            student = User.objects.create_user('180103{}'.format(x), mail,'iiitgQ!1')
            grp = Group.objects.get(name='student')
            student.groups.add(grp)
            student.save()
            
            branch_ = ['CSE','ECE']
            course_ = ['B_Tech', 'M_Tech', 'Phd']
            Year_ = ['2018', '2019', '2020', '2022']
            Student.objects.create(
                user = student,
                roll = '180103{}'.format(x),
                email = mail,
                firstname = name,
                middlename = '',
                lastname = '',
                phone = '707077298{}'.format(x),
                branch = random.choices(branch_)[0],
                course = random.choices(course_)[0],
                Year = random.choices(Year_)[0],
            )
    # student enquiry
    def test_enquiry(self):
        login = self.client.login(username='1801032', password='iiitgQ!1')
        response = self.client.get('/enquiry/')
        self.assertEqual(response.status_code, 200)

    def test_enquiry_template(self):
        login = self.client.login(username='1801032', password='iiitgQ!1')
        response = self.client.get('/enquiry/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fees/enq.html')

    #  valid enq
    def test_enquiry_valid(self):
        login = self.client.login(username='1801032', password='iiitgQ!1')
        response = self.client.get('/enquiry/')
        response = self.client.post('/enquiry/', {'roll':'1801032','name':'Ashmit','email':'aspking.ash.aa@gmail.com','branch':'CSE','Enquiry':'testing for the enquiry'})
        self.assertRedirects(response,'/enquiry/')

    def test_enquiry_not_valid(self):
        login = self.client.login(username='1801032', password='iiitgQ!1')
        response = self.client.get('/enquiry/')
        response = self.client.post('/enquiry/', {'roll':'1801032','name':'','email':'aspking.ash.aa@gmail.com','branch':'CSE','Enquiry':'testing for the enquiry'})
        self.assertFormError(response, 'form', 'name', 'This field is required.')


    # admin + template
    def test_enquiry_admin(self):
        login = self.client.login(username='1801032', password='iiitgQ!1')
        response = self.client.get('/enquiry/')
        response = self.client.post('/enquiry/', {'roll':'1801032','name':'Ashmit','email':'aspking.ash.aa@gmail.com','branch':'CSE','Enquiry':'testing for the enquiry'})
        self.client.logout()

        self.client.login(username='admin', password='admin')
        response = self.client.get('/enquiry_admin/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'fees/enq_admin.html')

    # admin admin data
    def test_enquiry_admin_check(self):
        login = self.client.login(username='1801032', password='iiitgQ!1')
        response = self.client.get('/enquiry/')
        response = self.client.post('/enquiry/', {'roll':'1801032','name':'Ashmit','email':'aspking.ash.aa@gmail.com','branch':'CSE','Enquiry':'testing for the enquiry'})
        self.client.logout()

        self.client.login(username='admin', password='admin')
        response = self.client.get('/enquiry_admin/')
        self.assertEqual(len(response.context['enquiries']),1)

        
    #  filter of form by admin
    def test_enquiry_admin_filter(self):
        login = self.client.login(username='1801032', password='iiitgQ!1')
        response = self.client.get('/enquiry/')
        response = self.client.post('/enquiry/', {'roll':'1801032','name':'Ashmit','email':'aspking.ash.aa@gmail.com','branch':'CSE','Enquiry':'testing for the enquiry'})
        self.client.logout()


        self.client.login(username='admin', password='admin')
        response = self.client.get('/enquiry_admin/', {'start':'18-04-2021','end':''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['enquiries']),1)

    #  enquiry render/update + template
    def test_enquiry_render(self):
        login = self.client.login(username='1801032', password='iiitgQ!1')
        response = self.client.get('/enquiry/')
        response = self.client.post('/enquiry/', {'roll':'1801032','name':'Ashmit','email':'aspking.ash.aa@gmail.com','branch':'CSE','Enquiry':'testing for the enquiry'})
        self.client.logout()


        self.client.login(username='admin', password='admin')
        response = self.client.get('/enquiry_render/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fees/part_enq.html')

    # updated only
    def test_enquiry_render_updated(self):
        login = self.client.login(username='1801032', password='iiitgQ!1')
        response = self.client.get('/enquiry/')
        response = self.client.post('/enquiry/', {'roll':'1801032','name':'Ashmit','email':'aspking.ash.aa@gmail.com','branch':'CSE','Enquiry':'testing for the enquiry'})
        self.client.logout()

        self.client.login(username='admin', password='admin')
        response = self.client.post('/enquiry_render/1/',{'roll':'1801032','name':'Ashmit','email':'aspking.ash.aa@gmail.com','branch':'CSE','Enquiry':'testing for the enquiry','Enquiry_status':'Yes'})
        self.assertRedirects(response,'/enquiry_admin/')