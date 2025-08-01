from flask import Flask
from flask_wtf.csrf import CSRFProtect
from exts import db,mail,cache,avatars
import config
from blueprints.cms import bp as cms_bp
from blueprints.front import bp as front_bp
from blueprints.user import bp as user_bp
from blueprints.post import bp as post_bp
from blueprints.media import bp as media_bp
from flask_migrate import Migrate
import util.commands as commands
from util.my_celery import make_celery
from util.hooks import before_request
from util.filters import email_hash
import os

app = Flask(__name__)

# 用于加载config模块中的配置信息（大写字母）
app.config.from_object(config)
app.config['AVATARS_SAVE_PATH'] = os.path.join(
    app.root_path,  # 项目根目录（自动适应项目位置）
    'static', 
    'avatars'
)

csrf = CSRFProtect(app)

db.init_app(app)
mail.init_app(app)
cache.init_app(app)
avatars.init_app(app)

# 构建celery
celery = make_celery(app)

migrate = Migrate(app,db)
# 注册蓝图
app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)
app.register_blueprint(user_bp)
app.register_blueprint(post_bp)
app.register_blueprint(media_bp)

# 添加命令 app.cli.command("命令")(执行函数)
app.cli.command("create-permission")(commands.create_permission)
app.cli.command("create-role")(commands.create_role)
app.cli.command("create-test-user")(commands.create_test_user)
app.cli.command("create-admin")(commands.create_admin)

app.cli.command("create-board")(commands.create_board)

app.cli.command("create-test-post")(commands.create_test_post)
# 添加钩子函数，用于验证用户是否登录
app.before_request(before_request)

app.template_filter("email_hash")(email_hash)
# with app.app_context():
    # db.drop_all()
    # db.create_all()
   
if __name__ == '__main__':
    app.run(debug=True)
    