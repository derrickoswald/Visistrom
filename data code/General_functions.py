# -*- coding: utf-8 -*-
"""
###########################################
###########################################
DEVICE USAGE PREDICTION - GENERAL FUNCTIONS
###########################################
###########################################

This module contains all general functions that are used to the disaggregation algorithm, but that can potentially be used in other programs as well. 

Created on Wed Feb 14 16:18:21 2018

@author: cuozzo
"""

##############################################
##############################################
##      FUNCTIONS SET OF GENERAL USAGE      ##
##############################################
##############################################

from numpy import array, matrix, roll, dot, tile, cumsum, random

############################################################
#  find the local maxima and minima ("peaks") in a vector  #
############################################################

def FindPeakLocations(vector1,vector2,delta): # vector1 and vector 2 are linear arrays (or lists) of data, delta is the threshold to compare the points

    """find the local maxima and minima ("peaks") in a vector. A point is considered a maximum peak if the difference with the previous or next point is higher than delta
    if we just need the regular index, vector 2 will correspond to the indexes of vector1
    
    - **Input**:
        - :vector1: linear array (or list) of data
        - :vector2: linear array (or list) of data
        - :delta: the threshold to compare the points
    
    - **Output**:
        - :max_peaks: dictionnary that contains all maximum peaks of vector1, its index, and the corresponding value in vector2
        - :min_peaks: dictionnary that contains all minimum peaks of vector1, its index, and the corresponding value in vector2"""
    
    max_peaks = {'time':[],'value':[],'index':[]} # maximum peak: will consist of two columns. Column 1 contains the position where the peak is found in the vector, and column 2 is the value
    min_peaks = {'time':[],'value':[],'index':[]} # minimum peak: same logic as max_peaks
    
    if list(vector2) == list(vector1): # if we just need the regular index
        vector2 = range(len(vector1)) # vector 2 will correspond to the indexes of vector1
     
    for i in range(0,len(vector1)): # loop for all points in the vector     
        if i>0: # if we have passed the first point
            if abs(vector1[i]-vector1[i-1]) > delta: # if the difference is above the threshold
                if vector1[i] > vector1[i-1]: # if the current value is higher than the previous one
                    if len(max_peaks['time'])==0 or max_peaks['time'][-1]!=vector2[i]: # if we have not already added this peak
                        max_peaks['time'].append(vector2[i]) # current=max => add to max list
                        max_peaks['value'].append(vector1[i]) # current=max => add to max list
                        max_peaks['index'].append(list(vector2).index(vector2[i])) # current=max => add to max list
                    if len(min_peaks['time'])==0 or min_peaks['time'][-1]!=vector2[i-1]: # if we have not already added this peak
                        min_peaks['time'].append(vector2[i-1]) # previous=min => add to min list
                        min_peaks['value'].append(vector1[i-1]) # previous=min => add to min list
                        min_peaks['index'].append(list(vector2).index(vector2[i-1])) # previous min => add to min list
                else: # if the current value is lower than the previous one
                    if len(max_peaks['time'])==0 or max_peaks['time'][-1]!=vector2[i-1]: # if we have not already added this peak
                        max_peaks['time'].append(vector2[i-1]) # current=max => add to max list
                        max_peaks['value'].append(vector1[i-1]) # current=max => add to max list
                        max_peaks['index'].append(list(vector2).index(vector2[i-1])) # current=max => add to max list
                    if len(min_peaks['time'])==0 or min_peaks['time'][-1]!=vector2[i]: # if we have not already added this peak
                        min_peaks['time'].append(vector2[i]) # previous=min => add to min list
                        min_peaks['value'].append(vector1[i]) # previous=min => add to min list
                        min_peaks['index'].append(list(vector2).index(vector2[i])) # previous min => add to min list
                    
    return max_peaks,min_peaks

####################################################################################################################
# Find the hypothetical index of where a value should be in a sorted list containing other values of the same kind # 
####################################################################################################################

