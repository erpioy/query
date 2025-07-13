from wtforms import StringField,ValidationError
from wtforms.validators import Email,EqualTo,Length
from exts import cache
from models.user import UserModel
from .baseform import BaseForm


# 表单验证类
class RegisterForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确的邮箱格式!")])
    captcha = StringField(validators=[Length(min=6,max=6,message="请输入正确格式的验证码!")])
    username = StringField(validators=[Length(min=2,max=10,message="用户名太长或太短!")])
    password = StringField(validators=[Length(min=6,max=16,message="请输入正确长度的密码")])
    confirm_password = StringField(validators=[EqualTo("password",message="两次密码不一致!")])

    # 在 Flask-WTF/WTForms 中，validate_ 前缀 + 字段名 的方法会被自动调用
    # field参数会自动绑定对应的字段
    def validate_email(self,field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise ValidationError(message="邮箱已经存在~")
    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        cache_captcha = cache.get(email)
        if not cache_captcha or captcha != cache_captcha:
            raise ValidationError(message="验证码错误~")
