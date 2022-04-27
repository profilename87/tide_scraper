#This script goes to the tide forecast site, and returns a list of low tides during the
# day for four locations. The output covers the forecast for the next 30 days.
#External dependencies: BeautifulSoup4
import urllib.request
from bs4 import BeautifulSoup
import json
#Format output and add list of locations
#tideURL = 'https://www.tide-forecast.com/locations/Half-Moon-Bay-California/tides/latest'

def getTideForecast(location, tideURL):
    tableID = 'window.FCGON = '
    #Get the forecast page
    request = urllib.request.Request(tideURL)
    try:
        response = urllib.request.urlopen(request)
    except:
        print("Something went wrong accessing the forecast page")
    #Decode text and set up beautifulSoup parser
    tideString = response.read().decode("utf8")
    tideSoup = BeautifulSoup(tideString, "html.parser")
    #Get list of script tags
    scriptTags = tideSoup.find_all('script')
    for each in scriptTags:
        scriptString = str(each.string)
        #Get tide table and remove leading and trailing characters
        if tableID in scriptString:
            tableString = scriptString.split(tableID, 1)[1]
            tableString = tableString.split(';\n', 1)[0]
            break
    #Convert table to json
    tableJson = json.loads(tableString)
    #print header
    print('\n\n' + location + '\nDate\t\t  Time\t\tHeight(ft)')
    #Iterate through table and save low tides between sunrise and sunset
    for dates in tableJson['tideDays']:
        date = dates['date']
        sunrise = dates['sunrise']
        sunset = dates['sunset']
        for tides in dates['tides']:
            if tides['type'] == 'low' and tides['timestamp'] > sunrise and tides['timestamp'] < sunset:
                #Formatting output
                height = str(round(float(tides['height'])*3.28, 2))
                time = tides['time']
                row = date + '\t ' + time + '\t' + height
                print(row)
if __name__ == '__main__':
    #List of locations/urls. Hardcoding these because there are only 4 locations
    locationList = [['Half Moon Bay, California', 'https://www.tide-forecast.com/locations/Half-Moon-Bay-California/tides/latest'],
                    ['Huntington-Beach, California', 'https://www.tide-forecast.com/locations/Huntington-Beach/tides/latest'],
                    ['Providence, Rhode Island', 'https://www.tide-forecast.com/locations/Providence-Rhode-Island/tides/latest'],
                    ['Wrightsville Beach, North Carolina', 'https://www.tide-forecast.com/locations/Wrightsville-Beach-North-Carolina/tides/latest']
                    ]
    for location in locationList:
        getTideForecast(location[0], location[1])