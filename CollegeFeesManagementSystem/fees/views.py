from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

from django.forms import inlineformset_factory
from django.contrib.auth.forms import AdminPasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *

from .forms import *
from .filters import *
from .decorators import *


# for mailing
from django.core.mail import send_mail
from django.template import loader

#  forr reverse page
from django.urls import reverse



# @allowed_users(allowed_roles=['admin'])
@login_required(login_url = 'login')
@admin_only
def home(request):
    students = Student.objects.all().order_by('-datecreated')
    

    # status part start
    btech = Student.objects.filter(course='B_Tech').count()
    mtech = Student.objects.filter(course='M_Tech').count()
    phd = Student.objects.filter(course='Phd').count()
    # status part end

    #  for the form
    myfilter = StudentFilter(request.GET, queryset=students)
    if request.method == 'GET':
        students = myfilter.qs
        

    context = {'students':students, 'btech':btech, 'mtech':mtech, 'phd':phd, 'myfilter':myfilter}
    return render(request,'fees/dashboard.html',context)



@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def student(request, pk):
    
    student_data = Student.objects.get(roll=pk)
    semester_tabs = student_data.semester_set.all()

    context = {'student_data':student_data, 'semester_tabs':semester_tabs}
    return render(request, 'fees/students.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def updateStudent(request, pk):
    student_data = Student.objects.get(roll=pk)
    form = UpdateStudent(instance=student_data)

    if request.method == 'POST':
        form = UpdateStudent(request.POST, instance=student_data)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("students",args=(pk,)))
            
    context = {'data':student_data, 'form':form}
    return render(request, 'fees/student_update.html', context)


