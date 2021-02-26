from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import base64
import os
import re
import csv


from apiclient import errors

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']


def get_read_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('read_token.pickle'):
        with open('read_token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                {"installed":{"client_id":"917643248270-ct8tp8os55ggcu4a35bnkd6s57jiojl4.apps.googleusercontent.com","project_id":"gmail-api-2-1604251313883","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"VVkxOcF2DbACM4fJadj-PKTR","redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]}}, ['https://www.googleapis.com/auth/gmail.readonly'])
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('read_token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def get_send_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('send_token.pickle'):
        with open('send_token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                {"installed":{"client_id":"917643248270-ct8tp8os55ggcu4a35bnkd6s57jiojl4.apps.googleusercontent.com","project_id":"gmail-api-2-1604251313883","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"VVkxOcF2DbACM4fJadj-PKTR","redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]}}, ['https://www.googleapis.com/auth/gmail.send'])
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('send_token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


read_service = get_read_service()
send_service = get_send_service()


def resend_message(id, email, name):
    s = read_service.users().messages().get(userId='me', id=id, format='raw').execute()['raw']
    s = base64.urlsafe_b64decode(s).decode('utf-8')
    subject = re.search(r'\nsubject:\s+[\s\S]*?\n', s, re.I).group(0)
    s = s[s.find('\nContent-Type'):].strip()
    h = f'''
MIME-Version: 1.0
to: {email}
from: CISxIdeas Hackathon <hackathon@cis.edu.hk>{subject}
    '''
    s = s[:s.find('\n')] + h + s[s.find('\n'):]
    s = s.replace('{{name}}', name)
    d = {'raw': base64.b64encode(s.encode('utf-8')).decode('ascii')}
    send_service.users().messages().send(userId='me', body=d).execute()


def get_lastest_message_id():
    return read_service.users().messages().list(userId='me').execute()['messages'][0]['id']


def test_send_message(email):
    mid = get_lastest_message_id()
    resend_message(mid, email, 'Tester')
    return mid


def send_all(eid):
    with open('participants.csv') as f:
        sheet = csv.reader(f)
        for row in sheet:
            name = row[2].strip()
            email = row[4].strip()
            resend_message(eid, email, name)



if __name__ == '__main__':
    id = get_lastest_message_id()
    s = read_service.users().messages().get(userId='me', id=id, format='raw').execute()['raw']
    s = base64.urlsafe_b64decode(s).decode('utf-8')
    print(s)
# resend_message('175b7df45934b4d4', 'deyaoc2021@student.cis.edu.hk')
#     # s = json.dumps(service.users().messages().get(userId='me', id='175b81e222784374').execute()['payload'])
#     s = read_service.users().messages().get(userId='me', id='175b7df45934b4d4', format='raw').execute()['raw']
#     s = base64.urlsafe_b64decode(s).decode('utf-8')
#     subject = re.search(r'\nsubject:\s+[\s\S]*?\n', s, re.I).group(0)
#     s = s[s.find('\nContent-Type'):].strip()
#     email = 'deyaoc2021@student.cis.edu.hk'
#     print(subject)
#     h = f'''
# MIME-Version: 1.0
# to: {email}
# from: CISxIdeas Hackathon <hackathon@cis.edu.hk>{subject}
# '''
#     s = s[:s.find('\n')] + h + s[s.find('\n'):]
#     print(s)
#     # print(s)
#     # part1 = MIMEText('hello', 'html')
#     # message.attach(s)
#     # print(message.as_string())
#     d =  {'raw': base64.b64encode(s.encode('utf-8')).decode('ascii')}
#     send_service.users().messages().send(userId='me', body=d).execute()
#     # .execute()