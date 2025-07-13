from flask import Blueprint,current_app,render_template,request,redirect,url_for,flash
from flask_mail import Message
from exts import mail,cache,db
import random
import string
from forms.register import RegisterForm
from forms.login import LoginForm
from models.user import UserModel



"""
文件名: user
功能: 创建蓝图路由，访问路由，执行对应的视图函数
作者: cube
创建时间: 2025-07-12
"""

# 点击"发送验证码"，执行的视图函数
bp = Blueprint("user",__name__,url_prefix="/user")
@bp.route('/mail/captcha/<email>')
def mail_captcha(email):
    verification_code = ''.join(random.choices(string.digits,k=6))
    subject = '验证码'
    body = f'【query】请接收验证码:{verification_code}。如非本人操作，请忽略此信息'
    # message = Message(subject=subject,recipients=[email],body=body)
    # mail.send(message)  
    # 改用celery的方式
    current_app.celery.send_task("send_mail",(email,subject,body))
    cache.set(email,verification_code,timeout=100)
    return {"status":"success"}

@bp.route("/signup",methods=['GET','POST'])
def signup():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template("signup.html",form=form)
    else:
        # html中的name字段需要和form.   验证类中的相同
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email,username=username,password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.signin"),form=form)
        else:
            for message in form.messages:
                flash(message)
            return render_template("signup.html", form=form)
        
@bp.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template("login.html",form=form)
    else:
        if form.validate():
            return redirect(url_for("front.index"))
        else:
            for message in form.messages:
                flash(message)
            return render_template("login.html",form=form)