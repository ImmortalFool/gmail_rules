import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def connect_gmail():
    """
    Lists the user's Gmail messages.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        return service
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        return f"An error occurred: {error}"


def get_message_list(service):
    """
    Retrieves a list of messages from the user's Gmail inbox.
    """
    message_response = service.users().messages()
    results = message_response.list(userId="me", labelIds=["INBOX"]).execute()
    messages = results.get("messages", [])
    if not messages:
        return "No messages found."
    for message in messages:
        msg_dict = message_response.get(userId='me', id=message['id']).execute()
        msg_headers = msg_dict['payload']['headers']

        # get from email from email message header
        msg_from = filter(lambda hdr: hdr['name'] == 'From', msg_headers)
        msg_from = list(msg_from)[0].get('value')
        print(msg_from)

        # get subject from email message header
        msg_subject = filter(lambda hdr: hdr['name'] == 'Subject', msg_headers)
        msg_subject = list(msg_subject)[0]
        print(msg_subject.get('value'))

        # get date from email message header
        msg_date = filter(lambda hdr: hdr['name'] == 'Date', msg_headers)
        msg_date = list(msg_date)[0]
        print(msg_date.get('value'))


def get_labels(service):
    """
    Retrieves a dictionary of labels from the user's Gmail account.
    """
    label_dict = {}
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])
    if not labels:
        return "No labels found."
    for label in labels:
        label_dict[label['name']] = label['id']
    print(label_dict)


def fetch_message_labels():
    service = connect_gmail()
    if isinstance(service, str):
        print(service)
    else:
        message_list = get_message_list(service)
        labels = get_labels(service)


fetch_message_labels()