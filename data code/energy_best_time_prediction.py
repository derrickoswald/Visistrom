#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 08:51:36 2019

@author: cuozzo
"""

from numpy import array, zeros # import module to work with arrays / matrices
from datetime import datetime, date # import module to deal with dates, time, etc.
from pandas import read_csv # import module to load excel data
import matplotlib.pyplot as plt # import module to make graphs
from pylab import imshow

dico_weekday = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}

data = read_csv('Solarenergie-6.csv')#,na_values="*)") # load excel file
matrixdata = data.as_matrix() # convert data into a matrix

Datum = array(matrixdata[0:len(matrixdata),0:1])[list(range(len(matrixdata))),[0]*len(matrixdata)] # devCode is the list of devices' names =>  to correct the really annoying format of the original array loaded by the matlab file... => we move from array([array([0]),array([1])...]) to array([0,1]), which is way more suitable for the next parts !       

Dates = [] # empty list
for day in Datum[1:]: # loop for each line/row of the file
    Dates.append(str(day).split(' ')[0]) # saving the date
Dates = list(zip(*[iter(Dates)]*Ntmp)) # changing the list into a list of sub-lists => each sublist corresponds to one day timepoints (96 x 15 minutes)
Dates = [sorted(list(set(dates)))[0] for dates in Dates] # we want each date only onc

select_days = []

D = 0
start = False
for i in range(len(Dates)):
    split = Dates[i].split('.') # splits the day string into a list separating the day, month and year
    dateofday = date(int(split[2]),int(split[1]),int(split[0])) # uses the datetime module to give the exact date in a usable format
    weekday = dateofday.weekday() # uses the datetime module: gives the week of the day for the given date in the form of an integer (0=monday, 1=tuesday, 2=wednesday, 3=thursday, 4=friday, 5=saturday, 6=sunday)
    day = dico_weekday[weekday] # day of the week in string (monday, tuesday, wednesday, thursday, friday, saturday, sunday)
    if day == 'Monday':
        start = True
    if start == True:
        select_days.append([Dates[i],day])
        D += 1
    if D == 7:
        start = False
        break
    
    

table = zeros((7,24))
start = select_days[0][0]

end = select_days[-1][0]

go = False
count = 0
mean = 0
hour = -1
day_index = 0
for line in matrixdata:
    if line[0] == start:
        go = True
    
    if go == True:
        hour += 0.25
        if int(hour)!=float(hour):
            mean += sum(line[6:])
        else:
            mean /= 4
            table[day_index,int(hour)] = mean
            mean = 0
            if hour == 23:
                day_index += 1
                hour = -1          
        
    if line[0] == end:
        count += 1
    if count == 96:
        go = False

#pcolor(table, edgecolors='k', linewidths=4)
#plt.show()
#imshow(table[8:18,:])
imshow(table[:,8:18])

"""
select_days
Out[56]: 
[['21.01.2019', 'Monday'],
 ['22.01.2019', 'Tuesday'],
 ['23.01.2019', 'Wednesday'],
 ['24.01.2019', 'Thursday'],
 ['25.01.2019', 'Friday'],
 ['26.01.2019', 'Saturday'],
 ['27.01.2019', 'Sunday']]
"""

#8h-12h
#12h-16h
#16h-20h
