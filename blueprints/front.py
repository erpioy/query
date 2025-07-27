from flask import Blueprint,render_template,request,current_app
from models.post import BoardModel,PostModel,CommentModel
from flask_paginate import Pagination

bp = Blueprint("front",__name__,url_prefix="")

@bp.route('/')
def index():
    posts = PostModel.query.all()
    boards = BoardModel.query.all()

    # 通过查询传参得到，当前页数，在url中
    page = request.args.get("page",type=int,default=1)

    board_id = request.args.get("board_id",type=int,default=0)

    start = (page - 1) * current_app.config.get("PER_PAGE_COUNT")
    end = start + current_app.config.get("PER_PAGE_COUNT")

    query_posts = PostModel.query.order_by(PostModel.create_time.desc())

    if board_id:
        query_posts = query_posts.filter_by(board_id=board_id)

    total = query_posts.count()

    posts = query_posts.slice(start,end)

    pagination = Pagination(bs_version=5,page=page,total=total,outer_window=0,inner_window=2,
                            alignment="center")
    
    context = {
        "posts": posts,
        "boards": boards,
        "pagination": pagination,
        "current_board": board_id
    }
    current_app.logger.info("index页面被请求了")
    return render_template("index.html", **context)
