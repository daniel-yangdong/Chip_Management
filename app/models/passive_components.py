from app.models.electronic_components import ElectronicComponent
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app.database.database import db


class PassiveComponent(ElectronicComponent):
    """被动元件大类 - 电阻、电容、电感等"""
    __tablename__ = 'passive_components'

    id = db.Column(db.Integer, db.ForeignKey('electronic_components.id'), primary_key=True,
                   comment='外键关联基础元器件ID')
    # 元件类型
    component_type = db.Column(db.String(50), comment='元件类型：resistor(电阻)、capacitor(电容)、inductor(电感)')
    # 额定值
    nominal_value = db.Column(db.Float, comment='额定值（电阻阻值、电容容值、电感感值）')
    # 单位
    value_unit = db.Column(db.String(10), comment='数值单位：Ω(欧姆)、F(法拉)、H(亨利)')
    # 容差
    tolerance = db.Column(db.Float, comment='容差，单位：%')
    # 额定电压
    rated_voltage = db.Column(db.Float, comment='额定电压，单位：V')
    # 温度系数
    temperature_coefficient = db.Column(db.String(50), comment='温度系数')

    __mapper_args__ = {
        'polymorphic_identity': 'passive'
    }