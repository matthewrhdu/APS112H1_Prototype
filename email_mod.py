import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def email(i, gmailUser, gmailPassword, recipients, second_warning):
    if not second_warning:
        message = "Warning, unit " + str(i + 1) + " has gone under the threshold for safe air exchange."
        msg = MIMEMultipart()
        msg['From'] = f'"Team 144" <{gmailUser}>'
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = "Riverdale Air Exchange Warning"
        msg.attach(MIMEText(message))
    else:
        message = "URGENT, unit " + str(i + 1) + " has gone under the threshold for safe air exchange for " \
                                                 "over 10 minutes."
        msg = MIMEMultipart()
        msg['From'] = f'"Team 144" <{gmailUser}>'
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = "Riverdale Air Exchange URGENT Warning"
        msg.attach(MIMEText(message))

    try:
        mail_server = smtplib.SMTP('smtp.gmail.com', 587)
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.ehlo()
        mail_server.login(gmailUser, gmailPassword)
        mail_server.sendmail(gmailUser, recipients, msg.as_string())
        mail_server.close()
        print('Email sent!')
    except Exception:
        print('Something went wrong...')

    exit(1)