import smtplib
from email.mime.text import MIMEText
from config import smtp, frontend

def send_verify_mail(token, user):
    mail = smtplib.SMTP(smtp['host'], smtp['port'])
    mail.starttls()
    mail.login(smtp['email'], smtp['password'])

    msg = MIMEText('Verification Link: {}/{}'.format(frontend, token))
    msg['Subject'] = '[DongariBang] 메일 인증'
    msg['To'] = user.email

    mail.sendmail(smtp['email'], user.email, msg.as_string())
    
