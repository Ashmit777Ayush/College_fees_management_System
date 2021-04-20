from datetime import datetime
import pandas as pd
import numpy as np


from .models import *
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

import datetime


def handle_uploaded_file(f, title):
                # try:
                # print('uploaded successfully')
                df = pd.read_csv(f)
                # print(f)
                # print(df.shape)
                try:
                        # print(df.columns)
                        df.drop('Unnamed: 0',inplace=True,axis=1)
                except:
                        df.drop('text/csvindex',inplace=True,axis=1)

                try:
                        # checking null values
                        for x in ['username', 'firstname', 'password1', 'email', 'phone', 'branch', 'course', 'Year']:
                                total_null = df[x].isnull().sum()
                                # print(total_null)
                                if total_null>0:
                                        return 'null value in column    ' + ' ' + x
                except:
                        return 'error in file format'

                # now checking repeat ones in usernsame
                # if getting error in in this section have to check both in the Student and the user database
                try:
                        for x in df['username']:
                                try:
                                        if Student.objects.get(roll=x) or user.objects.get(username=x):
                                                # print(True)
                                                return '{} same username have been registred already '.format(x)
                                except:
                                        pass
                except:
                        return 'Something went wrong in file format'

                # length of username must be the 7
                try:
                        for x in df['username']:
                                if len(str(x))!=7:
                                        # print(True)
                                        return '{} have error in roll number '.format(x)
                except:
                        return 'something went wrong in file format'

                #  now registering the students
                try:
                        Roll_No = []
                        Email_Id = []
                        Password = []
                        for x in range(df.shape[0]):
                                # for y in df.columns:
                                        # print(df.at[x,y])
                                
                                username = df.at[x,'username']
                                user = User.objects.create_user(username, df.at[x, 'email'], df.at[x, 'password1'])
                                group = Group.objects.get(name='student')
                                user.groups.add(group)

                                Student.objects.create(
                                        user = user,
                                        roll = username,
                                        email = df.at[x, 'email'],
                                        firstname = df.at[x, 'firstname'],
                                        middlename = df.at[x, 'middlename'],
                                        lastname = df.at[x, 'lastname'],
                                        phone = df.at[x, 'phone'],
                                        branch = df.at[x, 'branch'],
                                        course = df.at[x, 'course'],
                                        Year = df.at[x, 'Year'],
                                )
                                Email_Id.append(df.at[x, 'email'])
                                Password.append(df.at[x, 'password1'])
                                Roll_No.append(username)
                                # print('Successfully registered all the student {}'.format(x))
                except:
                        return 'something went wrong plesse try to upload the file again after verification'

                try:
                        #  for the saving of the uploaded file
                        RegisterFile.objects.create(
                        title = title,
                        uploaded_file = f,
                        password = ' '.join(map(str,Password)),
                        roll_no = ' '.join(map(str,Roll_No)),
                        email = ' '.join(map(str, Email_Id)),
                        email_sent = 'NO',
                        )
                        return 'Successfully registered all the students'
                except:
                        'error in the format or something else'