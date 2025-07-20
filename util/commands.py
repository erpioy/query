from models.user import PermissionModel,RoleModel,PermissionEnum,UserModel
from models.post import BoardModel,PostModel,CommentModel
import click
from exts import db
from faker import Faker
import random

def welcome():
    click.echo("welcome to my world!")

"""
    创建初始化角色与权限数据
"""
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
    zhangsan = UserModel(username="张三",email="zhangsan@query.com",password="111111",is_staff=True,role=admin_role)
    
    operator_role = RoleModel.query.filter_by(name="运营").first()
    lisi = UserModel(username="李四",email="lisi@query.com",password="111111",is_staff=True,role=operator_role)
    
    inpector_role = RoleModel.query.filter_by(name="稽查").first()
    wangwu = UserModel(username="王五2",email="wangwu@query.com",password="111111",is_staff=True,role=inpector_role)
    
    db.session.add_all([zhangsan,lisi,wangwu])
    db.session.commit()
    click.echo('测试用户创建成功^_^')

@click.option("--username",'-u')
@click.option("--email",'-e')
@click.option("--password",'-p')
def create_admin(username,email,password):
    admin_role = RoleModel.query.filter_by(name="管理员").first()
    admin_user = UserModel(username=username,email=email,password=password,is_staff=True,role=admin_role)
    db.session.add(admin_user)
    db.session.commit()
    click.echo("管理员创建成功^_^")

"""
    创建帖子板块的初始数据
"""

def create_board():
    boards_name = ['电影','诗词','歌词','文章']
    for name in boards_name:
        board = BoardModel(name=name)
        db.session.add(board)
    db.session.commit()
    click.echo('分类板块创建成功')


"""
    通过faker库，添加测试数据
"""

def create_test_post():
    faker = Faker(locale="zh_CN")
    author = UserModel.query.first()
    boards = BoardModel.query.all()

    click.echo("开始生成测试帖子...")

    for x in range(98):
        title = faker.sentence()
        content = faker.paragraph(nb_sentences=10)
        random_index = random.randint(0,3)
        board = boards[random_index]
        post = PostModel(title=title,content=content,board=board,author=author)
        db.session.add(post)
    db.session.commit()
    click.echo("测试帖子生成成功")






