
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.database import CloudEip


class CRUDCloudEip:

    async def get_eip_list(self,params, db: Session):
        """ 查询所有EIP信息 """
        query = db.query(CloudEip)
        return query.filter_by(**params).all()

    async def get_eip_by_instance_id(self, db: Session, instance_id: str):
        """ 查询单个实例信息 """
        statement = select(CloudEip).where(CloudEip.instance_id == instance_id)
        return db.scalars(statement).first()
    
cloud_eip_crud = CRUDCloudEip()