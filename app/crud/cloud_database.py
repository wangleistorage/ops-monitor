
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.database import CloudDatabase


class CRUDCloudDatabase:

    async def get_database_list(self, params, db: Session):
        """ 查询所有实例信息 """
        query = db.query(CloudDatabase)
        return query.filter_by(**params).all()

    async def get_database_by_instance_id(self, db: Session, instance_id: str):
        """ 查询单个实例信息 """
        statement = select(CloudDatabase).where(CloudDatabase.instance_id == instance_id)
        return db.scalars(statement).first()
    
cloud_database_crud = CRUDCloudDatabase()