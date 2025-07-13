from flask import Blueprint,render_template,request
from models.post import BoardModel,PostModel,CommentModel

bp = Blueprint("post",__name__,url_prefix="/post")

@bp.route('/public',methods=['GET','POST'])
def public():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template("front/public_post.html",boards=boards)
    else:
        pass