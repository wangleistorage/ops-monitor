from sqlalchemy import Integer, String, Boolean, JSON, TIMESTAMP
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from typing import Optional

import datetime


# declarative base class
class Base(DeclarativeBase):
    created: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))
    updated: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))
    deleted: Mapped[bool] = mapped_column(default=False)

    # created_at: Mapped[timestamp] = mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP())


class CloudHost(Base):

    """ 服务器表 """
    __tablename__ = "ops_host"

    id: Mapped[int] = mapped_column(primary_key=True)
    instance_id: Mapped[str] = mapped_column(String(128))
    name: Mapped[str] = mapped_column(String(128))
    private_ip: Mapped[Optional[str]] = mapped_column(JSON)
    public_ip: Mapped[Optional[str]] = mapped_column(JSON)
    eip: Mapped[Optional[str]] = mapped_column(String(128))
    vpn_ip: Mapped[Optional[str]] = mapped_column(String(128))
    network_type: Mapped[Optional[str]] = mapped_column(String(128))
    charge_type: Mapped[Optional[str]] = mapped_column(String(128))
    instance_type: Mapped[Optional[str]] = mapped_column(String(128))
    cpu: Mapped[Optional[str]] = mapped_column(String(128))
    memory: Mapped[Optional[str]] = mapped_column(String(128))
    zone: Mapped[Optional[str]] = mapped_column(String(128))
    os: Mapped[Optional[str]] = mapped_column(String(128))
    os_type: Mapped[Optional[str]] = mapped_column(String(128))
    region: Mapped[Optional[str]] = mapped_column(String(128))
    account_name: Mapped[str] = mapped_column(String(128))
    platform: Mapped[str] = mapped_column(String(128))
    resource_type: Mapped[str] = mapped_column(String(128))
    division: Mapped[str] = mapped_column(String(128))
    business: Mapped[str] = mapped_column(String(128))
    create_time: Mapped[str] = mapped_column(String(128))
    expire_time: Mapped[str] = mapped_column(String(128))
    alarm_status: Mapped[bool] = mapped_column(default=True)
    jumpserver_status: Mapped[bool] = mapped_column(default=True)
    locked: Mapped[bool] = mapped_column(default=False)

    # 
    # heihei1: Mapped[Optional[str]]
    # heihei2: Mapped[Optional[str]] = mapped_column(nullable=False)
    # heihei3: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))


class CloudDatabase(Base):

    """ 数据库表 """
    __tablename__ = "ops_cloud_database"

    id: Mapped[int] = mapped_column(primary_key=True)
    instance_id: Mapped[str] = mapped_column(String(128))
    name: Mapped[str] = mapped_column(String(128))
    port: Mapped[str] = mapped_column(String(128))
    address: Mapped[str] = mapped_column(String(128))
    net_type: Mapped[str] = mapped_column(String(128))
    cpu: Mapped[int] = mapped_column(Integer)
    memory: Mapped[int] = mapped_column(Integer)
    disk: Mapped[int] = mapped_column(Integer)
    max_conn: Mapped[int] = mapped_column(Integer)
    max_iops: Mapped[int] = mapped_column(Integer)
    engine: Mapped[str] = mapped_column(String(128))
    engine_version: Mapped[str] = mapped_column(String(128))
    architecture: Mapped[str] = mapped_column(String(128))
    db_class: Mapped[str] = mapped_column(String(128))
    zone: Mapped[str] = mapped_column(String(128))
    region: Mapped[str] = mapped_column(String(128))
    pay_type: Mapped[str] = mapped_column(String(128))
    create_time: Mapped[str] = mapped_column(String(128))
    expire_time: Mapped[str] = mapped_column(String(128))
    platform: Mapped[str] = mapped_column(String(128))
    account_name: Mapped[str] = mapped_column(String(128))
    division: Mapped[str] = mapped_column(String(128))
    business: Mapped[str] = mapped_column(String(128))
    resource_type: Mapped[str] = mapped_column(String(128))
    alarm_status: Mapped[bool] = mapped_column(default=True)


class CloudPlatform(Base):
    """ 云平台表 """
    __tablename__ = "ops_cloud_platform"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(String(128))