def deleteStudent(request, pk):
    student_data = Student.objects.get(roll=pk)
    context = {'data': student_data}

    if request.method=='POST':
        student_data.delete()
        return HttpResponseRedirect('/')
    return render(request,'fees/delete_student.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def createSemester(request, pk):
    student_data = Student.objects.get(roll=pk)
    semester_tabs = student_data.semester_set.all()
    form = SemesterForm(initial={'roll':pk})
    # print('yes')
    if request.method == 'POST':
        # print(request.POST)
        form = SemesterForm(request.POST)
        if form.is_valid():
            form.save()

            #  for total and dues -------------
            try:
                sem_fee = int(form.cleaned_data.get('tution_fee')) + int(form.cleaned_data.get('hostel_fee'))
                due = int(form.cleaned_data.get('tution_fee')) + int(form.cleaned_data.get('hostel_fee'))
                sem = student_data.semester_set.get(semestertype=form.cleaned_data.get('semestertype'))
                sem.total_payment = sem_fee
                sem.dues = due -  int(form.cleaned_data.get('total_paid'))
                sem.save()
            except:
                pass
            #  -----------------------------------------------------------

            # return render(request, 'fees/students.html', context)
            return HttpResponseRedirect(reverse("students",args=(pk,)))

    context = {'form':form}
    return render(request, 'fees/semester_tab_form.html',context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def updateSemester(request, pk):
    semester_tab = Semester.objects.get(id=pk)
    form = SemesterForm(instance = semester_tab)
    if request.method == 'POST':
        form = SemesterForm(request.POST, instance=semester_tab)
        if form.is_valid:
            form.save()

            #  for total and dues -------------
            try:
                sem_fee = int(form.cleaned_data.get('tution_fee')) + int(form.cleaned_data.get('hostel_fee')) +int(form.cleaned_data.get('mon_1_amount')) +int(form.cleaned_data.get('mon_2_amount')) +int(form.cleaned_data.get('mon_3_amount')) +int(form.cleaned_data.get('mon_4_amount')) +int(form.cleaned_data.get('mon_5_amount')) +int(form.cleaned_data.get('mon_6_amount'))
                
                sem = Semester.objects.get(id=pk)
                sem.total_payment = sem_fee
                sem.dues = sem_fee -  int(form.cleaned_data.get('total_paid')) 
                sem.save()
            except:
                pass
            #  -----------------------------------------------------------
            # HttpResponseRedirect(reverse("students", args=(semester_tab.roll.roll,)))
            # return HttpResponseRedirect('/students/{}/'.format(semester_tab.roll.roll))
            return HttpResponseRedirect('/students/{}/'.format(semester_tab.roll))
    context = {'form':form}
    return render(request, 'fees/semester_tab_form.html',context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def deleteSemester(request, pk):
    semester_tab = Semester.objects.get(id=pk)
    context = {'semester_tab':semester_tab}
    if request.method == 'POST':
        semester_tab.delete()

        # return HttpResponseRedirect(reverse("students",args=(semester_tab.roll.roll,)))
        return HttpResponseRedirect('/students/{}/'.format(semester_tab.roll.roll))
    # context = {'semester_tab':semester_tab}
    # print(semester_tab.roll.roll)
    
    return render(request, 'fees/semester_tab_delete.html', context)




@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def student_each_sem(request, pk):
    current_sem = Semester.objects.get(id=pk)
    student_data = Student.objects.get(roll=current_sem.roll.roll)
    # print(student_data)

    context = {'current_sem':current_sem, 'student_data':student_data}
    return render(request, 'fees/student_each_sem.html', context)


# @unauthenticated_user
@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def registration(request):
    form = CreateStudentForm()
    # print(form.fields['username'].label)


    if request.method == 'POST':
        form = CreateStudentForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='student')
            user.groups.add(group)

            # print(user)

            Student.objects.create(
                user = user,
                roll = username,
                email = form.cleaned_data.get('email'),
                firstname = form.cleaned_data.get('firstname'),
                middlename = form.cleaned_data.get('middlename'),
                lastname = form.cleaned_data.get('lastname'),
                phone = form.cleaned_data.get('phone'),
                branch = form.cleaned_data.get('branch'),
                course = form.cleaned_data.get('course'),
                Year = form.cleaned_data.get('Year'),
                
            )

            messages.success(request, 'Student was successfully Registered ' + username)
            return HttpResponseRedirect('/registration/')
            

    context = {'form':form}
    return render(request, 'fees/registration.html', context)

@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(request.POST.get('checker'))
        #  wheteher the login one is student or admin
        checker = request.POST.get('checker')
        user = authenticate(request, username=username, password=password)
        # print(user)

        if user is not None:
            login(request, user)
            # print(request.user.groups.all()[0].name)
            if request.user.groups.all()[0].name == checker:
                # print(user)
                return redirect('home')
            else:
                logout(request)
                # messages.info(request, 'username or password is incorrect')
        else:
            messages.info(request, 'username or password is incorrect')
            
    context = {}
    return render(request, 'fees/index.html', context)


def logout_student(request):
    logout(request)
    context = {}
    return redirect('login')
# not done yet

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['student'])
def userpage(request):
    student_sems = request.user.student.semester_set.all()
    
    roll = request.user
    # print('yes')
    student_data = Student.objects.get(roll=roll)
    semester_tabs = student_data.semester_set.all()
    context = {'student_sems':student_sems, 'student_data':student_data, 'semester_tabs':semester_tabs}
    return render(request, 'fees/user.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['student'])
def user_student_each_sem(request, pk):
    current_sem = Semester.objects.get(id=pk)
    student_data = Student.objects.get(roll=current_sem.roll.roll)
    # print(student_data)
    # print(request.user)
    
    context = {'current_sem':current_sem, 'student_data':student_data}
    return render(request, 'fees/user_student_each_sem.html', context)




@login_required(login_url = 'login')
@allowed_users(allowed_roles=['student'])
def enquiry(request):
    
    student_data = Student.objects.get(roll=request.user)
    # print(student_data)

    form = StudentEnquiryForm(initial={'roll':request.user, 'email':student_data.email})
    if request.method == 'POST':
        form = StudentEnquiryForm(request.POST)
        if form.is_valid():
            
            # print(form.cleaned_data.get('Enquiry'))

            html_message = loader.render_to_string(
            'fees/enquiry_html_message.html',
            {
                'roll': form.cleaned_data.get('roll'),
                'name': form.cleaned_data.get('name'),
                'branch': form.cleaned_data.get('branch'),
                'email': form.cleaned_data.get('email'),
                'Enquiry': form.cleaned_data.get('Enquiry'),
            }
        )

            send_mail(
                    'Your Enquiry has been Submitted',
                    form.cleaned_data.get('Enquiry'),
                    'aspking.ash.aa@gmail.com',
                    [student_data.email],
                    fail_silently=False,
                    html_message=html_message,
                )
            send_mail(
                    'New Enquiry ',
                    form.cleaned_data.get('Enquiry'),
                    'aspking.ash.aa@gmail.com',
                    ['aspking.ash.aa@gmail.com'],
                    fail_silently=False,
                    html_message=html_message,
                )
            form.save()
            messages.success(request, ' Your Enquiry has been Submitted ')
            return HttpResponseRedirect('/enquiry/')

    context = {'form':form, 'student_data':student_data}
    return render(request, 'fees/enq.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def enquiry_admin(request):
    enquiries = EnquiryForm.objects.all().order_by('-id')

    myfilter = EnquiryFilter(request.GET, queryset=enquiries)
    if request.method == 'GET':
        enquiries = myfilter.qs

    # if len(enquiries)>50:
    #     enquiries = enquiries[:50]

    context = {'enquiries' : enquiries, 'myfilter':myfilter}
    return render(request, 'fees/enq_admin.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def enquiry_render(request, pk):
    # here taking from the database first
    particular_enq = EnquiryForm.objects.get(id=pk)
    form = StudentEnquiryFormUpdate(instance=particular_enq)

    student_data = Student.objects.get(roll=particular_enq.roll)
    semester_tabs = student_data.semester_set.all()

    roll = particular_enq.roll
    # roll = form.cleaned_data.get('roll')
    name = particular_enq.name
    branch = particular_enq.branch
    email = particular_enq.email
    Enquiry = particular_enq.Enquiry
    Enquiry_status = particular_enq.Enquiry_status

    if request.method == 'POST':
            form = StudentEnquiryFormUpdate(request.POST, instance=particular_enq)
         
            if form.is_valid():
                if Enquiry_status!=form.cleaned_data.get('Enquiry_status') and branch==form.cleaned_data.get('branch') and branch==form.cleaned_data.get('branch') and Enquiry==form.cleaned_data.get('Enquiry') and roll==form.cleaned_data.get('roll'):
                    form.save()
                    return HttpResponseRedirect('/enquiry_admin/')
                else:
                    return HttpResponseRedirect('/enquiry_admin/')


    context = {'particular_enq':particular_enq, 'form':form, 'student_data':student_data, 'semester_tabs':semester_tabs, 'roll':roll, 'name':name, 'email':email, 'branch':branch, 'Enquiry':Enquiry}
    return render(request, 'fees/part_enq.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def announcement(request):
    announcements = Announcement.objects.all().order_by('-id')

    myfilter = AnnouncementFilter(request.GET, queryset=announcements)
    if request.method == 'GET':
        announcements = myfilter.qs

    context = {'announcements' : announcements, 'myfilter':myfilter}
    return render(request, 'fees/announcement.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def announcement_create(request):
    form = AnnouncementForm()
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request, ' New Announcement formed ')
            return HttpResponseRedirect('/announcement_new/')

    context = {'form':form}
    return render(request, 'fees/create_announcement.html', context)



@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def open_announcement(request, pk):
    announcement = Announcement.objects.get(id=pk)
    form = AnnouncementForm(instance=announcement)

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        
        if form.is_valid:
            form.save()
            return HttpResponseRedirect('/announcement/')

    context = {'announcement':announcement, 'form':form}
    return render(request, 'fees/open_announcement.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['student'])
def student_announcement(request):
    student_data = Student.objects.get(roll=request.user)
    announcement_Urgent = Announcement.objects.filter(Show='Show').filter(Status='Urgent').order_by('-id')
    announcement_Normal = Announcement.objects.filter(Show='Show').filter(Status='Normal').order_by('-id')
    u_len=len(announcement_Urgent)
    n_len=len(announcement_Normal)

    no_new_announcement = None

    if u_len==n_len==0:
        no_new_announcement = ['No New Announcement']
    
    context = {'announcement_Urgent':announcement_Urgent, 'announcement_Normal':announcement_Normal, 'u_len':u_len, 'n_len':n_len, 'no_new_announcement':no_new_announcement, 'student_data':student_data}
    return render(request, 'fees/announcement_student.html', context)




#  trying for the uploading part
from .somewhere import handle_uploaded_file

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            return_message =  handle_uploaded_file(request.FILES['file'], form.cleaned_data.get('title'))
            # return HttpResponseRedirect('/success/url/')
            print(return_message)
            messages.success(request, return_message)
            return HttpResponseRedirect('/upload_file/')
            # messages.success(request, ' Your file has been uploaded successfully ')
    else:
        form = UploadFileForm()
    return render(request, 'fees/upload.html', {'form': form})


#  automating the creating semester
from .automate_create_semester import *

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def automate_semester(request):
    form = AutomateCreateSemester()

    if request.method == 'POST':
        form = AutomateCreateSemester(request.POST)
        if form.is_valid():

            if form.cleaned_data.get('monsoon_wintertype') == 'Monsoon':
    
                return_message = Monsoon(form)
                form.save()
                messages.success(request, return_message)
                return HttpResponseRedirect('/automate_create_sem/')
            else:
                return_message = Winter(form)
                form.save()
                messages.success(request, return_message)
                return HttpResponseRedirect('/automate_create_sem/')

        else:
            messages.success(request, 'Oops something went wrong')


    context = {'form':form}
    return render(request, 'fees/automate_semester.html', context)


#  for the autation for the fees
from .automate_fees import *

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def automate_fee(request):

    form = UploadFeesFileForm()

    if request.method == 'POST':
        form = UploadFeesFileForm(request.POST, request.FILES)

        if form.is_valid():
            return_message = update_fees(request.FILES['file'], form.cleaned_data.get('month'))

            messages.success(request, return_message)
            return HttpResponseRedirect('/automate_fees/')
            
        else:
            messages.success(request, 'ops something went wrong')
            return HttpResponseRedirect('/automate_fees/')

    context = {'form':form}
    return render(request, 'fees/automate_fees.html', context)


#  registered student details
@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def registered_details(request):
    all_files = RegisterFile.objects.all().order_by('-datecreated')
    btech = Student.objects.filter(course='B_Tech').count()
    mtech = Student.objects.filter(course='M_Tech').count()
    phd = Student.objects.filter(course='Phd').count()

    myfilter = RegisteredDetails(request.GET, queryset=all_files)
    if request.method == 'GET':
        all_files = myfilter.qs



    context = {'all_files':all_files, 'btech':btech, 'mtech':mtech, 'phd':phd, 'myfilter':myfilter}

    return render(request, 'fees/registered_details.html', context)


# returning the uploaded file
import pandas as pd
import csv
@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def return_uploaded_registered(request,pk):
    one_file = RegisterFile.objects.get(id=pk)

    df = pd.read_csv(one_file.uploaded_file)

    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(one_file.title)
    # Create the CSV writer using the HttpResponse as the "file"
    writer = csv.writer(response)
    writer.writerow(df.columns)

    for x in range(df.shape[0]):
        writer.writerow(df.loc[x])
    return response


#  for giving the password file
@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def get_password(request, pk):
    one_file = RegisterFile.objects.get(id=pk)
    Roll = (one_file.roll_no).split(' ')
    Email = (one_file.email).split(' ')
    Password = (one_file.password).split(' ')
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=password.csv'
    # Create the CSV writer using the HttpResponse as the "file"    
    writer = csv.writer(response)
    writer.writerow(['index', 'Username', 'Email', 'Password'])
    i = 0
    for (roll, email, password) in zip(Roll, Email, Password):
        writer.writerow([i, roll, email, password])
        i+=1
    return response


#  for sending mail to the registered students
@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def send_register_mail(request,pk):
    one_file = RegisterFile.objects.get(id=pk)
    Roll = (one_file.roll_no).split(' ')
    Email = (one_file.email).split(' ')
    Password = (one_file.password).split(' ')

    for (roll, email, password) in zip(Roll, Email, Password):
        # print(email)
        html_message = loader.render_to_string(
            'fees/register_student_email.html',
            {
                'Username': '{} Same as Your Roll No of your Institute'.format(roll),
                'email': email,
                'Password': password,
                'Messages' : ['Your Credentials for the login', ' You must change the password after login or before login', 'for any fees related details use this website', 'for any query mail us']

            }
        )

        send_mail(
            'Your Credentials for College Fees Website',
            'no',
            'aspking.ash.aa@gmail.com',
            [email],
            fail_silently=False,
            html_message=html_message,
        )
    # change the status of the sent_email
    one_file.email_sent = 'YES'
    one_file.save()
    # print('save the file')

    return HttpResponseRedirect("/registration_details/")
    

#  file format for the upload
@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def format(request, pk):
    if pk == '1':
        index = [0, 1, 2, 3]
        username = ['3199099', '3199097', '3199087', '3199085']
        firstname = ['Gurnoor', 'Badal', 'Name_', 'not_name']
        password1 = ['iiitgQ!1', 'iiitgQ!1', 'iiitgQ!1', 'iiitgQ!1']
        middlename = ['','', '','']
        lastname = ['','', '','']
        email = ['aspking.ash.aa@gmail.com', 'ayushashmit777@gmail.com', 'ashmit.ayush@iiitg.ac.in', 'cancrushon@gmail.com']
        phone = ['7070772225', '7070772273','7070772525', '7570772273']
        branch = ['CSE', 'ECE', 'CSE', 'ECE']
        course = ['B_Tech','M_Tech','Phd', 'M_Tech']
        Year = ['2018', '2019','2018', '2019']


        response = HttpResponse('text/csv')
        response['Content-Disposition'] = 'attachment; filename=registration_format.csv'
        # Create the CSV writer using the HttpResponse as the "file"    
        writer = csv.writer(response)
        writer.writerow(['index','username', 'firstname', 'password1','middlename', 'lastname', 'email','phone', 'branch', 'course','Year'])
        for (index_, username_, firstname_, password1_,middlename_, lastname_, email_,phone_, branch_, course_,Year_) in zip(index, username, firstname, password1,middlename, lastname, email,phone, branch, course,Year):
            writer.writerow([index_, username_, firstname_, password1_,middlename_, lastname_, email_,phone_, branch_, course_,Year_])
        return response
    elif pk == '2':

        username = ['1801032', '1801012']
        semestertype = ['third', 'third']
        amount = [4399, 3999]
        response = HttpResponse('text/csv')
        response['Content-Disposition'] = 'attachment; filename=mess.csv'
        # Create the CSV writer using the HttpResponse as the "file"    
        writer = csv.writer(response)
        writer.writerow(['index', 'username', 'semestertype', 'amount'])
        i = 0
        for (username_, semestertype_, amount_) in zip(username, semestertype, amount):
            writer.writerow([i, username_, semestertype_, amount_])
            i+=1
        return response
    else:
        HttpResponse('OOPS! Something went wrong')



#  change password
@login_required(login_url = 'login')
@allowed_users(allowed_roles=['student'])
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/changePassword/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    student_data = Student.objects.get(roll=request.user)
    context = {'form':form, 'student_data':student_data}
    return render(request, 'fees/change_password.html', context)


# change password admin
@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def changePasswordAdmin(request, pk):
    student_data = Student.objects.get(roll=pk)
    user = User.objects.get(username=pk)
    if request.method == 'POST':
        form = ChangePasswordAdmin(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data.get('New_Password')
            password2 = form.cleaned_data.get('Confirm_Password')

            if password1 == password2:
                user.set_password(password1)
                user.save()
                messages.success(request, 'password was successfully updated!')
                return HttpResponseRedirect('/changePasswordAdmin/{}/'.format(student_data.roll))
            else:
                messages.error(request, 'password does not match')
                return HttpResponseRedirect('/changePasswordAdmin/{}/'.format(student_data.roll))

        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ChangePasswordAdmin()

    context = {'form':form, 'student_data':student_data}
    return render(request, 'fees/change_password_admin.html', context)