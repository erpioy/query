from flask import Blueprint,current_app,render_template,request,redirect,url_for,flash,g,session
from flask_mail import Message
from exts import mail,cache,db
import random
import string
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.user import EditProfileForm
from models.user import UserModel
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
from flask import send_from_directory
from util.decorators import login_required
import os



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
        
@bp.route('/profile/<string:user_id>')
def profile(user_id):
    form = EditProfileForm()
    user = UserModel.query.get(user_id)
    print(g.user.avatar)
    is_mine = False
    if hasattr(g,"user") and g.user.id == user_id:
        is_mine = True

    context = {
        "user": user,
        "is_mine": is_mine,
        "form": form
    }
    
    return render_template("front/profile.html",**context)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@bp.route('/profile/edit',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(CombinedMultiDict([request.form,request.files]))
    if form.validate_on_submit():
        username = form.username.data
        avatar = form.avatar.data
        signature =  form.signature.data
        
        #如果上传了头像
        if avatar:
            # 生成安全的文件名
            filename = secure_filename(avatar.filename)
            # 拼接头像存储路径
            avatar_path = os.path.join(current_app.config.get("AVATARS_SAVE_PATH"),filename)
            # 保存文件
            avatar.save(avatar_path)
            #设置头像的URL
            #g.user.avatar = url_for("media.media_file",filename=os.path.join("avatars",filename))
            g.user.avatar = url_for('static', filename=f'avatars/{filename}')
        g.user.username = username
        g.user.signature = signature
        db.session.commit()
        return redirect(url_for("user.profile",user_id=g.user.id))
    else:
        for message in form.messages:
            flash(message)
        return redirect(url_for("user.profile",user_id=g.user.id))



