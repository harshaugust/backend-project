
from celery import Celery
from db.database import SessionLocal
from db.models import AccessLog


celery = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)

@celery.task
def log_access(text):
    db = SessionLocal()
    access_log = AccessLog(text=text)
    db.add(access_log)
    db.commit()
    db.close()