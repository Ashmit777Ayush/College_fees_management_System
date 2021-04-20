import pandas as pd
import numpy as np

username = ['1801032', '1801012', '1801033', '1801132', '1801112',  '1801133']
semestertype = ['first', 'first','first', 'first','first', 'first']
amount = [4399, 3999,4399, 3999,4399, 3999]

dicti = {
    'username':username,
    'semestertype':semestertype,
    'amount':amount,
}


df = pd.DataFrame(dicti)
df.to_csv('first_fees.csv')