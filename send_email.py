import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import datetime

from config import *


def send_email(fromaddr, pwd, toaddr, host, port, subject, body, Cc='', attachment=False, filename='', filepath=''):
    '''
    send email via gmail SMTP and add one attachment file
    TODO: embed image in body of the email
    https://stackoverflow.com/questions/920910/sending-multipart-html-emails-which-contain-embedded-images
    '''
    
    # instance of MIMEMultipart 
    msg = MIMEMultipart() 
    msg['From'] = fromaddr 
    msg['To'] = toaddr 
    if Cc != '':
        msg['Cc'] = Cc
    msg['Subject'] = subject
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 
    
    if attachment:
        # instance of MIMEBase and named as p 
        p = MIMEBase('application', 'octet-stream') 
        p.set_payload(open(filepath, "rb").read()) 
        encoders.encode_base64(p) 
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
        msg.attach(p) 

    # creates SMTP session 
    s = smtplib.SMTP(host, port) 
    # start TLS for security 
    s.starttls() 
    # Authentication 
    s.login(fromaddr, pwd) 

    # Converts the Multipart msg into a string 
    text = msg.as_string() 
    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 
    print('Email sent')

    # terminating the session 
    s.quit()

def main():
    
    send_email(fromaddr, pwd, toaddr, host, port, subject, body, Cc=Cc, attachment=True, filename=filename, filepath=filepath)
    print('execution finished :)')


if __name__ == '__main__':
	main()
