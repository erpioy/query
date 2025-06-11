from flask import Blueprint
from flask_mail import Message
from exts import mail
import random
import string

bp = Blueprint("user",__name__,url_prefix="/user")
@bp.route('/mail/captcha/<email>')
def mail_captcha(email):
    verification_code = ''.join(random.choices(string.digits,k=6))
    subject = '验证码'
    body = f'【query】请接收验证码:{verification_code}。如非本人操作，请忽略此信息'
    message = Message(subject=subject,recipients=[email],body=body)
    mail.send(message)
    return "success"