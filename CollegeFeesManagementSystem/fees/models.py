from django.db import models
from django.contrib.auth.models import User
# Create your models here.

BranchType = [
    ('CSE','CSE'),
    ('ECE','ECE'),
]
CourseType = [
    ('B_Tech','B_Tech'),
    ('M_Tech','M_Tech'),
    ('Phd','Phd'),
]
date = [str(x) for x in range(2013,2050)]
# date=' '.join(date)
YearType = []
for x in date:
    YearType.append((x,x))

MonthType = [ ('Jan','Jan'), ('Feb','Feb'), ('Mar','Mar'), ('Apr','Apr'), ('May','May'), ('Jun','Jun'), ('Jul','Jul'), ('Aug','Aug'), ('Sept','Sept'), ('Oct','Oct'), ('Nov','Nov'), ('Dec','Dec'),]
class Student(models.Model):

    BranchType = models.TextChoices('BranchType', 'CSE ECE')
    
    date = [str(x) for x in range(2013,2050)]
    date=' '.join(date)
    YearType = models.TextChoices('YearType', date)

    CourseType = models.TextChoices('CourseType', 'B_Tech M_Tech Phd')

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    roll = models.CharField('Roll_No', max_length=7, primary_key=True, blank=False)
    firstname = models.CharField('First_Name', max_length=250, blank=False)
    middlename = models.CharField('Middle_Name', max_length=250, null=True, blank=True)
    lastname = models.CharField('Last_Name', max_length=250, null=True, blank=True)
    email = models.EmailField('Email', max_length=250, blank=False)
    phone = models.CharField('Phone', max_length=15, blank=False)
    branch = models.CharField('Branch', max_length=3, blank=False, choices=BranchType.choices)
    Year = models.CharField('Year', max_length=4, blank=False, choices=YearType.choices)
    course = models.CharField('Course', max_length=7, blank=False, choices=CourseType.choices)
    datecreated = models.DateTimeField(auto_now_add=True, null=True)

    
    template = '{} {}'
    def __str__(self):
        return self.roll
        return self.template.format(self.roll,self.firstname)



class Semester(models.Model):

    date = [str(x) for x in range(2013,2050)]
    date=' '.join(date)

    SemesterType = models.TextChoices('SemesterType', 'first second third fourth fifth sixth seventh eighth')
    Monsoon_WinterType = models.TextChoices('Monsoon_WinterType', 'Monsoon Winter')
    PaidType = models.TextChoices('PaidType', 'NotPaid Paid')
    YearType = models.TextChoices('YearType', date)
    MonthType = models.TextChoices('MonthType', 'Jan Feb Mar Apr May Jun Jul Aug Sept Oct Nov Dec')

    roll = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False) 
    semestertype = models.CharField('Semester_type', max_length=50, blank=False, choices=SemesterType.choices)
    monsoon_wintertype = models.CharField('Monsoon_or_Winter', max_length=50, blank=False, choices=Monsoon_WinterType.choices)
    Year = models.CharField('Year', max_length=50, blank=False, choices=YearType.choices)
    datecreated = models.DateTimeField(auto_now_add=True, null=True)


    # Tution Fee
    tution_fee = models.CharField('Tution_Fee', max_length=50, null=True, blank=True, default='0')
    # tution_fee_status = models.CharField('Tution_Fee_status', max_length=50, null=True, choices=PaidType.choices, blank=True, default=PaidType.NotPaid)


    # Hostel Fee
    hostel_fee = models.CharField('Hostel_Fee', max_length=50, null=True, blank=True, default='0')
    # hostel_fee_status = models.CharField('Hostel_Fee_status', max_length=50, null=True, choices=PaidType.choices, blank=True, default=PaidType.NotPaid)
    

    #  mess section
        
    mon_1 = models.CharField('Mon_1', max_length=50, null=True, choices=MonthType.choices, blank=True)
    mon_1_amount = models.CharField('Mon_1_amount', max_length=50, null=True, blank=True, default='0')
    # mon_1_status = models.CharField('Mon_1_status', max_length=50, null=True, choices=PaidType.choices, blank=True, default=PaidType.NotPaid)

    mon_2 = models.CharField('Mon_2', max_length=50, null=True, choices=MonthType.choices, blank=True)
    mon_2_amount = models.CharField('Mon_2_amount', max_length=50, null=True, blank=True, default='0')
    # mon_2_status = models.CharField('Mon_2_status', max_length=50, null=True, choices=PaidType.choices, blank=True, default=PaidType.NotPaid)

    mon_3 = models.CharField('Mon_3', max_length=50, null=True, choices=MonthType.choices, blank=True)
    mon_3_amount = models.CharField('Mon_3_amount', max_length=50, null=True, blank=True, default='0')
    # mon_3_status = models.CharField('Mon_3_status', max_length=50, null=True, choices=PaidType.choices, blank=True, default=PaidType.NotPaid)

    mon_4 = models.CharField('Mon_4', max_length=50, null=True, choices=MonthType.choices, blank=True)
    mon_4_amount = models.CharField('Mon_4_amount', max_length=50, null=True, blank=True, default='0')
    # mon_4_status = models.CharField('Mon_4_status', max_length=50, null=True, choices=PaidType.choices, blank=True, default=PaidType.NotPaid)

    mon_5 = models.CharField('Mon_5', max_length=50, null=True, choices=MonthType.choices, blank=True)
    mon_5_amount = models.CharField('Mon_5_amount', max_length=50, null=True, blank=True, default='0')
    # mon_5_status = models.CharField('Mon_5_status', max_length=50, null=True, choices=PaidType.choices, blank=True, default=PaidType.NotPaid)

    mon_6 = models.CharField('Mon_6', max_length=50, null=True, choices=MonthType.choices, blank=True)
    mon_6_amount = models.CharField('Mon_6_amount', max_length=50, null=True, blank=True, default='0')
    # mon_6_status = models.CharField('Mon_6_status', max_length=50, null=True, choices=PaidType.choices, blank=True, default=PaidType.NotPaid)

    
    # Extra charges
    extra_charges = models.TextField("Extra Charges", null=True, blank=True, default='None')
    extra_charges_amount = models.CharField('Extra Charge Amount', max_length=50, default = '0', blank=True)
    # extra_charges_status = models.CharField('Extra_Fee_status', max_length=50, null=True, choices=PaidType.choices, blank=True, default=PaidType.NotPaid)


    # for the total payment and dues
    total_payment = models.CharField('Total Payment', max_length=50, null=True, blank=True, default='0')
    total_paid = models.CharField('Total paid',max_length=50, null=True, blank=True, default='0')
    dues = models.CharField('Dues', max_length=50, null=True, blank=True, default='0')

    template = '{} {} {} {}'
    def __str__(self):
        return self.template.format(self.roll, self.semestertype, self.monsoon_wintertype, self.Year)
    


