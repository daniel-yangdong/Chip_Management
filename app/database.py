# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.models.base_model import Base
from app.models import customer  # 导入模型以确保它们被注册
import os

class Database:
    """数据库管理类"""
    
    def __init__(self):
        """初始化数据库连接参数"""
        self.engine = None  # SQLAlchemy引擎
        self.session_factory = None  # 会话工厂
        self.Session = None  # 线程安全的会话类
    
    def init_app(self, app):
        """初始化数据库连接"""
        # 从应用配置获取数据库URL
        database_url = app.config.get('SQLALCHEMY_DATABASE_URL')
        if not database_url:
            raise ValueError("DATABASE_URL 未配置")
        
        # 创建数据库引擎
        self.engine = create_engine(
            database_url,
            echo=app.config.get('SQLALCHEMY_ECHO', False),  # 是否输出SQL日志
            pool_pre_ping=True,  # 连接池预检查
            pool_recycle=3600  # 连接回收时间（秒）
        )
        
        # 创建会话工厂
        self.session_factory = sessionmaker(bind=self.engine)
        # 创建线程安全的会话类
        self.Session = scoped_session(self.session_factory)
        
        # 创建所有数据库表
        Base.metadata.create_all(self.engine)
    
    def get_session(self):
        """获取数据库会话"""
        if not self.Session:
            raise RuntimeError("数据库未初始化")
        return self.Session()  # 返回新的数据库会话
    
    def close_session(self):
        """关闭数据库会话"""
        if self.Session:
            self.Session.remove()  # 移除当前线程的会话

# 创建全局数据库实例
db = Database()