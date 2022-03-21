from app import app, mail
import os
from flask_mail import Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')


def send_mail():
    msg=Message('test email',recipients='jnance1979@gmail.com',body='testing e-mail.')
    print('testing')
    mail.send(msg)

