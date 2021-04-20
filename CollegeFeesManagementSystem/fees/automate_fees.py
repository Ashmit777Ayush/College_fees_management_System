import pandas as pd
import numpy as np

from .models import *

def update_fees(f, month):
    try:
        print('uploaded successfully')

        df = pd.read_csv(f)
        try:
            df.drop('Unnamed: 0', inplace=True, axis=1)
        except:
            df.drop('text/csvindex', inplace=True, axis=1)


        try:
            for x in ['username', 'semestertype', 'amount']:
                total_null = df[x].isnull().sum()
                # print(total_null)
                if total_null>0:
                    return 'missing value in column    ' + ' ' + x
        except:
            return 'error in the file format'

        
        try:
            for x in df['username']:
                if len(str(x))!=7:
                    return 'error in username {}'.format(x)
        except:
            return 'error in file format in username column'

        try:
            for x in df['semestertype']:
                if (x in ['first', 'third', 'fifth',  'seventh']) and (month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']):
                    return 'error in month and semestertype, check smestertype and month'
        except:
            return 'error in file format'


        try:
            for x in df['semestertype']:
                if (x in ['second', 'fourth', 'sixth',  'eighth']) and (month in ['Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']):
                    return 'error in month and semestertype, check smestertype and month'
        except:
            return 'error in file format'    
        
        try:

            # print(df.shape)

            for x in range(df.shape[0]):
                student_data = Student.objects.get(roll=df.at[x, 'username'])
                # print(student_data.roll)

                sem = student_data.semester_set.get(semestertype=df.at[x, 'semestertype'])
                # print(sem)

                
                #  a/c to month i.e y we are calculating manupulating the data of the database
                y=month
                # print(sem.mon_1_amount)
                if y=='Jan' or y=='Jul':
                    sem.mon_1_amount = df.at[x, 'amount']
                elif y=='Feb' or y=='Aug':
                    sem.mon_2_amount = df.at[x, 'amount']
                elif y=='Mar' or y=='Sept':
                    sem.mon_3_amount = df.at[x, 'amount']
                elif y=='Apr' or y=='Oct':
                    sem.mon_4_amount = df.at[x, 'amount']
                elif y=='May' or y=='Nov':
                    sem.mon_5_amount = df.at[x, 'amount']
                else:
                    sem.mon_6_amount = df.at[x, 'amount']

                sem.save()

                # ---------------------------------------------
                # for the total and dues------
                sem = student_data.semester_set.get(semestertype=df.at[x, 'semestertype'])

                sem.total_payment = int(sem.tution_fee) + int(sem.hostel_fee) + int(sem.mon_1_amount) + int(sem.mon_2_amount) + int(sem.mon_3_amount) + int(sem.mon_4_amount) + int(sem.mon_5_amount) + int(sem.mon_6_amount)
                sem.save()
                sem = student_data.semester_set.get(semestertype=df.at[x, 'semestertype'])
                tp = int(sem.total_payment)
                paid = int(sem.total_paid)
                sem.dues = tp - paid
                sem.save()
                # print(sem.mon_1_amount)
                # -----------------------------------------------------------------
            return 'updated successfully'
        except:
            return 'problem in the student {}'.format(student_data.roll)


    except:
        return 'either format of csv is wrong or semester have not been created'   
        