import email, os, smtplib
import email.encoders
import email.mime.base
import email.mime.multipart
import email.header
import magic
from email.mime.text import MIMEText
from saillog import logger

# return MIME multipart object
def get_message(message_subject, message_body, message_attachment, sender, receiver):
  message = email.mime.multipart.MIMEMultipart()

  # declare charset and various headers, attach message body to MIME object
  message.set_charset('utf-8')
  message['Subject'] = email.header.Header(message_subject)
  message['From'] = email.header.Header(sender)
  message['To'] = email.header.Header(receiver)
  message['Message-ID'] = email.header.Header(email.utils.make_msgid())
  message.attach(email.mime.text.MIMEText(message_body, 'plain'))

  # # detect attachment filetypes
  m = magic.from_file(message_attachment, mime=True) 
  maintype, subtype = m.split('/')
  part = email.mime.base.MIMEBase(maintype, subtype)

  # encode attachment, attach to MIME object
  part.set_payload(open(message_attachment, 'rb').read())
  email.encoders.encode_base64(part)
  part.add_header('Content-disposition', 'attachment; filename={}'.format(os.path.basename(message_attachment)))
  message.attach(part)
  
  return message

# login to mail, send
@logger
def send_mail(server, sender, receiver, pwd, message):
  
  # context manager
  with smtplib.SMTP_SSL(server) as s:
    s.login(sender, pwd)
    s.sendmail(sender, receiver, message.as_string())