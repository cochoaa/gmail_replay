from __future__ import print_function
import html_parse
import os.path
import auth
import pprint
import base64
import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file credentials.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

labelId = os.environ['labelId']
attName = os.environ['attName']

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

def main():
    creds=auth.get_credentials("keys",SCOPES)
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

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()