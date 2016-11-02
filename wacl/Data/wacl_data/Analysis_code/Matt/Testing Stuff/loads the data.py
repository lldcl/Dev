import pandas as pd
from time import strftime


date = raw_input('\n\nOkie doke, what date would you like to load data from?\nInput date in format mmdd: ')
try:
    pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Raw_data_files\\2015'+date[0:2]
    filenameL ='\d20' + str((strftime('%y'))) + date + '_0' + raw_input('\n\nWhich file would you like to load? ')
    dataL = pd.read_csv(pathL+filenameL)
    
except IOError:
    pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\2015'+date[0:2]
    dataL = pd.read_csv(pathL+filenameL)


