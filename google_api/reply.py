import html_parse
import os.path
import auth
import read_mail
import base64
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file credentials.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.modify']

def main():
    creds=auth.get_credentials("keys",SCOPES)
    mails=read_mail.get_mails(creds)

    for mail in mails:
        read_mail.mark_as_read(creds,mail.msgid)

if __name__ == '__main__':
    main()