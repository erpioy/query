from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_caching import Cache
from flask_avatars import Avatars

db = SQLAlchemy()
mail = Mail()
cache = Cache()
avatars = Avatars()


