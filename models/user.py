from exts import db

# User继承自db.Model  , 用操作对象的方式来写SQL语句
class User(db.Model):
    # 建表操作，相当于
    # CREATE TABLE user(
    # id INT PRIMARY KEY,
    # username VARCHAR(100),
    # passwd VARCHAR(100)
    # );
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100))
    passwd = db.Column(db.String(100))