class CloudAccount(Base):
    """ 云账户表 """
    __tablename__ = "ops_cloud_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    uid: Mapped[str] = mapped_column(String(128), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    ak: Mapped[str] = mapped_column(String(128), nullable=False)
    sk: Mapped[str] = mapped_column(String(128), nullable=False)
    sas_grade: Mapped[str] = mapped_column(String(128), nullable=False)
    balance: Mapped[int] = mapped_column(Integer)
    balance_alert: Mapped[int] = mapped_column(Integer)
    cms_monitor: Mapped[bool] = mapped_column(default=True)
    tag: Mapped[list[str]] = mapped_column(JSON)
    region: Mapped[list[str]] = mapped_column(JSON)
    authorization_list: Mapped[list[str]] = mapped_column(JSON)
    platform: Mapped[str] = mapped_column(String(128))


class CloudBusiness(Base):
    """ 业务线表 """
    __tablename__ = "business"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    code: Mapped[str] = mapped_column(String(128), nullable=False)


class CloudEip(Base):
    """ 云弹性IP表 """
    __tablename__ = "ops_cloud_vpc_eip"

    id: Mapped[int] = mapped_column(primary_key=True)
    instance_id: Mapped[str] = mapped_column(String(128), nullable=False)
    ip_address: Mapped[str] = mapped_column(String(128))
    name: Mapped[str] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(128))
    describe: Mapped[str] = mapped_column(String(128))
    bandwidth: Mapped[str] = mapped_column(String(128))
    instance_type: Mapped[str] = mapped_column(String(128))
    bind_instance_id: Mapped[str] = mapped_column(String(128))
    net_mode: Mapped[str] = mapped_column(String(128))
    charge_type: Mapped[str] = mapped_column(String(128))
    create_time: Mapped[str] = mapped_column(String(128))
    expire_time: Mapped[str] = mapped_column(String(128))
    alarm_status: Mapped[bool] = mapped_column(default=True)
    division: Mapped[str] = mapped_column(String(128))
    business: Mapped[str] = mapped_column(String(128))
    region: Mapped[str] = mapped_column(String(128))
    account_name: Mapped[str] = mapped_column(String(128))
    platform: Mapped[str] = mapped_column(String(128))
    resource_type: Mapped[str] = mapped_column(String(128))


class CloudNatGateway(Base):
    """ 云NatGateway表 """
    __tablename__ = "ops_cloud_nat_gateway"

    id: Mapped[int] = mapped_column(primary_key=True)
    instance_id: Mapped[str] = mapped_column(String(128), nullable=False)
    name: Mapped[str] = mapped_column(String(128))
    private_ip: Mapped[str] = mapped_column(String(128))
    max_bandwidth: Mapped[int] = mapped_column(String(128))
    eni_instance_id: Mapped[str] = mapped_column(String(128))
    nat_gateway_switch_id: Mapped[str] = mapped_column(String(128))
    bind_eip: Mapped[list[str]] = mapped_column(JSON)
    vpc_id: Mapped[str] = mapped_column(String(128))
    zone: Mapped[str] = mapped_column(String(128))

    charge_type: Mapped[str] = mapped_column(String(128))
    create_time: Mapped[str] = mapped_column(String(128))
    expire_time: Mapped[str] = mapped_column(String(128))
    division: Mapped[str] = mapped_column(String(128))
    business: Mapped[str] = mapped_column(String(128))
    region: Mapped[str] = mapped_column(String(128))
    account_name: Mapped[str] = mapped_column(String(128))
    platform: Mapped[str] = mapped_column(String(128))
    resource_type: Mapped[str] = mapped_column(String(128))


class PublishProject(Base):
    """ 发布系统项目映射表 """
    __tablename__ = "ops_publish_project_label_map"

    id: Mapped[int] = mapped_column(primary_key=True)
    local_name: Mapped[str] = mapped_column(String(128))
    label_name: Mapped[str] = mapped_column(String(128))
    label: Mapped[str] = mapped_column(String(128))
    slb_id: Mapped[str] = mapped_column(String(128))
    port: Mapped[Optional[int]] = mapped_column(Integer)
    