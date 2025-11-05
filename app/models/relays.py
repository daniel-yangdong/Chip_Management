from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app.models.electronic_components import ElectronicComponent

from app.database.database import db



class Relay(ElectronicComponent):
    """继电器大类"""
    __tablename__ = 'relays'

    id = db.Column(db.Integer, db.ForeignKey('electronic_components.id'), primary_key=True,
                   comment='外键关联基础元器件ID')
    # 继电器类型
    relay_type = db.Column(db.String(50),
                           comment='继电器类型：electromechanical(电磁继电器)、solid_state(固态继电器)、reed(干簧继电器)')
    # 线圈电压
    coil_voltage = db.Column(db.Float, comment='线圈电压，单位：V')
    # 触点配置
    contact_configuration = db.Column(db.String(50), comment='触点配置：SPST(单刀单掷)、SPDT(单刀双掷)、DPDT(双刀双掷)等')
    # 触点额定电流
    contact_current_rating = db.Column(db.Float, comment='触点额定电流，单位：A')
    # 触点额定电压
    contact_voltage_rating = db.Column(db.Float, comment='触点额定电压，单位：V')
    # 操作时间
    operate_time = db.Column(db.Float, comment='操作时间，单位：ms')

    __mapper_args__ = {
        'polymorphic_identity': 'relay'
    }