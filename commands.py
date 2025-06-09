from models.user import PermissionModel,RoleModel,PermissionEnum,UserModel
import click
from exts import db

def welcome():
    click.echo("welcome to my world!")

def create_permission():
    # 返回PermissionEnum 类中所有属性名，一个字符串列表
    # for permission_name in dir(PermissionEnum):
    #     if permission_name.startswith("__"):
    #         continue
        # getattr(PermissionEnum,permission_name) 等价于PermissionEnum.BOARD
        # permission = PermissionModel(name=getattr(PermissionEnum,permission_name))
    # 这里的permission是PermissionEnum.name，也就是PermissionEnum.BOARD
    for permission in PermissionEnum:
        # permission是PermissionModel类的实例对象，也就是表中的一行数据
        # 默认传入枚举对象的.value
        permission = PermissionModel(name=permission)
        db.session.add(permission)
    db.session.commit()
    click.echo('权限添加成功！')

def create_role():
    inspector = RoleModel(name='稽查',desc='负责审核帖子和评论是否合法合规！')
    operator = RoleModel(name='运营',desc='负责网站继续正常运营!')
    administer = RoleModel(name='管理员',desc='负责管理整个网站所有工作!')
    db.session.add_all([inspector,operator,administer])

    # SELECT * FROM permission WHERE name IN ('POST', 'COMMENT')
    inspector.permissions = PermissionModel.query.filter(PermissionModel.name.in_([
        PermissionEnum.POST,PermissionEnum.COMMENT])).all()
    
    operator.permissions = PermissionModel.query.filter(PermissionModel.name.in_([
        PermissionEnum.POST,
        PermissionEnum.COMMENT,
        PermissionEnum.BOARD,
        PermissionEnum.FRONT_USER,
        PermissionEnum.CMS_USER
    ])).all()

    administer.permissions = PermissionModel.query.all()

    db.session.commit()
    click.echo('角色添加成功')

# 创建测试用户
def create_test_user():
    admin_role = RoleModel.query.filter_by(name="管理员").first()
    operator_role = RoleModel.query.filter_by(name="运营").first()
    inpector_role = RoleModel.query.filter_by(name="稽查").first()
    
    zhangsan = UserModel(username="张三",email="zhangsan@query.com",password="111111",is_staff=True)

    lisi = UserModel(username="李四",email="lisi@query.com",password="111111",is_staff=True)

    wangwu = UserModel(username="王五2",email="wangwu@query.com",password="111111",is_staff=True)

    db.session.add_all([zhangsan,lisi,wangwu])
    
    zhangsan.role=admin_role
    lisi.role=operator_role
    wangwu.role=inpector_role

    db.session.commit()
    click.echo('测试用户创建成功^_^')





