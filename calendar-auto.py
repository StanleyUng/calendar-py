from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from shift import Shift

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar/readonly']

calendar_type = {
    'main': 'primary',
    'target': '   '
}

MAX_RESULTS = 14

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

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

#==================================================================================================
    print('Getting the upcoming shifts in your work schedule')
    events_result = service.events().list(
        calendarId=calendar_type['target'], 
        timeMin=now,
        maxResults=MAX_RESULTS).execute()

    shifts = events_result.get('items', [])

    schedule = []

    if not shifts:
        print('No upcoming shifts')
    for shift in shifts:
        start_time = parse_date(shift['start'].get('dateTime'))
        end_time = parse_date(shift['end'].get('dateTime'))

        day = datetime.date(start_time.year, start_time.month, start_time.day)
        time_in = datetime.time(start_time.hour, start_time.minute, start_time.second)
        time_out = datetime.time(end_time.hour, end_time.minute, end_time.second)

        s = Shift(day, time_in, time_out)
        schedule.append(s)

        print(s.get_shift(), s.get_hours())
        # print(s.calculate_pay())
#==================================================================================================

# Converts and ISO 8601 string to datetime object
# '%Y-%m-%dT%H:%M:%S%z'
# 2020-01-25T14:15:00-08:00
def parse_date(d):
    return datetime.datetime.strptime(d, '%Y-%m-%dT%H:%M:%S%z')

if __name__ == '__main__':
    main()