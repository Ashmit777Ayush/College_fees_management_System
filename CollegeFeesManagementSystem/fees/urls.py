from django.urls import path

from . import views

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('students/<str:pk>/', views.student, name='students'),
    path('update_student/<str:pk>/', views.updateStudent, name='updateStudent'),
    path('deleteStudent/<str:pk>/', views.deleteStudent, name='deleteStudent'),
    path('createSemester/<str:pk>/', views.createSemester, name='createSemester'),
    path('updateSemester/<str:pk>/', views.updateSemester, name='updateSemester'),
    path('deleteSemester/<str:pk>/', views.deleteSemester, name='deleteSemester'),
    path('student_each_sem/<str:pk>/', views.student_each_sem, name='student_each_sem'),
    path('registration/', views.registration, name='registration'),
    # 
    path('login/', views.loginpage, name='login'),
    path('user_student_each_sem/<str:pk>/', views.user_student_each_sem, name='user_student_each_sem'),
    path('user/', views.userpage, name='userpage'),
    path('logout/', views.logout_student, name='Logout'),
    path('changePassword/', views.changePassword, name='changePassword'),
    path('changePasswordAdmin/<str:pk>/', views.changePasswordAdmin, name='changePasswordAdmin'),


    path('enquiry/', views.enquiry, name='enquiry'),
    path('enquiry_admin/', views.enquiry_admin, name='enquiry_admin'),
    path('enquiry_render/<str:pk>/', views.enquiry_render, name='enquiry_render'),

    path('announcement/', views.announcement,name='announcement'),
    path('announcement_new/', views.announcement_create,name='announcement_create'),
    path('open_announcement/<str:pk>/', views.open_announcement, name='open_announcement'),
    path('announcement_student/', views.student_announcement, name='student_announcement'),

    path('upload_file/', views.upload_file, name='upload_file'),

    # password reset
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='fees/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='fees/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='fees/password_reset_page.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='fees/password_reset_complete.html'), name='password_reset_complete'),

    #  automate create semester
    path('automate_create_sem/', views.automate_semester, name='automate_semester'),

    #  automate the fees department
    path('automate_fees/', views.automate_fee, name='automate_fees'),

    # details of registration of uploaded file
    path('registration_details/', views.registered_details, name='registered_details'),
    path('return_uploaded_registered/<str:pk>/', views.return_uploaded_registered, name='return_uploaded_registered'),
    path('get_password/<str:pk>/', views.get_password, name='get_password'),
    path('send_register_mail/<str:pk>/', views.send_register_mail, name='send_register_mail'),

    # format
    path('format/<str:pk>', views.format, name='format'),
]