def FindHypotheticalIndex(sorted_list,value):
    
    """Find the hypothetical index of where a value should be in a sorted list containing other values of the same kind
    
    - **Input**:
        - :sorted_list: the sorted list
        - :value: a value of the same kind than the ones in sorted_list"""
    
    from bisect import insort # import module to provide support for maintaining a list in sorted order without having to sort the list after each insertion
    
    insort(sorted_list, value) # insert the value to the list where it should be respecting the sorting
    value_index = sorted_list.index(value) # value_index is the index of the value in the list
    sorted_list.remove(value) # remove the freshly added value from the sorted list => Important ! (if not, the original list will remain modified)
    
    return value_index

###########################################################################
# Picks and returns a random number (index) from a discrete distribution  #
# By computing the least square from a matrix input                       #
###########################################################################

def discreteRand(discreteP): # Discrete distribution coefficients, in matrix/array shape => Does not have to be normalized.
    
    """Picks and returns a random number (index) from a discrete distribution. By computing the least square from a matrix input.
    
    - **Input**:
        - :discreteP: discrete distribution coefficients, in matrix/array shape => Does not have to be normalized."""
    
    import sys # import sys module to deal with infinity values
    from scipy import linalg # import module to perform matrix operations
    from numpy import random # import module to use random results generating built-in-functions
    from math import inf
    
    discreteP = array(discreteP) # just in case discrete P was not a proper array
    s = discreteP.sum(axis=0) # gives a vector of sum for each column of discreteP
    cum = cumsum(discreteP,axis=0) # gives a vector of cumulative sum for each column of discreteP
    if s==inf: # if s reaches "infinity"
        s = sys.float_info.max # in case the number reaches "infinity" => the linalg module does not support such a number
    cum[cum==inf] = sys.float_info.max # in case the number reaches "infinity" => the linalg module does not support such a number
    least = array(linalg.lstsq(matrix(s),matrix(cum))[0])[0] # uses the linalg module to compute least squares matrix operation (solution of A*X = B)
    R = random.rand(1)[0] # uses the random module: picks a random number between 0 and 1
    index = array(list(range(len(least))),dtype=int) # all indexes of least vector
    index = index[least>=R] # returns vector containing only least square products that are higher than the random number
    if len(index)==0: # if no square number was higher than the random number
        return array([min(least)],dtype=int) # we set the default index any element that has the minimum probability
    else:
        return index[0] # returns the randomly selected number (index) between 1 and length(discreteP) => The lowest found value that is higher or equal to the random number


############################################################
# Returns random vectors drawn from a single GaussD object #
############################################################

def randGaussian(GaussD, nData):
    
    """Returns random vectors drawn from a single GaussD object
    
    - **Input**:
         :GaussD: the GaussD object
         :nDada: scalar defining the number of wanted random data vectors

    - **Output**:
         :R: the random sample from Gaussian"""

    from numpy import random, diag

    mu, sigma = GaussD.Mean, GaussD.StDev # mean and standard deviation
    R = random.randn(int(GaussD.DataSize), nData) # generate random samples from normal (gaussian) => normalized independent Gaussian random variables
    R = dot(R.T,diag(sigma)) # to get the specific standard distribution => scaled to correct standard deviations
    R = dot(R,GaussD.CovEigen) # matrix multiply / scalar product
    R = R + tile(mu, (1, nData)) # create copies of the Matrix
    return R

############################################################
# Returns random vectors drawn from given mean, stdev, etc #
############################################################

def randGaussianV2(mean,stdev,coveigen,datasize,nData):
    
    """ Returns random vectors drawn from given mean, stdev, etc
    
    - **Input**:
         :mean: mean for the distribution
         :stdev: standard deviation
         :coveigen: coveigen vector
         :datasize: size of data
         :nDada: scalar defining the number of wanted random data vectors

    - **Output**:
         :R: the random sample from Gaussian"""

    from numpy import random, diag

    mu, sigma = matrix(mean), matrix(stdev) # mean and standard deviation
    R = matrix(random.randn(int(datasize), nData)) # generate random samples from normal (gaussian) => normalized independent Gaussian random variables
    R = dot(R.T,diag(sigma)) # to get the specific standard distribution => scaled to correct standard deviations
    R = dot(R,matrix(coveigen)) # matrix multiply / scalar product
    R = R + tile(mu, (1, nData)) # create copies of the Matrix
    return random.choice(array(R)[0])

