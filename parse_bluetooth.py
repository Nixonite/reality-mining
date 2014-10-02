import scipy.io
from datetime import datetime, timedelta
import time
import sys, os
import itertools
import numpy
from collections import deque


def validSubjects(allSubjects):
   return [s for s in allSubjects if hasNumeric(s,'mac') and hasNumeric(s,'my_hashedNumber')]


# First hash is contiguousId: subjectObject
# second hash is macAddress: contiguousId, subjectObject
# third hash is hashedNumber: contiguousId, subjectObject
# because the id dictionaries reference the subject object, we can replace
# the array of subject objects with these dictionaries.
def idDicts(subjects):
   return (dict((i, s) for (i,s) in enumerate(subjects)),
      dict((getNumeric(s,'mac'), (i, s)) for (i,s) in enumerate(subjects)),
      dict((getNumeric(s, 'my_hashedNumber'), (i, s)) for (i,s) in enumerate(subjects)))
      
    
def matchBlueToothEvents(idd1, idd2):
	mac1 = idd1['mac'][0][0]
	print "Mac 1: ",mac1
	mac2 = idd2['mac'][0][0]
	print "Mac 2: ",mac2
	events = []
	for i in range(len(idd1['device_date'][0])):
		for j in range(len(idd1['device_macs'][0][i])):
			if len(idd1['device_macs'][0][i][j])!=0 and mac2==idd1['device_macs'][0][i][j][0]:
				events.append(convertDatetime(idd1['device_date'][0][i]))
	for k in range(len(idd2['device_date'][0])):
		for l in range(len(idd2['device_macs'][0][k])):
			if len(idd2['device_macs'][0][k][l])!=0 and mac1==idd2['device_macs'][0][k][l][0]:
				if convertDatetime(idd2['device_date'][0][k]) not in events:
					events.append(convertDatetime(idd2['device_date'][0][k]))	
	#events = events.sort()
	return events
	
def isWeekend(d):
	if d.isoweekday()==5 or d.isoweekday()==6 or d.isoweekday()==7:
		return True
	else: return False
	
def filterByWeekend(events):
	list =[]
	for i in events:
		if isWeekend(i):
			list.append(i)
	return list

def convertDatetime(dt):
   return datetime.fromordinal(int(dt)) + timedelta(days=dt%1) - timedelta(days=366) - timedelta(hours=5)

def makeGraph(events):
	x = []
	for i in events:
		if i not in X:
			x.append(i)
	y=[]
	count = 0
	for k in x:
		for j in events:
			if k==j:
				count = count + 1
	y.append(count)
	count = 0
	#plot
	
def filterByTime(events,starth,endh):
	list = []
	for i in events:
		if i.hour >= starh and i.hour<= endh:
			list.append(i)
	return list
	
def filterByWeekend(events):
	list = []
	for i in events:
		if isWeekend(i):
			list.append(i)
	return list

def isFriend(user1,user2):
	events = filterByTime(filterByWeekend(matchBlueToothEvents(user1,user2)))
	if events> 10:
		return True
	else:
		return False

# survey values are either numeric or numpy.nan, so we need special
# functions to account for means/maxes involving nan.
def mean(x, y):
   if numpy.isnan(x):
      return mean(0, y)
   if numpy.isnan(y):
      return mean(x, 0)
   return float(x + y) / 2

def myMax(x, y):
   if numpy.isnan(x):
      return myMax(0, y)
   if numpy.isnan(y):
      return myMax(x, 0)
   return max(x,y)