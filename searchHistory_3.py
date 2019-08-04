from __future__ import print_function
import json
import datetime
import tzlocal
import sys
import csv
import pprint

print('Opening file...')

with open("D:\Takeout\Location History\FinacialYear.json", "r") as locationJSON:
    dictionary = json.load(locationJSON)
    locationJSON.close()
   

#show user size of file
recordCount = len(dictionary['locations'])
print('Number of records to process: ' + str(recordCount))

#set up variables
dateList = []
recordList = []
range = []
longTarget = 1385150560
latTarget = -348785870
accuracy = 10000

#get local time zone        
localTimezone = tzlocal.get_localzone()

totalRecords = str(len(dictionary['locations']))
addedRecords = 0
rejectedRecords = 0

for record in dictionary['locations']:
    
    timestamp = datetime.datetime.fromtimestamp(float(record["timestampMs"])/1000, localTimezone)

    if (timestamp.date() not in dateList) and \
       (record['longitudeE7'] > longTarget - accuracy and record['longitudeE7'] < longTarget + accuracy) and \
       (record['latitudeE7'] > latTarget - accuracy and record['latitudeE7'] < latTarget + accuracy):        

        dateList.append(timestamp.date())
        recordList.append([str(float(record['latitudeE7'])/10000000), str(float(record['longitudeE7'])/10000000), 'circle1', 'red', 1, str(timestamp.date())])
        addedRecords += 1
        
    else:
        rejectedRecords += 1
        
    sys.stdout.write('\rTotal records:' + totalRecords + " Added reccords:" + str(addedRecords) + " Rejected records:" + str(rejectedRecords))
    sys.stdout.flush()


range = [[str(float(latTarget)/10000000), str(float(longTarget)/10000000),'diamond3', 'yellow', 3, 'Center of search'],
        [str(float(latTarget - accuracy)/10000000), str(float(longTarget - accuracy)/10000000),'cross3', 'blue', 1, 'Corner of search'],
        [str(float(latTarget + accuracy)/10000000), str(float(longTarget + accuracy)/10000000),'cross3', 'blue', 1, 'Corner of search'],
        [str(float(latTarget - accuracy)/10000000), str(float(longTarget + accuracy)/10000000),'cross3', 'blue', 1, 'Corner of search'],
        [str(float(latTarget + accuracy)/10000000), str(float(longTarget - accuracy)/10000000),'cross3', 'blue', 1, 'Corner of search']]



with open('D:\Takeout\Location History\dates.csv', 'w', newline='') as dateWriter:
    file = csv.writer(dateWriter, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    file.writerows(recordList)
    file.writerows(range)
    
       
print('\nFinished')

# Copy and paste the data in the dates.csv into this website.
# http://www.hamstermap.com/map.php