#######################################################################################################
# returns a random duration (random indexes) of activity, among a possible maximum full time duration #
#######################################################################################################

def randindex(start,end,duration):

    """returns a chain of indexes starting sometime between start and end, and respecting duration

    - **Input**:
         :start: minimum start index possible
         :end: minimum end index possible
         :duration: maximum duration possible   

    - **Output**:
         :startindex: new start index inside the available time
         :endindex: new end index inside the available time"""

    if duration>=end-start:  # if we are already short on available time
        startindex = start # we keep the current start
        endindex = end # we keep the current end

    else: # if the given possibility allows a change
        shift = random.randint(0,end-duration+1) # uses the numpy.random module => random shift, according to possible time
        startindex = start + shift # new start
        endindex = startindex + int(duration) # new end
    
    return startindex, endindex
    
#######################################################################################################
# returns a random duration (random indexes) of activity, among a possible maximum full time duration #
#######################################################################################################

def randindexV2(start,end,duration):

    """returns a chain of indexes starting sometime between start and end, and respecting duration

    - **Input**:
         :start: minimum start index possible
         :end: minimum end index possible
         :duration: maximum duration possible   

    - **Output**:
         :startindex: new start index inside the available time
         :indexes: array of randomly selected indexes"""

    from heapq import nsmallest # import module to return the N smallest values in a list

    if duration>end-start:  # if we are already short on available time
        duration = end-start # the duration is the full activity sequence interval
    interval = array(list(range(start,end)),dtype=int) # indexes interval
    R = random.rand(1,len(interval))[0] # vector of random values between 0 and 1
    Nsmallest = array(nsmallest(int(duration),R),dtype=int) # the N smallest values from random vector
    indexes = interval[Nsmallest] # the corresponding indexes
        
    return indexes
    
#######################################################################################################
# returns a random duration (random indexes) of activity, among a possible maximum full time duration #
#######################################################################################################

def randindexV3(freeslot,start,end,duration,P):
    
    """returns a chain of indexes starting sometime between start and end, and respecting duration.

    - **Input**:
         :freeslot: list (array) of possible indexes
         :start: minimum start index possible
         :end: minimum end index possible
         :duration: maximum duration possible
         :P: probability threshsold

    - **Output**:
         :indexes: array of randomly selected indexes"""

    from heapq import nsmallest # import module to return the N smallest values in a list
    #from math import log # Note: in python, log = ln (natural base logarithm)
    # duration = duration*log(len(freeslot)) # strectch or reduce the duration according to length of the interval => N.B. In python log = ln (natural base logarithm)
    
    if duration>end-start:  # if we are already short on available time
        duration = end-start # the duration is the full activity sequence interval
    interval = array(list(freeslot),dtype=int) # incase it was not a list
    R = sorted(random.rand(1,len(interval))[0]) # vector of random values between 0 and 1, sorted by size
    Rint = random.randint(0,len(interval)) # random integer that will device where the device will be turned ON => it respects the freeslot
    R = roll(R,Rint) # roll the randomly  position of the devices where it can be used => it respects the freeslot possibility
    Nsmallest = array(nsmallest(int(duration),R),dtype=int) # the N smallest values from random vector
    Nsmallest = Nsmallest[Nsmallest<=P] # keep only the timepoints where the values are lower or equal to the probabilitiy threshold (device usage probability)
    indexes = interval[Nsmallest] # the corresponding indexes
            
    return indexes
    

#######################################################################################################################################
# returns the next start and end index of a value, in a vector containing following sequences with varying length of different values #
###################################################################################################################################### #

def TrackIndex(SeqChain,start,end,seq,target):
    
    """returns the next start and end index of a value, in a vector containing following sequences with varying length of different values
    

    - **Input**:
           :SeqChain: The original complete sequence
           :start: default start index
           :end: default end index 
           :seq: the sequence part in which we are currently tracking the values 
           :target: the target to track

    - **Output**:
           :start: the start index of the tracked value in seq
           :end: the end index of the tracked value in seq
           :seq: the sequence shortened at the left until newly tracked start"""

    seq = array(seq) # in case seq was not a proper array
    start = end+list(seq).index(seq[seq==target][0]) # nearest starting point of the target
    seq = SeqChain[start:] # we don't care about the timepoints/values before start
    if len(set(list(seq)))>1: # if the remaining time/values contains at least another activity/value than our target
        end = start+list(seq).index(seq[seq!=target][0]) # nearest ending point of the target
    else: # if the remaining time/values does not contain the target
        end = len(SeqChain) # the end is the end of the day/vector
    seq = SeqChain[end:] # passed time/values = everything before the end
    
    
    return start, end, seq

