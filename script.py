#!/usr/bin/python3

from datetime import datetime
import sys
import requests
import json

def usage():
    print ("USAGE : " + sys.argv[0] + " <RRCODE CITY FROM (FRPAR, FRLIL, etc.)> <RRCODE CITY TO> <DATE YYYY-mm-DD>", file=sys.stdout)
    sys.exit(1)

def sendEmail():
    # Send an email with the results and timestamps
    pass

def parseAndFilterTrain(jsonPayload, fromHours, toHours):
    # Parse JSON and filter all the trains
    parsedArray = []
    for trip in jsonPayload:
        filteredTrip = {}
        filteredTrip['departure'] = trip['departureDate']
        filteredTrip['arrival'] = trip['arrivalDate']
        filteredTrip['origin'] = trip['segments'][0]['origin']
        filteredTrip['dest'] = trip['segments'][0]['destination']
        filteredTrip['trainNumber'] = trip['segments'][0]['trainNumber']
        parsedArray.append(filteredTrip)
        print(filteredTrip)



def getAvailableTrain(fromCode, toCode, date):
    r = requests.get("https://www.oui.sncf/calendar/cdp/api/proposals/v3/outward/" + fromCode + "/" + toCode + "/" + date + "/12-HAPPY_CARD/2/fr/fr?extendedToLocality=true&fareCodes=HC16,GBNGJF1X&onlyDirectTrains=true")
    
    try:
        r.raise_for_status()
    except:
        print("The request failed - with code %d", r.status_code, file=sys.stdout)
        sys.exit(1)

    parseAndFilterTrain(r.json(), '', '')

def main():
    # Take few args : from (RRCODE), to (RRCODE), DATE (YYYY-MM-DD - less than 30 days ahead), FROM HOURS (24h/optional), TO HOURS (24h/optional)
    try:
        rrcodeFrom = sys.argv[1]
        rrcodeTo = sys.argv[2]
        tripDate = datetime.strptime(sys.argv[3], "%Y-%m-%d")
    except:
        usage()

    print(rrcodeFrom)
    print(rrcodeTo)
    print(tripDate)

    getAvailableTrain(rrcodeFrom, rrcodeTo, sys.argv[3])

if __name__ == "__main__":
    main()