from flask import Flask,render_template
from exts import db
import config
from blueprints.cms import bp as cms_bp
from blueprints.front import bp as front_bp
from blueprints.user import bp as user_bp
from flask_migrate import Migrate
from models import user
import click

app = Flask(__name__)
app.config.from_object(config)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:830849@localhost/myquery"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app,db)
# 注册蓝图
app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)
app.register_blueprint(user_bp)

with app.app_context():
    db.create_all()

@app.route('/signup')
def signup_page():
    return render_template("signup.html")

@app.cli.command("my-command")
def my():
    click.echo("welcome to my world")

if __name__ == '__main__':
    app.run(debug=True)