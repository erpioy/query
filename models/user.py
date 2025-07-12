from exts import db
from enum import Enum
from datetime import datetime
from shortuuid import uuid
from werkzeug.security import generate_password_hash,check_password_hash

"""
功能：创建表模型
"""

class PermissionEnum(Enum):
    # 推荐枚举变量名，写成大写
    BOARD = "板块"
    POST = "帖子"
    COMMENT = "评论"
    FRONT_USER = "前台用户"
    CMS_USER = "后台用户"

# 创建一个permission表（id，name）
class PermissionModel(db.Model):
    __tablename__ = "permission"
    id = db.Column(db.Integer,primary_key=True)
    # 限制该字段只能存储PermissionEnum中定义的枚举值
    name = db.Column(db.Enum(PermissionEnum),nullable=False,unique=True)

# 创建一个中间关系，通过外键建立关系
# SQLAlchemy 会自动处理表的创建顺序，保证父表先被创建,关联表
role_permission_table = db.Table(
    "role_permission_table",
    db.Column("role_id",db.Integer,db.ForeignKey("role.id")),
    db.Column("permission_id",db.Integer,db.ForeignKey("permission.id"))
)

# 创建一个role表（id，name，desc，create_time）
class RoleModel(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    desc = db.Column(db.String(200),nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now) 

    # 通过中间表来建立多对多关系，并在PermissionModel类中自动创建roles属性
    permissions = db.relationship("PermissionModel",secondary=role_permission_table,backref="roles")
    users = db.relationship("UserModel",back_populates="role")

# 创建一个user表
# 把函数传进去，插入时自动调用,每条记录生成一个新的ID  如果使用uuid()，会立即执行函数，所有记录用同一个ID
class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.String(100),primary_key=True,default=uuid)
    username = db.Column(db.String(50),nullable=False,unique=True)
    # password = db.Column(db.String(200),nullable=False)  修改为：
    _password = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(50),nullable=False,unique=True)
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    join_time = db.Column(db.DateTime,default=datetime.now)
    is_staff = db.Column(db.Boolean,default=False)
    is_active = db.Column(db.Boolean,default=True)

    # 外键
    role_id = db.Column(db.Integer,db.ForeignKey("role.id"))
    # ForeignKey是relationship的基础，relationship必须依赖外键列才能正常工作
    # 如果这样定义的话，自动在 RoleModel 类中创建反向属性 users，能够使RoleModel类的实例通过“.users”属性访问到绑定了该角色的用户，以列表的形式返回
    # role = db.relationship("RoleModel",backref="users")
    role = db.relationship("RoleModel",back_populates="users")

    # *args 元组，**kwargs 字典。args变为一个元组，kwargs变为一个字典
    def __init__(self,*args,**kwargs):
        if "password" in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop("password")
        super(UserModel,self).__init__(*args,**kwargs)

    # 将这个函数包装成一个属性对象,把方法伪装成属性，标记为读
    @property
    def password(self):
        return self._password
    # 当这个属性被调用时，自动执行这段函数，标记为写
    @password.setter
    def password(self,raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self,raw_password):
        result = check_password_hash(self.password,raw_password)
        return result
    

