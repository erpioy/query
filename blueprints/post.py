from flask import Blueprint,render_template,request,g,flash,redirect,url_for
from models.post import BoardModel,PostModel,CommentModel
from util.decorators import login_required
from forms.post import PublicPostForm,CommentForm
from exts import db
from util import restful

bp = Blueprint("post",__name__,url_prefix="/post")

@bp.route('/public',methods=['GET','POST'])
# 添加装饰器，需要先登录才能发布帖子
@login_required
def public():
    form = PublicPostForm()
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template("front/public_post.html",boards=boards,form=form)
    else: 
        data = request.get_json()
        form = PublicPostForm(data=data)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data

            print(title,content,board_id)

            post = PostModel(title=title,content=content,board_id=board_id,author=g.user)
            db.session.add(post)
            db.session.commit()
            return restful.ok()
        else:
            message = form.messages[0]
            return restful.params_error(message=message)

@bp.route('/detail/<int:post_id>')
def post_detail(post_id):
    form=CommentForm()
    post = PostModel.query.get(post_id)
    post.read_count += 1
    db.session.commit()

    return render_template("front/post_detail.html",post=post,form=form)

@bp.route('/<int:post_id>/comment',methods=['POST'])
@login_required
def post_comment(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        # 获取前端属性为“content”标签中的内容
        content = form.content.data
        comment = CommentModel(content=content,post_id=post_id,author=g.user)
        db.session.add(comment)
        db.session.commit()
    else:
        for message in form.messages:
            flash(message)
    return redirect(url_for('post.post_detail',post_id=post_id))






