from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models.electronic_components import ElectronicComponent
from app.models.power_management_chips import PowerManagementChip, ACDCController, DCDCConverter, LDORegulator
from app.models.mcu_controllers import MCUController
from app.models.memory_chips import MemoryChip
from app.models.discrete_devices import DiscreteDevice
from app.models.passive_components import PassiveComponent
from app.models.filters import Filter
from app.models.relays import Relay
from app.controllers.component_controller import components_bp
from app.database.database import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/electronic_components_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 300,
        'pool_pre_ping': True
    }

    # 初始化数据库
    db.init_app(app)

    # 注册蓝图
    app.register_blueprint(components_bp)

    # 创建表结构
    with app.app_context():
        print("准备创建的表:", list(db.metadata.tables.keys()))
        db.create_all()
        print("数据库表创建完成")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
