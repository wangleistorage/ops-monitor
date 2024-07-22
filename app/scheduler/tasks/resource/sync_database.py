from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import CloudDatabase
from scheduler.celery import celery_app
from settings import config


engine = create_engine(config.DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@celery_app.task(name="sync_database", bind=True)
def sync_databases(self):
    print("this is a scheduled database task")
    db = SessionLocal()
    objs = db.query(CloudDatabase).filter_by(platform="阿里云").first()
    print(objs.account_name, objs.region)
    return []

