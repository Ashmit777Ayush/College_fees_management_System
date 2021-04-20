from .models import *
import datetime



#  for the monsoon semester type
def Monsoon(form):
    months=['Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    
    try:    
        selected_student = Student.objects.filter(Year=form.cleaned_data.get('Year'), branch=form.cleaned_data.get('branch'), course=form.cleaned_data.get('course'))
        for student in selected_student:
            # print(student.roll)
            Semester.objects.create(
                roll = student,
                semestertype = form.cleaned_data.get('semestertype'),
                monsoon_wintertype = form.cleaned_data.get('monsoon_wintertype'),
                Year = datetime.datetime.now().year,
                tution_fee = form.cleaned_data.get('tution_fee'),
                hostel_fee = form.cleaned_data.get('hostel_fee'),
                mon_1 = months[0],
                mon_2 = months[1],
                mon_3 = months[2],
                mon_4 = months[3],
                mon_5 = months[4],
                mon_6 = months[5],
                total_payment = int(form.cleaned_data.get('tution_fee')) + int(form.cleaned_data.get('hostel_fee')),
                dues = int(form.cleaned_data.get('tution_fee')) + int(form.cleaned_data.get('hostel_fee')),
            )
        return 'semester added successfully'

    except:
        return 'Something went wrong'

#  for the winter semester type
def Winter(form):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']

    try:   
        selected_student = Student.objects.filter(Year=form.cleaned_data.get('Year'), branch=form.cleaned_data.get('branch'), course=form.cleaned_data.get('course'))
        for student in selected_student:
            # print(student.roll)
            Semester.objects.create(
                roll = student,
                semestertype = form.cleaned_data.get('semestertype'),
                monsoon_wintertype = form.cleaned_data.get('monsoon_wintertype'),
                Year = datetime.datetime.now().year,
                tution_fee = form.cleaned_data.get('tution_fee'),
                hostel_fee = form.cleaned_data.get('hostel_fee'),
                mon_1 = months[0],
                mon_2 = months[1],
                mon_3 = months[2],
                mon_4 = months[3],
                mon_5 = months[4],
                mon_6 = months[5],
                total_payment = int(form.cleaned_data.get('tution_fee')) + int(form.cleaned_data.get('hostel_fee')),
                dues = int(form.cleaned_data.get('tution_fee')) + int(form.cleaned_data.get('hostel_fee')),
            )
        return 'semester added successfully'

    except:
        return 'something went wrong'