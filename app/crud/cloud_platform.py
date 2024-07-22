
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.database import CloudPlatform


class CRUDCloudPlatform:

    async def get_cloud_platform_list(self, db: Session):
        """ 查询云平台账户列表 """
        statement = select(CloudPlatform)
        return db.scalars(statement).all()
    
cloud_platform_crud = CRUDCloudPlatform()