from __future__ import print_function
import json
import datetime
import tzlocal
import sys
import csv


print('Opening file...')

with open("E:\\Location History\\Takeout\\finacialYear.json", "r") as locationJSON:
    dictionary = json.load(locationJSON)
    locationJSON.close()
   

#show user size of file
recordCount = len(dictionary['locations'])
print('Number of records to process: ' + str(recordCount))

#set up variables

dateList = []
recordList = []
longTarget = 1385308020
latTarget = -349373620
accuracy = 1000
print(dictionary['locations'][0].keys())

#get local time zone        
localTimezone = tzlocal.get_localzone()

for record in dictionary['locations']:
    
    timestamp = datetime.datetime.fromtimestamp(float(record["timestampMs"])/1000, localTimezone)

    if (timestamp.date() not in dateList) and \
       (record['longitudeE7'] > longTarget - accuracy and record['longitudeE7'] < longTarget + accuracy) and \
       (record['latitudeE7'] > latTarget - accuracy and record['latitudeE7'] > latTarget + accuracy):
        print("adding reccord")
        dateList.append(timestamp.date())
        recordList.append(record)

with open('dates.csv', 'wb') as dateWriter:
    file = csv.writer(dateWriter, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for date in dateList:
        file.writerow([date])
    
print(dateList)
print('\nFinished')

# used to get acacia travel data
