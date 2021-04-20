import pandas as pd
import numpy as np

username = ['1801032', '1801012', '1801000', '1801001','1801033', '1801013', '1801003', '1801014','1801132', '1801112', '1801100', '1801101','1801133', '1801113', '1801103', '1801114']
firstname = ['Ashmit', 'Akash', 'Ayush', 'Golu','Ashmit', 'Akash', 'Ayush', 'Golu','Ashmit', 'Akash', 'Ayush', 'Golu','Ashmit', 'Akash', 'Ayush', 'Golu']
password1 = ['iiitgQ!1', 'iiitgQ!1', 'iiitgQ!1', 'iiitgQ!1','iiitgQ!1', 'iiitgQ!1', 'iiitgQ!1', 'iiitgQ!1','iiitgQ!1', 'iiitgQ!1', 'iiitgQ!1', 'iiitgQ!1','iiitgQ!1', 'iiitgQ!1', 'iiitgQ!1', 'iiitgQ!1']
password2 = ['iiitgQ!1', 'iiitgQ!1', 'iiitgQ!1', 'iiitgQ!1','iiitgQ!1', 'iiitgQ!1', 'iiitgQ!1', 'iiitgQ!1','iiitgQ!1', 'iiitgQ!1', 'iiitgQ!1', 'iiitgQ!1','iiitgQ!1', 'iiitgQ!1', 'iiitgQ!1', 'iiitgQ!1']
middlename = ['','', '','','','', '','','','', '','','','', '','']
lastname = ['','', '','','','', '','','','', '','','','', '','']
email = ['ashmit.ayush@iiitg.ac.in', 'cancrushon@gmail.com', 'ayushashmit777@gmail.com', 'cancrushon@gmail.com','ashmit.ayush@iiitg.ac.in', 'cancrushon@gmail.com', 'ayushashmit777@gmail.com', 'cancrushon@gmail.com','ashmit.ayush@iiitg.ac.in', 'cancrushon@gmail.com', 'ayushashmit777@gmail.com', 'cancrushon@gmail.com','ashmit.ayush@iiitg.ac.in', 'cancrushon@gmail.com', 'ayushashmit777@gmail.com', 'cancrushon@gmail.com']
phone = ['7070772225', '7070772273','7070772525', '7570772273','7070772225', '7070772273','7070772525', '7570772273','7070772225', '7070772273','7070772525', '7570772273','7070772225', '7070772273','7070772525', '7570772273']
branch = ['CSE', 'CSE', 'CSE', 'ECE','CSE', 'ECE', 'CSE', 'ECE','CSE', 'CSE', 'CSE', 'ECE','CSE', 'ECE', 'CSE', 'ECE']
course = ['B_Tech','B_Tech','Phd', 'M_Tech','B_Tech','B_Tech','Phd', 'M_Tech','B_Tech','B_Tech','Phd', 'M_Tech','B_Tech','B_Tech','Phd', 'M_Tech']
Year = ['2018', '2018','2019', '2019','2018', '2018','2019', '2019','2018', '2018','2019', '2019','2018', '2018','2019', '2019']

dicti = {
    'username':username,
    'firstname':firstname,
    'password1':password1,
    'password2':password2,
    'middlename':middlename,
    'lastname':lastname,
    'email':email,
    'phone':phone,
    'branch':branch,
    'course':course,
    'Year':Year,
}


df = pd.DataFrame(dicti)
# df.drop('Unnamed: 0',inplace=True,axis=1)
df.to_csv('first.csv')