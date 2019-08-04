from __future__ import print_function
import json
import datetime
import tzlocal
import sys


print('Opening file...')

with open("D:\Takeout\Location History\Location History.json", "r") as locationJSON:
    dictionary = json.load(locationJSON)
    locationJSON.close()
    
#show user starting message
print('Finding dates within range')

#show user size of file
recordCount = len(dictionary['locations'])
print('Number of records to process: ' + str(recordCount))

recordsProcessed = 0
recordsFound = 0
newList = []

for record in dictionary['locations']:
    
    #get local time zone        
    localTimezone = tzlocal.get_localzone()

    #convert timestamp to datetime
    timestamp = datetime.datetime.fromtimestamp(float(record["timestampMs"])/1000, localTimezone) 

    #define tax year dates
    taxStartDate = datetime.datetime(2018, 7, 1, tzinfo=localTimezone) #.strftime('%a, %d %b %Y %H:%M:%S')
    taxEndDate = datetime.datetime(2019,6,30,tzinfo=localTimezone)

    #check if in range
    if timestamp > taxStartDate and timestamp < taxEndDate:
        
        #printout for user
        recordsFound += 1
        sys.stdout.write("\rNumber of records found: " + str(recordsFound))
        sys.stdout.flush()

        #push to new file
        newList.append(record)
        
    recordsProcessed += 1  

print("\nWriting new file...")
newDic = {'locations' : []}
newDic['locations'] = newList

with open("D:\Takeout\Location History\FinacialYear.json", 'w') as outfile:
    json.dump(newDic, outfile)
    outfile.close()
    

print('\nFinished')

