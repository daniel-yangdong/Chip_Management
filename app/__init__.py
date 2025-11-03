# app/__init__.py
from flask import Flask
from flask_cors import CORS
from app.database import db

def create_app():
    """Flask应用工厂函数"""
    # 创建Flask应用实例
    app = Flask(__name__)
    # 启用CORS（跨域资源共享）
    CORS(app)
    
    # 应用配置
    app.config['JSON_SORT_KEYS'] = False  # 保持JSON字段顺序
    app.config['JSON_AS_ASCII'] = False   # 支持中文字符
    app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///app.db'  # 数据库URL
    app.config['SQLALCHEMY_ECHO'] = True  # 输出SQL日志（开发环境）
    
    # 初始化数据库
    db.init_app(app)
    
    # 注册蓝图（路由）
    register_blueprints(app)
    
    return app  # 返回配置好的Flask应用

def register_blueprints(app):
    """注册所有蓝图"""
    from app.controllers.customer_controller import customer_bp
    
    # 注册客户相关的API路由，URL前缀为/api/v1
    app.register_blueprint(customer_bp, url_prefix='/api/v1')