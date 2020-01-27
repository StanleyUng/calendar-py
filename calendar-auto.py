from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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

    service = build('calendar', 'v3', credentials=creds)

#==================================================================================================

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    print('Getting the upcoming shifts in your work schedule')
    events_result = service.events().list(
        calendarId='bf6eke2pd9t325gpqp8j49bp1k@group.calendar.google.com', 
        timeMin=now,
        maxResults=14).execute()

    events = events_result.get('items', [])

    print('Your next shift starts on ')
    today = events[0]

    start_time = parse_date(today['start'].get('dateTime'))

    print(start_time.time)

    #2020-01-25T14:15:00-08:00


    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('date', event['start'].get('date'))
    #     print(start)
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     end = event['end'].get('dateTime')
    #     print(start, end)


# Converts and ISO 8601 string to datetime object
def parse_date(d):
    return datetime.datetime.strptime(d, '%Y-%m-%dT%H:%M:%S%z')

if __name__ == '__main__':
    main()
