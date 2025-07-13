from flask_mail import Message
from exts import mail
from celery import Celery

def send_mail(recipient,subject,body):
    message = Message(subject=subject,recipients=[recipient],body=body)
    mail.send(message)
    print("发送成功!")

def make_celery(app):
    celery = Celery(app.import_name,backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self,*args,**kwargs):
            with app.app_context():
                return TaskBase.__call__(self,*args,**kwargs)
    # 这不是在创建实例，而是在设置类属性       
    celery.Task = ContextTask
    app.celery = celery

    # 添加任务
    celery.task(name="send_mail")(send_mail)

    return celery