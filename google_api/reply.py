from __future__ import print_function

import os.path
import pprint
import base64
import io
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

labelId = os.environ['labelId']
attName = os.environ['attName']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        print(str(service))
        # result = service.users().labels().list(userId='me').execute()
        # for label in result.get('labels'):
        #     print(label)
        results = service.users().messages().list(userId='me',maxResults=10,labelIds=['INBOX','UNREAD',labelId]).execute()
        print(labelId)
        messages = results.get('messages', [])
        nextPageToken = results.get('nextPageToken','')
        resultSizeEstimate = results.get('resultSizeEstimate','')
        print('Cantidad de resultados: '+str(resultSizeEstimate))
        for m in messages:
            #print(m)
            email = service.users().messages().get(userId='me',id=m.get('id')).execute()
            #pprint.pprint(email)
            msg_id=email.get('id')
            print(email.get('id'))
            print(email.get('labelIds'))
            print(email.get('snippet'))
            print(email.get('historyId'))
            print(email.get('internalDate'))
            # timestamp = datetime.datetime.fromtimestamp(int(email.get('internalDate')))
            # print(timestamp)
            for part in email.get('payload').get('parts',[]):
                #print(part)
                if part.get('filename').startswith(attName):
                    pprint.pprint(part)
                    print(part.get('filename'))
                    att_id = part['body']['attachmentId']
                    att = service.users().messages().attachments().get(userId='me', messageId=msg_id,
                                                                       id=att_id).execute()
                    data = att['data']
                    decrypted = base64.b64decode(data).decode('utf-8')
                    print(type(decrypted))
                    print(decrypted)

        # if not labels:
        #     print('No labels found.')
        #     return
        # print('messages:')
        # for label in labels:
        #     print(label['name'])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()