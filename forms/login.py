from flask import session
from wtforms import StringField,ValidationError,PasswordField
from wtforms.validators import DataRequired
from models.user import UserModel
from werkzeug.security import check_password_hash
from .baseform import BaseForm

    # 验证用户名和密码是否匹配一致
class LoginForm(BaseForm):
    username = StringField("用户名", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired()])
    def validate_username(self,field):
        username = self.username.data
        password = self.password.data

        user = UserModel.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
        else:
            raise ValidationError(message="用户名或密码错误！") 
        
            
        
