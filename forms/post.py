from .baseform import BaseForm
from wtforms import StringField,IntegerField
from wtforms.validators import InputRequired,Length

class PublicPostForm(BaseForm):
    title = StringField(validators=[Length(min=2,max=30,message="请输入正确长度的标题")])
    content = StringField(validators=[Length(min=2,message="输入内容过短")])
    board_id = IntegerField(validators=[InputRequired(message="请输入板块id")])