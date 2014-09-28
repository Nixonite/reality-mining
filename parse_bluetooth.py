import scipy.io
from datetime import datetime, timedelta
import time
import sys, os
import itertools
import numpy
from collections import deque

def hasNumeric(obj, field):
   try:
      obj[field][0][0]
      return True
   except:
      return False


def getNumeric(obj, field):
   return obj[field][0][0]


def hasArray(obj, field):
   try:
      obj[field][0]
      return True
   except:
      return False


def getArray(obj, field):
   return obj[field][0]


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
      
def isEmpty(obj):
    if len(obj)==0:
        return True
    return False
      
def countEncounters(p1, p2):
    print "working gina's code"
    counter=0
    t=[]
    for i in xrange(len(p1['device_date'][0])):
        for j in xrange(len(p1['device_macs'][0][i])):
            if isEmpty(p1['device_macs'][0][i][j])==False and p2['mac'][0][0]==p1['device_macs'][0][i][j][0]:
            	t.append(convertDatetime(p1['device_date'][0][i]))
            	counter+=1
    return counter, t #timeArray1,t
    
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

def convertDatetime(dt):
   return datetime.fromordinal(int(dt)) + timedelta(days=dt%1) - timedelta(days=366) - timedelta(hours=5)


def inRange(dateRange, timevalue):
   start, end = dateRange
   unixTime = int(time.mktime(timevalue.timetuple()))
   return start <= unixTime <= end


def filterByDate(dateRange, events):
   filteredCalls = [e for e in events if inRange(dateRange, e['date'])]
   print("%d calls after filtering by date" % len(filteredCalls))
   return filteredCalls


def writeCallEvents(callEventDicts, filename):
   with open(filename, 'w') as outfile:
      outfile.write('subjectId\totherPartyId\tduration\tdirection\tdate\n')
      for d in callEventDicts:
         values = [d['subjectId'], d['otherPartyId'], d['duration'], d['direction'], d['date']]
         line = '\t'.join(("%s" % (v,)) for v in values)
         outfile.write('%s\n' % line)

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


def dateIntervalOverlap(dtint1, dtint2):
   start1, end1 = dtint1
   start2, end2 = dtint2

   if start1 <= start2 <= end1:
      return (start2, min(end1, end2))
   elif start2 <= start1 <= end2:
      return (start1, min(end1, end2))
   else:
      return None


if __name__ == "__main__":
   

   #createFriendshipDataset(matlab_obj['network'][0][0], idDictionaries)
   #createPhoneCallDataset(idDictionaries)
   createCellTowerDataset(idDictionaries)