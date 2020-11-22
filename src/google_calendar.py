#!/usr/bin/env python3

''' Google Calendar Class to get list of
    events within a calendar and set new events '''

import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class GoogleCalendar:
    ''' Google Calendar Class '''

    def __init__(self):

        # Define attributes
        self.calendar_list = []
        self.event_list = []

        # Init credentials
        self.get_credentials()

    def get_credentials(self):
        '''Get Google Calendar credentials. The file token.pickle stores
         the user's access and refresh tokens, and is
         created automatically when the authorization flow completes for the first
         time. '''

        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)

    def get_calendars(self):
        ''' Get list of calendars '''

        calendars_result = self.service.calendarList().list().execute()
        calendars = calendars_result.get('items', [])

        if not calendars:
            print('No avaiable calendars')
        for calendar_item in calendars:
            self.calendar_list.append(calendar_item)


    def get_events(self,
                   calendar_name = 'primary',
                   limit = 10):
        ''' Get list of events into calendar '''
        now = datetime.datetime.utcnow().isoformat() + 'Z'

        if calendar_name != 'primary':
            # Retrieve list of calendars
            self.get_calendars()

            # Check calendar by calendar
            for calendar_item in self.calendar_list:

                # Extract events from desired calendar
                if calendar_item['summary'] == calendar_name:
                    calendar_id = calendar_item['id']
                    events_result = self.service.events().list(calendarId=calendar_id,
                                                                timeMin=now,
                                                                maxResults=limit,
                                                                singleEvents=True,
                                                                orderBy='startTime').execute()
                    events = events_result.get('items', [])
                    if not events:
                        print('No upcoming events found!')
                    for event in events:
                        print(event['summary'])
                    break
        else:
            events_result = self.service.events().list(calendarId='primary',
                                                                timeMin=now,
                                                                maxResults=limit,
                                                                singleEvents=True,
                                                                orderBy='startTime').execute()
            events = events_result.get('items', [])
            if not events:
                print('No upcoming events found!')
            for event in events:
                self.event_list.append(event['summary'])

if __name__ == '__main__':

    # Init calendar instance
    calendar = GoogleCalendar()

    # Get list of calendars
    calendar.get_calendars()
    for calendar_element in calendar.calendar_list:
        print(calendar_element['summary'])

    # List events into primary calendar
    calendar.get_events()
    for item in calendar.event_list:
        print(item)
