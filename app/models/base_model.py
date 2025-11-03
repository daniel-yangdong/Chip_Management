# app/models/base_model.py
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
import uuid

# 创建声明性基类，所有模型都将继承自这个类
Base = declarative_base()

def generate_uuid():
    """生成UUID字符串作为主键"""
    return str(uuid.uuid4())

class BaseModel(Base):
    """基础模型类，包含所有模型共有的字段"""
    __abstract__ = True  # 这是一个抽象基类，不会创建对应的数据库表
    
    # 主键字段，使用UUID确保全局唯一性
    id = Column(String(36), primary_key=True, default=generate_uuid)
    # 创建时间，默认使用当前时间
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # 更新时间，每次记录更新时自动更新
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """将模型实例转换为字典格式，便于JSON序列化"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}