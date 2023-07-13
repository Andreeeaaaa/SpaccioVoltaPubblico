import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from DjangoWebApp.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

def send_message(indirizzo, oggetto, messaggio):
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = EMAIL_HOST_USER
    message['To'] = indirizzo
    message['Subject'] = oggetto   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(messaggio, 'plain'))

    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD) #login with mail_id and password
    text = message.as_string()
    session.sendmail(EMAIL_HOST_USER, indirizzo, text)
    session.quit()
