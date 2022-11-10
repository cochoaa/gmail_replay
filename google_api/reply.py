from __future__ import print_function
import html_parse
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

# If modifying these scopes, delete the file credentials.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

labelId = os.environ['labelId']
attName = os.environ['attName']

# def filter_html(part):
#     return part.mimeType == 'text/html';

def get_registro_solicitud(parts):
    parts_filter = filter(lambda part: part.get('parts'), parts)
    parts=list(parts_filter)
    print('****************************')
    parts_body=parts[0].get('parts',[])
    #part = parts.filter(filter_html,
    parts_body_filter=filter(lambda part:part.get('mimeType') == 'text/html',parts_body)
    parts_body_html=list(parts_body_filter)
    data=list(parts_body_html)[0].get('body').get('data')
    decrypted = base64.urlsafe_b64decode(data)
    #decrypted = base64.b64decode(data).decode('ASCII')
    #print('html')
    html = decrypted.decode('utf-8')
    #print(html)
    registro=html_parse.get_registro_solicitud(html)
    return (registro)

def get_script_sql(service,msg_id:str,att_id:str):
    att = service.users().messages().attachments().get(userId='me', messageId=msg_id,id=att_id).execute()
    data = att['data']
    script = base64.b64decode(data).decode('utf-8')
    return script

def get_attachmentId(parts):
    parts_filter=filter(lambda part:part.get('filename').startswith(attName), parts)
    parts=list(parts_filter)
    part=parts[0]
    att_id = part['body']['attachmentId']
    return att_id
    # for part in parts:
    #     print('--------------------------------------------')
    #     pprint.pprint(part)
    #     if part.get('parts'):
    #         print('Tienes parts:')
    #         get_part_no_attachment(part.get('parts'))
    #     if part.get('filename').startswith(attName):
    #         print(part.get('filename'))
    #         att_id = part['body']['attachmentId']

def main():
    url_token="keys/token.json"
    url_credentials = "keys/credentials.json"
    creds = None
    # The file credentials.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(url_token):
        creds = Credentials.from_authorized_user_file(url_token, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(url_credentials, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(url_token, 'w') as token:
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
            headers = email["payload"]["headers"]
            #pprint.pprint(headers)
            subject = [i['value'] for i in headers if i["name"] == "Subject"].pop(0)
            print(type(subject))
            print(subject)
            msg_id=email.get('id')
            print(email.get('id'))
            print(email.get('labelIds'))
            print(email.get('snippet'))
            print(email.get('historyId'))
            print(email.get('internalDate'))
            # timestamp = datetime.datetime.fromtimestamp(int(email.get('internalDate')))
            # print(timestamp)
            parts=email.get('payload').get('parts',[])
            print('Size parts:'+str(len(parts)))
            datos=get_registro_solicitud(parts)
            for dato in datos:
                print(dato)
            att_id=get_attachmentId(parts)
            print('att_id:' + att_id)
            script = get_script_sql(service, msg_id, att_id)
            print('script:' + script)
            # for part in parts:
            #     print('--------------------------------------------')
            #     pprint.pprint(part)
            #     if part.get('parts'):
            #         print('Tienes parts:')
            #         get_part_no_attachment(part.get('parts'))
            #     if part.get('filename').startswith(attName):
            #         print(part.get('filename'))
            #         att_id = part['body']['attachmentId']
            #         script=get_script_sql(service,msg_id,att_id)
                    # att = service.users().messages().attachments().get(userId='me', messageId=msg_id,
                    #                                                    id=att_id).execute()
                    # data = att['data']
                    # script = base64.b64decode(data).decode('utf-8')
                    #print(script)

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