class EnquiryForm(models.Model):

    BranchType = models.TextChoices('BranchType', 'CSE ECE')
    EnquiryStatus = models.TextChoices('EnquiryStatus', 'No Yes')

    roll = models.CharField('Roll_No', max_length=7, blank=False)
    name = models.CharField('Name', max_length=250, blank=False)
    email = models.EmailField('Email', max_length=250, blank=False)
    branch = models.CharField('Branch', max_length=3, blank=False, choices=BranchType.choices)
    
    Enquiry = models.TextField("Enquiry", blank=False)
    Enquiry_status = models.CharField('Enquiry_status', max_length=3, null=True, choices=EnquiryStatus.choices, blank=True, default=EnquiryStatus.No)
    datecreated = models.DateTimeField(auto_now_add=True, null=True)

    
    template = '{} {} {}'
    def __str__(self):
        # return self.roll, self.firstname
        return self.template.format(self.roll,self.name,self.email)

class Announcement(models.Model):

    Ann_Status = models.TextChoices('Ann_Status', 'Normal Urgent')
    Show_Status = models.TextChoices('Show_Status', 'Show Remove')
    
    Subject = models.CharField('Subject', max_length=250, blank=False)
    Query = models.TextField('Query', blank=False)
    Status = models.CharField('Status', max_length=10, blank=False, choices=Ann_Status.choices, default='Normal')
    Show = models.CharField('Show', max_length=7, blank=False, choices=Show_Status.choices, default='Show')
    datecreated = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.Subject
    


class Automate_Create_Semester(models.Model):
    date = [str(x) for x in range(2017,2050)]
    date=' '.join(date)

    SemesterType = models.TextChoices('SemesterType', 'first second third fourth fifth sixth seventh eighth')
    Monsoon_WinterType = models.TextChoices('Monsoon_WinterType', 'Monsoon Winter')
    YearType = models.TextChoices('YearType', date)
    BranchType = models.TextChoices('BranchType', 'CSE ECE')
    CourseType = models.TextChoices('CourseType', 'B_Tech M_Tech Phd')

    semestertype = models.CharField('Semester_type', max_length=50, blank=False, choices=SemesterType.choices)
    monsoon_wintertype = models.CharField('Monsoon_or_Winter', max_length=50, blank=False, choices=Monsoon_WinterType.choices)
    Year = models.CharField('College Joining Year', max_length=50, blank=False, choices=YearType.choices)
    branch = models.CharField('Branch', max_length=3, blank=False, choices=BranchType.choices)
    course = models.CharField('Course', max_length=7, blank=False, choices=CourseType.choices)
    tution_fee = models.CharField('Tution_Fee', max_length=50, null=True, blank=True, default='0')
    hostel_fee = models.CharField('Hostel_Fee', max_length=50, null=True, blank=True, default='0')
    datecreated = models.DateTimeField(auto_now_add=True, null=True)

    template = '{} {} {}'
    def __str__(self):
        return self.template.format(self.Year,self.branch,self.course)
    

# saving registered files
class RegisterFile(models.Model):

    Email_Status = models.TextChoices('Email_Status', 'NO YES')

    title = models.CharField('Title', max_length=150, blank=False)
    uploaded_file = models.FileField('Uploaded File', upload_to='uploads/')
    password = models.TextField('Password', blank=False)
    roll_no = models.TextField('Roll_No', blank=False)
    email = models.TextField('email', blank=False)

    #  fo the satatus whether the email have been send or not
    email_sent = models.CharField('Show', max_length=3, null=True, choices=Email_Status.choices, default='NO')
    datecreated = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

