import os
import json
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.auth.transport.requests import Request

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'
CLIENT_SECRETS_FILE = 'credentials.json'

def get_credentials():
    credentials = None
    token_path = 'token.json'

    if os.path.exists(token_path):
        with open(token_path, 'r') as token:
            credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(json.load(token), SCOPES)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)

        with open(token_path, 'w') as token:
            token.write(credentials.to_json())

    return credentials

def get_calendar_service():
    credentials = get_credentials()
    service = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    return service

def list_events():
    service = get_calendar_service()
    events_result = service.events().list(calendarId='primary', maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events
