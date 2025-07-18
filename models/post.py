from exts import db
from datetime import datetime

# 板块模型，只需要在创建板块时给出板块的名称
class BoardModel(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(20),nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    is_active = db.Column(db.Boolean,default=True)

# 帖子模型
class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(30),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    read_count = db.Column(db.Integer,default=0)
    is_active = db.Column(db.Boolean,default=True)
    board_id = db.Column(db.Integer,db.ForeignKey("board.id"))
    author_id = db.Column(db.String(100),db.ForeignKey("user.id"),nullable=False)
    
    # 建立联系
    board = db.relationship("BoardModel",backref="posts")
    author = db.relationship("UserModel",backref="posts")

# 评论模型
class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    is_active = db.Column(db.Boolean,default=True)
    post_id = db.Column(db.Integer,db.ForeignKey("post.id"))
    author_id = db.Column(db.String(100),db.ForeignKey("user.id"),nullable=False)

    # 建立联系
    post = db.relationship("PostModel",backref="comments")
    author = db.relationship("UserModel",backref="comments")


