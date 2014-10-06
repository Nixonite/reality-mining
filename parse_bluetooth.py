import scipy.io
from datetime import datetime, timedelta
import time
import sys, os
import itertools
import numpy as np
from collections import deque

def hasNumeric(obj, field):
   try:
      obj[field][0][0]
      return True
   except:
      return False
      
def getNumeric(obj, field):
   return obj[field][0][0]

def validSubjects(allSubjects):#kept as is
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

def matchBlueToothEvents(idd1, idd2): #returns bluetooth matches for user1->user2 AND user2->user1
	mac1 = idd1['mac'][0][0]
	mac2 = idd2['mac'][0][0]
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
	
def printAllFriends(idd):
	for i in range(1,len(idd[0])): #actually no need to go all the way through, only halfway since redundant
		for j in range(1,len(idd[0])):
			print "User:",i,"\t User:",j,"\t",isFriend(idd[0][i],idd[0][j])
	
	
def isWeekend(d):
	if d.isoweekday()==5 or d.isoweekday()==6 or d.isoweekday()==7:
		return True
	else: return False

def convertDatetime(dt):
   return datetime.fromordinal(int(dt)) + timedelta(days=dt%1) - timedelta(days=366) - timedelta(hours=5)

def makeGraph(events): #nevermind this is not a useful function, but it might be interesting someday
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
	
def numberOfUniqueDays(events):
	return len({(i.day,i.month,i.year) for i in events})
	
def isHoliday(date):
	if(date.month== 10 and date.day == 31):#halloween
		return True
	elif(date.month == 11 and (date.day == 25 or date.day == 26)):#thanksgiving and black friday
		return True
	elif(date.month == 12 and (date.day == 24 or date.day == 25 or date.day == 31)):#christmas eve, christmas, new year's eve
		return True
	elif(date.month == 1 and date.day == 1):#new year day
		return True
	elif(date.month == 2 and date.day == 14):#valentine's day
		return True
	else:
		return False
		
def HolidayEvents(events):#returns all events which are holidays
	hEvents = []
	for i in events:
		if isHoliday(i):
			hEvents.append(i)
	return hEvents
	
def filterByTime(events,starth,endh):
	list = []
	for i in events:
		if i.hour >= starth and i.hour<= endh:
			list.append(i)
	return list
	
def filterByWeekend(events):#returns weekend events
	list = []
	for i in events:
		if isWeekend(i):
			list.append(i)
	return list
	
def friendMatrix():
	#np array = [[list],[list],[list]... etc. in loop ]]

def isFriend(user1,user2):
	events = filterByTime(filterByWeekend(matchBlueToothEvents(user1,user2)),1,23)#friday 1am to saturday 11pm
	holidayEvents = matchBlueToothEvents(user1,user2)
	
	#numbers are based on number of scans which take place every 6 minutes for two people
	
	if (len(holidayEvents)>80 and numberOfUniqueDays(events)>=12 and len(events)>120):
		return True
	elif(numberOfUniqueDays(events)>=18 and len(events)>180):
		return True
	else: return False