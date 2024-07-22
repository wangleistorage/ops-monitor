
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.database import CloudNatGateway


class CRUDCloudNatGateway:

    async def get_nat_gateway_list(self,params, db: Session):
        """ 查询所有natgateway信息 """
        query = db.query(CloudNatGateway)
        return query.filter_by(**params).all()

    async def get_nat_gateway_by_instance_id(self, db: Session, instance_id: str):
        """ 查询单个实例信息 """
        statement = select(CloudNatGateway).where(CloudNatGateway.instance_id == instance_id)
        return db.scalars(statement).first()
    
cloud_nat_gateway_crud = CRUDCloudNatGateway()