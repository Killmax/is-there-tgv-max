#!/usr/bin/python3

from datetime import datetime, date
import sys
import os
import requests
import json

import sendgrid
from sendgrid.helpers.mail import *

def usage():
    print ("USAGE : " + sys.argv[0] + " <RRCODE CITY FROM (FRPAR, FRLIL, etc.)> <RRCODE CITY TO> <DATE (YYYY-mm-DD)>", file=sys.stdout)
    sys.exit(1)

def customEmailBody(results):
    dateFormatted = datetime.strptime(sys.argv[3], "%Y-%m-%d")
    body = "Hello, these are the results of your search\n\n"
    body += "At " + datetime.strftime(datetime.utcnow(), "%H:%M:%S - %d/%m/%Y") + "\n\n"
    body += "From: " + sys.argv[1] + " - " + results[0]['origin']['cityLabel'] + "\n\n"
    body += "To: " + sys.argv[2] + " - " + results[0]['dest']['cityLabel'] +"\n\n"
    body += "Date: " + datetime.strftime(dateFormatted, "%d/%m/%Y") + "\n\n"
    body += str(len(results)) + " direct train(s) found.\n\n"
    for trip in results:
        depHours = datetime.strptime(trip['departure'], "%Y-%m-%dT%H:%M")
        arrHours = datetime.strptime(trip['arrival'], "%Y-%m-%dT%H:%M")
        body += "TRAIN NUMBER " + trip['trainNumber'] + "\n\n"
        body += "FROM " + trip['origin']['label'] + " in " + trip['origin']['cityLabel']
        body += " AT " + datetime.strftime(depHours, "%H:%M") + "\n"
        body += "TO " + trip['dest']['label'] + " in " + trip['dest']['cityLabel']
        body += " AT " + datetime.strftime(arrHours, "%H:%M") + "\n\n"

    return body

def sendEmail(results):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(os.environ.get('EMAIL_FROM'))
    to_email = Email(os.environ.get('EMAIL_TO'))
    subject = "Result of your TGV MAX search"
    content = Content("text/plain", customEmailBody(results))
    mail = Mail(from_email, subject, to_email, content)
    try :
        response = sg.client.mail.send.post(request_body=mail.get())
    except:
        print("The email couldn't be sent, please check your environment and try again later.", file=sys.stderr)    
        sys.exit(1)
    print(customEmailBody(results))
    print("An email was sent to " + os.environ.get('EMAIL_TO'))
    sys.exit()

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
    sendEmail(sorted(parsedArray, key=lambda x: x['departure'], reverse=False))


def getAvailableTrain(fromCode, toCode, date):
    r = requests.get("https://www.oui.sncf/calendar/cdp/api/proposals/v3/outward/" + fromCode + "/" + toCode + "/" + date + "/12-HAPPY_CARD/2/fr/fr?extendedToLocality=true&fareCodes=HC16,GBNGJF1X&onlyDirectTrains=true")
    
    try:
        r.raise_for_status()
    except:
        print("The request failed - with code", r.status_code, file=sys.stdout)
        sys.exit(1)

    parseAndFilterTrain(r.json(), '', '')

def main():
    try:
        rrcodeFrom = sys.argv[1]
        rrcodeTo = sys.argv[2]
        datetime.strptime(sys.argv[3], "%Y-%m-%d")
    except:
        usage()

    getAvailableTrain(rrcodeFrom, rrcodeTo, sys.argv[3])

if __name__ == "__main__":
    main()