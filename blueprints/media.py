from flask import Blueprint,current_app,send_from_directory
import os

bp = Blueprint("media",__name__,url_prefix="/media")
@bp.get("avatars/<path:filename>")
def media_file(filename):
    avatars_dir = current_app.config['AVATARS_SAVE_PATH']
    return send_from_directory(avatars_dir, filename)