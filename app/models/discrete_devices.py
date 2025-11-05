from app.models.electronic_components import ElectronicComponent
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app.database.database import db


class DiscreteDevice(ElectronicComponent):
    """分立器件大类 - 二极管、晶体管等"""
    __tablename__ = 'discrete_devices'

    id = db.Column(db.Integer, db.ForeignKey('electronic_components.id'), primary_key=True,
                   comment='外键关联基础元器件ID')
    # 器件类型
    device_type = db.Column(db.String(50),
                            comment='器件类型：diode(二极管)、transistor(晶体管)、mosfet(场效应管)、thyristor(晶闸管)等')
    # 额定电压
    rated_voltage = db.Column(db.Float, comment='额定电压，单位：V')
    # 额定电流
    rated_current = db.Column(db.Float, comment='额定电流，单位：A')
    # 最大功耗
    max_power_dissipation = db.Column(db.Float, comment='最大功耗，单位：W')
    # 正向压降（二极管）
    forward_voltage = db.Column(db.Float, comment='正向压降，单位：V')
    # 反向恢复时间（二极管）
    reverse_recovery_time = db.Column(db.Float, comment='反向恢复时间，单位：ns')

    __mapper_args__ = {
        'polymorphic_identity': 'discrete'
    }