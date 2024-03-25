import os.path
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
EXCLUDE_LABEL = ['IMPORTANT', 'CATEGORY_FORUMS', 'CATEGORY_UPDATES', 'CATEGORY_PERSONAL', 'CATEGORY_PROMOTIONS',
                 'CATEGORY_SOCIAL', 'STARRED', 'UNREAD']

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
        return f"An error occurred: {error}"


def get_message_list():
    """
    Retrieves a list of messages from the user's Gmail inbox.

    Returns:
        A list of tuples representing email messages.
    """
    service = connect_gmail()
    if isinstance(service, str):
        # Return an error message if connection fails
        raise Exception("Failed to connect to Gmail: " + service)

    message_list = []
    labels = get_labels()
    label_names = list(labels.values())

    for label in label_names:
        if label in EXCLUDE_LABEL:
            continue
        print('Fetching messages form label: ', label)
        # Retrieve message list from Gmail API
        message_response = service.users().messages()
        results = message_response.list(userId="me", labelIds=label).execute()
        messages = results.get("messages", [])

        if not messages:
            continue

        for message in messages:
            # Retrieve full message details
            msg_dict = message_response.get(userId='me', id=message['id']).execute()
            msg_headers = msg_dict['payload']['headers']

            # Extract id from the message details
            message_id = msg_dict['id']

            # Extract read status and folder from the message details
            message_labels = msg_dict['labelIds']
            if 'UNREAD' in message_labels:
                is_read = 0  # Message is unread
            else:
                is_read = 1  # Message is read

            # Extract sender's email from message headers
            msg_from = next((hdr['value'] for hdr in msg_headers if hdr['name'] == 'From'), None)

            # Extract subject from message headers
            msg_subject = next((hdr['value'] for hdr in msg_headers if hdr['name'] == 'Subject'), None)

            # Extract date from message headers
            msg_date = next((hdr['value'] for hdr in msg_headers if hdr['name'] == 'Date'), None)
            if msg_date[3] == ',':
                if msg_date[6] == ' ':
                    msg_date = msg_date[5:24]
                else:
                    msg_date = msg_date[5:25]
            else:
                if msg_date[1] == ' ':
                    msg_date = msg_date[0:19]
                else:
                    msg_date = msg_date[0:20]
                    # Remove the timezone information (+0000) from the date string
            msg_date = re.sub(r'\s+\+\d{4}$', '', msg_date)
            # Parse the date string into a datetime object
            message_date = datetime.strptime(msg_date, "%d %b %Y %H:%M:%S")
            message_list.append((message_id, msg_from, msg_subject, message_date, is_read, label))
    return message_list


def get_labels():
    """
    Retrieves a dictionary of labels from the user's Gmail account.

    Returns:
        A dictionary mapping label names to their corresponding IDs.
    """
    # Connect to Gmail
    service = connect_gmail()

    # Check if connection was successful
    if isinstance(service, str):
        # If connection failed, raise an exception with the error message
        raise Exception("Failed to connect to Gmail: " + service)
    else:
        # If connection succeeded, proceed to fetch labels
        label_dict = {}  # Initialize an empty dictionary to store labels

        # Retrieve labels from Gmail API
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])  # Extract labels from API response

        # Check if any labels were returned
        if not labels:
            return "No labels found."  # If no labels found, return appropriate message

        # Extract label names and IDs and store them in the dictionary
        for label in labels:
            if label['id'] in EXCLUDE_LABEL:
                continue
            label_dict[label['name']] = label['id']

        return label_dict  # Return the dictionary containing labels
