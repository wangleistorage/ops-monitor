
from sqlalchemy import select, update, and_
from sqlalchemy.orm import Session
from models.database import PublishProject, CloudHost


class CRUDPublishProject:

    async def get_publish_project_list(self, db: Session):
        """ 查询所有项目信息 """
        query = db.query(PublishProject)

        return query.filter(and_(
            PublishProject.label != '',
            PublishProject.slb_id != '-1',
            PublishProject.port != '-1'
        )).all()


    async def get_publish_project_by_local_name(self, db: Session, params: dict):
        """ 查询单个项目信息 """
        query = db.query(PublishProject)
        queryset = query.filter_by(**params).all()
        data = []
        for obj in queryset:
            query = db.query(CloudHost)
            slb_obj = query.filter_by(resource_type='slb', instance_id=obj.slb_id).first()
            if slb_obj.private_ip:
                http = f'{slb_obj.private_ip[0]}:{obj.port}'
            elif slb_obj.public_ip:
                http = f'{slb_obj.public_ip[0]}:{obj.port}'
            else:
                http = f'获取端口失败, 建议反馈至运维'
            data.append({
                "local_name": obj.local_name,
                "label": obj.label,
                "label_name": obj.label_name,
                "slb_id": obj.slb_id,
                "port": obj.port,
                "http": http
            })

        return data
    
publish_project_crud = CRUDPublishProject()