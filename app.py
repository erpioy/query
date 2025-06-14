from flask import Flask,render_template
from exts import db,mail,cache
import config
from blueprints.cms import bp as cms_bp
from blueprints.front import bp as front_bp
from blueprints.user import bp as user_bp
from flask_migrate import Migrate
from models import user
import commands
from my_celery import make_celery

app = Flask(__name__)
# 用于加载config模块
app.config.from_object(config)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:830849@localhost/myquery"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
mail.init_app(app)
cache.init_app(app)

# 构建celery
celery = make_celery(app)

migrate = Migrate(app,db)
# 注册蓝图
app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)
app.register_blueprint(user_bp)

# 添加命令
app.cli.command("create-permission")(commands.create_permission)
app.cli.command("create-role")(commands.create_role)
app.cli.command("create-test-user")(commands.create_test_user)
app.cli.command("create-admin")(commands.create_admin)

with app.app_context():
    #db.drop_all()
    db.create_all()

@app.route('/signup')
def signup_page():
    return render_template("signup.html")



if __name__ == '__main__':
    app.run(debug=True)