###################################################################################################################################
# Takes a vector containing following subsequences of values, and returns a smaller vector containing the mean a each subsequence #
###################################################################################################################################

def meanSubseqVector(vector, n):
    
    """Takes a vector containing following subsequences of values, and returns a smaller vector containing the mean a each subsequence

    - **Input**:
           :vector: original vector of subsequence
           :n: the number of following subsequences

    - **Output**:
           :meanvector: vector containing the mean of each subsequence"""
    
    meanvector = list(zip(*[iter(list(vector))]*n)) # vector of values, regrouped in n sublists of values
    meanvector = array([sum(meanvector[t])/n for t in range(len(meanvector))]) # mean for each sublist
    # meanvector = array(list(map(lambda x: sum(x)/n,vector))) # do the same thing but slower
    
    return meanvector

#######################################################################
# Converts a number equal to 4 to another number higher or equal than #
#######################################################################
    
def maxNumber(number1, number2): 
    
    """Converts a number equal to 4 to another number higher or equal than
    
    - **Input**:
           :number1: the first number
           :number2: the second number
    
    - **Output**:
        - :number1: the selected number (may not be the same as the number1 from input)"""
    
    if number1==4: # if the number is equal to four 4
        number1 = max(number1, number2) # return the maximum number between number1 and 4
    return number1 

#####################################################################################
# Custom print => print values of a dictionnary according to values of another one  #
#####################################################################################

def customprint(dico,dico2,key):
    
    """Custom print => print values of a dictionnary according to values of another on
    
    - **Input**:
        - :dico1: dictionnary with keys and values
        - :dico2: dictionnary with keys and values
        - :key: the key that will be used"""
    
    print(key+':',len(dico[key])) # print the key + number of values
    for value in dico[key]: # for each value in the dictionnary's key
        print(' ',dico2[value]) # the second value is the value of the second dictionnary, which is the value of the previous
        
##########################################################################################
# Custom sort => sort a 2D list (vector) where each component itself is a list (vector)  #
# Sort according to the first component (in position 0)                                  # 
##########################################################################################

def comparator(value): # value is an element with length > 1
    
    """Get teh first element of a list, array, any object that can be indexed.
    
    - **Input**:
        - :value: an element (list, array, any object that can be indexed) with length > 0
        
    - **Output**:
        - the first element of value [element in position index=0]"""
    
    return value[0] # return the second element (in position 0)

def sort_by_first(list2d): # list where all elements inside possess length > 1
    
    """Custom sort => sort a 2D list (vector) where each component itself is a list (vector).
    Sort according to the first component (in position 0).
    
    - **Input**:
        - :list2d: a list of sub-lists
        
    - **Output**:
        - :list2d: the sorted list of sub-lists"""
        
    list2d.sort(key=comparator) # sort using the comparator specified in the previous function
    return list2d


####################
# create time list #
####################

def createTimeList(Ntmp,res):
    
    """Create string time list of dataset timepoints for one day
    
    - **Input**:
        - :Ntmp: number of timepoints of the data
        - :res: time resolution separating 2 timwpoints
    
    - **Output**:
        - :liste: the build time list"""

    from datetime import time # import module to deal with dates, time, etc.

    liste = [] # empty final list
    hour = 0 # hour counter
    minute = 0 # minute counter

    for i in range(0,Ntmp): # loop for each timepoint
        minute += res # next resolution minute of the timepoint
        if minute == 60: # we have reached one hour
            hour += 1 # next hour
            minute = 0 # reset minute
        now = str(time(0,hour,minute)) # call the datetime module to get the timepoint in string format
        split = now.split(':')[1:3] # we do not take the seconds
        join = ':'.join(split) # rejoin only hours and minutes
        liste.append(join) # add current timepoint to the list
        
    return liste