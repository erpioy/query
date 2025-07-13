from flask import session,g
from models.user import UserModel

def before_request():
    if "user_id" in session:
        user_id = session.get("user_id")
        try:
            user = UserModel.query.get(user_id)
            # 给g全局变量添加一个属性
            setattr(g,"user",user)
        except Exception:
            pass