from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
import os.path
import base64
import re
#from __future__ import print_function
from pprint import pprint
import html_parse
from models import MailScript

labelId = os.environ['labelId']
attName = os.environ['attName']

def __get_registro_solicitud(parts):
    parts_filter = filter(lambda part: part.get('parts'), parts)
    parts=list(parts_filter)
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

def __get_script_sql(service,msg_id:str,att_id:str):
    try:
        att = service.users().messages().attachments().get(userId='me', messageId=msg_id,id=att_id).execute()
        data = att['data']
        script = base64.b64decode(data).decode('utf-8')
        return script
    except:
        return ''
def __get_attachmentId(parts):
    try:
        parts_filter=filter(lambda part:part.get('filename').startswith(attName), parts)
        parts=list(parts_filter)
        part=parts[0]
        att_id = part['body']['attachmentId']
        return att_id
    except:
        return ''

def __extract_email(mail_from:str):
    pattern='(?:"?([^"]*)"?\s)?(?:<?(.+@[^>]+)>?)';
    match=re.search(pattern, mail_from)
    return match.group(2)

def __get_mail(msg_id,service):
    email = service.users().messages().get(userId='me', id=msg_id).execute()
    # pprint.pprint(email)
    headers = email["payload"]["headers"]
    #pprint.pprint(email)
    subject = [i['value'] for i in headers if i["name"] == "Subject"].pop(0)
    sender = [i['value'] for i in headers if i["name"] == "From"].pop(0)
    sender = __extract_email(sender)
    historyId=email.get('historyId')
    print(f'El history_id del mensaje: {historyId}')
    timestamp = datetime.datetime.fromtimestamp(int(email.get('internalDate'))/1000)
    parts = email.get('payload').get('parts', [])
    print('Size parts:' + str(len(parts)))
    datos = __get_registro_solicitud(parts)
    area = datos[0]
    solicitante = datos[1]
    dependencia = datos[2]
    motivo = datos[3]
    att_id = __get_attachmentId(parts)
    script = __get_script_sql(service, msg_id, att_id)
    return MailScript(timestamp,msg_id,subject,sender,area,solicitante,dependencia,motivo,script)

def get_mails(credentials):
    mails=[]
    try:
        service = build('gmail', 'v1', credentials=credentials)
        print(str(service))
        results = service.users().messages().list(userId='me', maxResults=10,
                                                  labelIds=['INBOX', 'UNREAD', labelId]).execute()
        messages = results.get('messages', [])
        resultSizeEstimate = results.get('resultSizeEstimate', '')
        print('Cantidad de resultados: ' + str(resultSizeEstimate))
        for m in messages:
            msg_id = m.get('id')
            thread_id = m.get('threadId')
            print(f'El id del mensaje: {msg_id}')
            print(f'El thread_id del mensaje: {thread_id}')

            mail=__get_mail(msg_id, service)
            mails.append(mail)

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

    return mails

def mark_as_read(credentials, msg_id):
    try:
        service = build('gmail', 'v1', credentials=credentials)
        service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')