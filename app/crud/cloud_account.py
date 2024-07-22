
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.database import CloudAccount


class CRUDCloudAccount:

    async def get_account_by_platform(self, db: Session, params: dict):
        """ 查询云平台账户列表 """
        query = db.query(CloudAccount.name)
        return query.filter_by(**params).all()
    
    async def get_account_obj_by_platform(self, db: Session, platform: str, account_name: str):
        """ 查询云平台账户信息 """
        statement = select(CloudAccount).where(CloudAccount.platform == platform, CloudAccount.name == account_name)
        return db.scalars(statement).first()
    
    
cloud_account_crud = CRUDCloudAccount()