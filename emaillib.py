import smtplib
import sys
import urllib2
import json

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


HOST = "localhost"
PORT = 8089
USERNAME = "admin"
PASSWORD = "changeme"


def getaddress():
	return "mwiser@splunk.com"

def getEntities (kpiid):
        import splunklib.results as results
        import splunklib.client as client
        arr = []

        # Create a Service instance and log in
        service = client.connect(
    host=HOST,
    port=PORT,
    username=USERNAME,
    password=PASSWORD)

        kwargs_oneshot = {}
        searchquery_oneshot = "search index=itsi_summary entity_title=server* kpiid="+kpiid+" |dedup entity_title|table entity_title alert_severity kpi"
        print (searchquery_oneshot)
        oneshotsearch_results = service.jobs.oneshot(searchquery_oneshot, **kwargs_oneshot)

        # Get the results and display them using the ResultsReader
        reader = results.ResultsReader(oneshotsearch_results)
        #print "Found individual events:"+str(len(reader))
        for item in reader:
                row = item.values()
                #print("Updating EventId:"+row[0])
                arr.append(row[0]+"\t\t\t "+row[1].ljust(10)+"\t\t\t "+row[2])
                
	return arr
	
def send_email(user, pwd, recipient, subject, body,serverlist):
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    for myarray in serverlist:
        for server in myarray:
            body=body+"\r\n"+server
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail" 


