from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# OAuth 2.0 Setup
SCOPES = ['https://www.googleapis.com/auth/calendar']

flow = InstalledAppFlow.from_client_secrets_file("client_secret.json",
                                                 scopes=SCOPES)
credentials = flow.run_local_server()

pickle.dump(credentials, open("token.pkl", "wb"))
credentials = pickle.load(open("token.pkl", "rb"))
service = build("calendar", "v3", credentials=credentials)

# Get my calendars
result = service.calendarList().list().execute()
print(result['items'])

# Get all my callendar events
calendar_Id = result['items'][0]['id']
result = service.events().list(calendarId=calendar_Id).execute()
# print(result['items'])
