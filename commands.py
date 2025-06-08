from models.user import PermissionModel,RoleModel,PermissionEnum
import click
from exts import db

def welcome():
    click.echo("welcome to my world!")

def create_permission():
    # 返回PermissionEnum 类中所有属性名，一个字符串列表
    for permission_name in dir(PermissionEnum):
        if permission_name.startswith("__"):
            continue
        # getattr(PermissionEnum,permission_name) 等价于PermissionEnum.BOARD
        permission = PermissionModel(name=getattr(PermissionEnum,permission_name))
        db.session.add(permission)
    db.session.commit()
    click.echo('权限添加成功！')

def create_role():
    inspector = RoleModel(name='稽查',desc='负责审核帖子和评论是否合法合规！')
    inspector.permissions = PermissionModel.query.filter(PermissionModel.name.in_([
        PermissionEnum.POST],PermissionEnum.COMMENT)).all()
    
    operator = RoleModel(name='运营',desc='负责网站继续正常运营!')
    operator.permissions = PermissionModel.query.filter(PermissionModel.name.in_([
        PermissionEnum.POST,
        PermissionEnum.COMMENT,
        PermissionEnum.BOARD,
        PermissionEnum.FRONT_USER,
        PermissionEnum.CMS_USER
    ])).all()

    administer = RoleModel(name='管理员',desc='负责管理整个网站所有工作!')
    administer.permissions = PermissionModel.query.all()

    db.session.add_all([inspector,operator,administer])
    db.session.commit()
    click.echo('角色添加成功')


