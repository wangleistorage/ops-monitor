from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from settings import config


engine = create_engine(config.DATABASE_URL, echo=False)
Session = sessionmaker(engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()