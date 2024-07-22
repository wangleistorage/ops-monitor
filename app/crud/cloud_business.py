
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.database import CloudBusiness


class CRUDCloudBusiness:

    async def get_business_list(self, params, db: Session):
        """ 查询所有实例信息 """
        query = db.query(CloudBusiness)
        return query.filter_by(**params).all()

cloud_business_crud = CRUDCloudBusiness()