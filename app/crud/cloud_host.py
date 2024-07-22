
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from models.database import CloudHost


class CRUDCloudHost:

    async def get_host_list(self, params, db: Session):
        """ 查询所有实例信息 """
        query = db.query(CloudHost)
        return query.filter_by(**params).all()

    async def get_host_by_instance_id(self, db: Session, instance_id: str):
        """ 查询单个实例信息 """
        statement = select(CloudHost).where(CloudHost.instance_id == instance_id)
        return db.scalars(statement).first()

    async def update_host(self, db: Session, host_id: str, data: dict):
        """ 更新主机信息 """
        statement = update(CloudHost).where(CloudHost.id == host_id).values(**data)
        db.execute(statement)
        db.commit()
        db.flush()

    async def create_host(self, db: Session, data: dict):
        """ 添加主机信息 """
        host = CloudHost(**data)
        db.add(host)
        db.commit()
        db.flush()
    
cloud_host_crud = CRUDCloudHost()