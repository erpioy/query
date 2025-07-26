from wtforms import FileField,StringField,ValidationError
from wtforms.validators import Length
from flask_wtf.file import FileAllowed
from .baseform import BaseForm

class EditProfileForm(BaseForm):
    # StringField、FileField分别对应type=text、type=file
    # name="username"表单数据会对应都名为username的验证器，自动匹配绑定
    username = StringField(validators=[Length(min=2,max=20,message="用户名太长或太短")])
    avatar = FileField(validators=[FileAllowed(['jpg','jepg','png'],message="文件类型错误")])
    signature = StringField()

    # field会自动绑定validate_...，这里是signature，绑定的是signature = StringField()
    def validate_signature(self,field):
        signature = field.data
        if signature and len(signature) > 100:
            raise ValidationError(message="签名不能超过100字符")


