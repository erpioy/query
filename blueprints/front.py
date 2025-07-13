from flask import Blueprint,render_template
from models.post import BoardModel,PostModel,CommentModel

bp = Blueprint("front",__name__,url_prefix="")

@bp.route('/')
def index():
    return render_template("index.html")