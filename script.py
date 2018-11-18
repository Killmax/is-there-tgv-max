#!/usr/bin/python3

def sendEmail():
    # Send an email with the results and timestamps
    pass

def parseAndFilterTrain(fromHours, toHours):
    # Parse JSON and filter all the trains
    pass

def getAvailableTrain(fromCode, toCode, date):
    # https://www.oui.sncf/calendar/cdp/api/proposals/v3/outward/<fromCode>/<toCode>/<date>/12-HAPPY_CARD/2/fr/fr?extendedToLocality=true&fareCodes=HC16,GBNGJF1X&onlyDirectTrains=true
    pass

def main():
    # Take few args : from (RRCODE), to (RRCODE), DATE (YYYY-MM-DD - less than 30 days ahead), FROM HOURS (24h/optional), TO HOURS (24h/optional)
    pass

if __name__ == "__main__":
    main()