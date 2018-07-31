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
range = []
longTarget = 1385190550
latTarget = -348690880
accuracy = 10000
print(dictionary['locations'][0].keys()) 

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

        print(timestamp.date())
        dateList.append(timestamp.date())
        recordList.append(str(float(record['latitudeE7'])/10000000) + "; " + str(float(record['longitudeE7'])/10000000))
        addedRecords += 1
        
    else:
        rejectedRecords += 1
        
    print('Total records:' + totalRecords + " Added reccords:" + str(addedRecords) + " Rejected records:" + str(rejectedRecords))

#convert lists to rows
rows = zip(dateList, recordList)

range = (str(float(latTarget)/10000000) + " " + str(float(longTarget)/10000000), \
        str(float(latTarget - accuracy)/10000000) + " " + str(float(longTarget - accuracy)/10000000), \
        str(float(latTarget + accuracy)/10000000) + " " + str(float(longTarget + accuracy)/10000000), \
        str(float(latTarget - accuracy)/10000000) + " " + str(float(longTarget + accuracy)/10000000), \
        str(float(latTarget + accuracy)/10000000) + " " + str(float(longTarget - accuracy)/10000000))

print(range)

with open('dates.csv', 'wb') as dateWriter:
    file = csv.writer(dateWriter, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    file.writerows(rows)
    
       
print(rows[0])
print('\nFinished')

