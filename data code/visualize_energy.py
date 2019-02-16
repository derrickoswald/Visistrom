#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 13:07:44 2019

@author: cuozzo

Created on Fri Feb 15 13:07:44 2019

@author: cuozzo

Note: the sunset module used to calculate sunrise and sunset times was lightly adapted from

the code of Rick Harris (rconradharris)

https://github.com/rconradharris/pysunset 

"""

from numpy import array, zeros, repeat, amin # import module to work with arrays / matrices
from datetime import datetime, date # import module to deal with dates, time, etc.
from pandas import read_excel, DataFrame # import module to load excel data
from numpy import array, concatenate # import module to work with arrays / matrices
from sunset import get_sunset, get_sunrise # import module to access to the hours of sunrise/sunset at a precise location, at a given date
from General_functions import createTimeList, FindHypotheticalIndex
import matplotlib.pyplot as plt # import module to make graphs
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_pdf import PdfPages

dico_weekday = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
dico_weekday_index = {0:0, 1:0, 2:0, 3:0, 4:0, 5:1, 6:2} # for each weekday key returns the index value to use in the probability matrices of the Houshold objects (hld.initP, hld.transP, hld.durationD)

timeratio = 15 # the ratio to convert from measured timepoints to 1440x1min timpeoints => number of minutes that separate 2 observed timepoints
Ntmp = 96 # Number of measured timepoints for one day
Time = createTimeList(Ntmp,timeratio) # create a list of string code time points, observed time points reso9lution => cf: General_functions, createTimeList

Dates = [] # empty list
for day in Datum[1:]: # loop for each line/row of the file
    Dates.append(str(day).split(' ')[0]) # saving the date
Dates = list(zip(*[iter(Dates)]*Ntmp)) # changing the list into a list of sub-lists => each sublist corresponds to one day timepoints (96 x 15 minutes)
Dates = [sorted(list(set(dates)))[0] for dates in Dates] # we want each date only onc


lat, lng =  47.0982, 7.4405 # St-Imier GPS coordinates (Flexi project measurments reference location) => latitudes, longitudes
utc_offset = 1 # Universal Time Coordinated => CDT => apparently time sumer/winter time change was not taken into account during the measurment so no need to bother with the hour switching        
startDay = 0 # included => int(input('Select the index of the first day taken for the simulation, between 0 and len(load): '))
endDay = 396 # 30 # 396 # not included => int(input('Select the index of the last day taken for the simulation, between startDay and len(load)-1: '))

data = read_excel('MD_T1_MFH1.xlsx')#,na_values="*)") # load excel file
matrixdata = data.as_matrix() # convert data into a matrix

Datum = array(matrixdata[0:len(matrixdata),0:1])[list(range(len(matrixdata))),[0]*len(matrixdata)] # devCode is the list of devices' names =>  to correct the really annoying format of the original array loaded by the matlab file... => we move from array([array([0]),array([1])...]) to array([0,1]), which is way more suitable for the next parts !       
Zeit = array(matrixdata[0:len(matrixdata),1:2])[list(range(len(matrixdata))),[0]*len(matrixdata)] # devCode is the list of devices' names =>  to correct the really annoying format of the original array loaded by the matlab file... => we move from array([array([0]),array([1])...]) to array([0,1]), which is way more suitable for the next parts !       
Wirkleistung = array(matrixdata[0:len(matrixdata),2:3])[list(range(len(matrixdata))),[0]*len(matrixdata)] # devCode is the list of devices' names =>  to correct the really annoying format of the original array loaded by the matlab file... => we move from array([array([0]),array([1])...]) to array([0,1]), which is way more suitable for the next parts !       

loadcurve = array(list(zip(*[iter(list(Wirkleistung[1:]))]*Ntmp))) # total loadcurve of the selected Household => list subdivided into sub-lists => each sublist corresponds to the loadcurve for one day (96 x 15 minutes timepoints)
loadcurve = loadcurve*4*1000 # loadcurve converted from kiloWatt hour per 15min [kWh] in Watt [W]


seasons = {
'2017':{'spring':'03-20','summer':'06-21','autumn':'09-22','winter':'12-21'},
'2018':{'spring':'03-20','summer':'06-21','autumn':'09-23','winter':'12-22'}
}



# ------------------------ #
# 4 previous weeks Average #
# ------------------------ #            
Average4 = zeros((len(loadcurve),len(loadcurve[0]))) + loadcurve
Average4 += roll(loadcurve,-21,0)
Average4 += roll(loadcurve,-14,0)
Average4 += roll(loadcurve,-7,0)
Average4 /= 4
Average4 = Average4/4/1000

averageFrame = array(zeros((len(Wirkleistung[1:]),4)),dtype=object)
averageFrame[:,0] = Datum[1:] #array(Time*396)
averageFrame[:,1] = Zeit[1:]
averageFrame[:,2] = reshape(Average4,len(Wirkleistung[1:]))
averageFrame[:,3] = Wirkleistung[1:]
DataFrame(averageFrame).to_csv('Results/4weeks_dataset1.csv')

month_average = zeros((len(loadcurve),len(loadcurve[0])))
season_average = zeros((len(loadcurve),len(loadcurve[0])))
"""
split = Dates[Nday].split(' ')[0].split('-') # splits the day string into a list separating the day, month and year
dateofday = date(int(split[0]),int(split[1]),int(split[2])) # uses the datetime module to give the exact date in a usable format
old_month = str(dateofday).split('-')[1]
M = 0
"""
S = 0

for Nday in range(startDay,min(endDay,len(loadcurve))): # main loop of the simulation for the day => mesload is the measured loadcurve        
        
        # -------------------------------- #
        #   Find the weekday of the date   #
        # -------------------------------- #
        split = Dates[Nday].split(' ')[0].split('-') # splits the day string into a list separating the day, month and year
        dateofday = date(int(split[0]),int(split[1]),int(split[2])) # uses the datetime module to give the exact date in a usable format
        weekday = dateofday.weekday() # uses the datetime module: gives the week of the day for the given date in the form of an integer (0=monday, 1=tuesday, 2=wednesday, 3=thursday, 4=friday, 5=saturday, 6=sunday)
        year = str(dateofday).split('-')[0]
        day = dico_weekday[weekday] # day of the week in string (monday, tuesday, wednesday, thursday, friday, saturday, sunday)
        month = str(dateofday).split('-')[1]
        daymonth = str(dateofday).split('-')[2] 
    

        # --------------- #
        # Monthly Average #
        # --------------- #  
        month_average[int(month)] += loadcurve[Nday]
        """
        if old_month == month:
            M += 1
        else:
            month_average[int(month)-1] /= M
            M = 0
            old_month = month
        """
        
        # -------------- #
        # season Average #
        # -------------- #
        index = Dates.index(str(dateofday))
        if 50 < index < 143: # Autumn 2017
            case = 2
        elif 143 < index < 232: # Winter 2017-2018
            case = 3
        elif 232 < index < 324: # Spring 2018
            case = 0
        else: # Summer -> mix 2017-2018
            case = 1
        season_average[case] += loadcurve[Nday]

month_average[0] /= 31
month_average[1] /= 28
month_average[2] /= 31
month_average[3] /= 30
month_average[4] /= 31
month_average[5] /= 30
month_average[6] /= 31
month_average[7] /= 30
month_average[8] /= 31
month_average[9] /= 30
month_average[10] /= 31
month_average[11] /= 30
month_average[12] /= 31



season_average[2] /= 143-50
season_average[3] /= 232-143
season_average[0] /= 324-232
season_average[1] /= len(Dates)-324+50

####################################
# CREATE FILES FOR RESULTS STORAGE #
####################################

with PdfPages('Results/Loadcurve_'+str(startDay)+'-'+str(endDay)+'_'+today+'.pdf') as pdf:

    ###########################################
    # FIRST MAIN LOOP - FOR EACH MEASURED DAY #
    ###########################################
        
    for Nday in range(startDay,min(endDay,len(loadcurve))): # main loop of the simulation for the day => mesload is the measured loadcurve        
        
        print('Progression Run:\tDay ===',Nday+1,'/',endDay)
        
        
        # -------------------------------- #
        #   Find the weekday of the date   #
        # -------------------------------- #
        split = Dates[Nday].split(' ')[0].split('-') # splits the day string into a list separating the day, month and year
        dateofday = date(int(split[0]),int(split[1]),int(split[2])) # uses the datetime module to give the exact date in a usable format
        weekday = dateofday.weekday() # uses the datetime module: gives the week of the day for the given date in the form of an integer (0=monday, 1=tuesday, 2=wednesday, 3=thursday, 4=friday, 5=saturday, 6=sunday)
        year = str(dateofday).split('-')[0]
        day = dico_weekday[weekday] # day of the week in string (monday, tuesday, wednesday, thursday, friday, saturday, sunday)
        month = str(dateofday).split('-')[1]
        daymonth = str(dateofday).split('-')[2] 
        

        # ---------------------------------------------------- #
        # Calculate sunrise and sunset hours at the given date # 
        # ---------------------------------------------------- #
        sunset = str(get_sunset(dateofday, lat, lng, utc_offset)).split(' ')[1] # uses the sunset module to calculate the sunset hour at this date
        sunrise = str(get_sunrise(dateofday, lat, lng, utc_offset)).split(' ')[1] # uses the sunset module to calculate the sunrise hour at this date
        sunset_index = FindHypotheticalIndex(Time,sunset)
        sunrise_index = FindHypotheticalIndex(Time,sunrise)
        
        # ----------------------------------------------- #
        # PDF containg graphs for each day of the profile #
        # ----------------------------------------------- #
        fig=plt.figure # initialize a figure
        
        OBSERVED = plt.plot(Time,loadcurve[Nday],linestyle="-",marker="",label="Observed",color="green") # make the graph
        #AVERAGE = plt.plot(Time,Average4[Nday]*4*1000,linestyle="-",marker="",label="Average 4 w",color="cyan") # make the graph
        plt.grid(True)
        ax=plt.gca() # To customize the axis ticks A
        ax.set_xticks([0,16,32,48,64,80,95]) # choose which x locations to have ticks
        ax.set_xticklabels(['00:15','04:15','08:15','12:15','16:15','20:15','24:00']) # set the labels to display at those ticks
            
        ax.annotate('', xy=(Time[sunrise_index], min(loadcurve[Nday])-0.003), xytext=(Time[sunrise_index], min(loadcurve[Nday])-0.006),arrowprops=dict(facecolor='darkorange', shrink=0.05,headwidth=7))
        ax.annotate('', xy=(Time[sunset_index], min(loadcurve[Nday])-0.003), xytext=(Time[sunset_index], min(loadcurve[Nday])-0.006),arrowprops=dict(facecolor='turquoise', shrink=0.05,headwidth=7))

        plt.suptitle('Load curve of '+day+' '+str(dateofday)+' for MD_T1_MFH1')
        plt.xlabel("Time [15 minutes timepoints]") # title for X axis
        plt.ylabel("Energy in Watt [W]") # title for Y axis
        
        
        fontP = FontProperties()
        fontP.set_size('small') # xx-small / x-small / small / medium / large / x-large / xx-large
        plt.legend([OBSERVED[0]])
        #plt.legend([OBSERVED[0],AVERAGE[0]])
            
        pdf.savefig(bbox_inches='tight')
        plt.clf()

with PdfPages('Results/month_'+str(startDay)+'-'+str(endDay)+'_'+today+'.pdf') as pdf:
    
    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    for i in range(12):
        
        # ----------------------------------------------- #
        # PDF containg graphs for each day of the profile #
        # ----------------------------------------------- #
        fig=plt.figure # initialize a figure
        
        MONTH = plt.plot(Time,month_average[i],linestyle="-",marker="",label="Month",color="green") # make the graph
        plt.grid(True)
        ax=plt.gca() # To customize the axis ticks A
        ax.set_xticks([0,16,32,48,64,80,95]) # choose which x locations to have ticks
        ax.set_xticklabels(['00:15','04:15','08:15','12:15','16:15','20:15','24:00']) # set the labels to display at those ticks
            
        plt.suptitle('Load curve of '+month_list[i]+' for MD_T1_MFH1')
        plt.xlabel("Time [15 minutes timepoints]") # title for X axis
        plt.ylabel("Energy in Watt [W]") # title for Y axis        
        
        fontP = FontProperties()
        fontP.set_size('small') # xx-small / x-small / small / medium / large / x-large / xx-large
        #plt.legend([OBSERVED[0])
        plt.legend([MONTH[0]])
            
        pdf.savefig(bbox_inches='tight')
        plt.clf()    
    

with PdfPages('Results/season_'+str(startDay)+'-'+str(endDay)+'_'+today+'.pdf') as pdf:
    
    season_list = ['Spring','Summer','Autumn','Winter']
    
    for i in range(4):
        
        # ----------------------------------------------- #
        # PDF containg graphs for each day of the profile #
        # ----------------------------------------------- #
        fig=plt.figure # initialize a figure
        
        SEASON = plt.plot(Time,season_average[i],linestyle="-",marker="",label="Season",color="green") # make the graph
        plt.grid(True)
        ax=plt.gca() # To customize the axis ticks A
        ax.set_xticks([0,16,32,48,64,80,95]) # choose which x locations to have ticks
        ax.set_xticklabels(['00:15','04:15','08:15','12:15','16:15','20:15','24:00']) # set the labels to display at those ticks
            
        plt.suptitle('Load curve of '+season_list[i]+' for MD_T1_MFH1')
        plt.xlabel("Time [15 minutes timepoints]") # title for X axis
        plt.ylabel("Energy in Watt [W]") # title for Y axis        
        
        fontP = FontProperties()
        fontP.set_size('small') # xx-small / x-small / small / medium / large / x-large / xx-large
        #plt.legend([OBSERVED[0])
        plt.legend([SEASON[0]])
            
        pdf.savefig(bbox_inches='tight')
        plt.clf()    
