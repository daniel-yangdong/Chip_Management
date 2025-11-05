from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app.database.database import db


class ElectronicComponent(db.Model):
    """电子元器件基类 - 所有电子元器件的通用属性"""
    __tablename__ = 'electronic_components'

    # 主键标识
    id = db.Column(db.Integer, primary_key=True, comment='元器件唯一标识ID')
    # 元器件名称
    name = db.Column(db.String(100), nullable=False, comment='元器件显示名称')
    # 制造商
    manufacturer = db.Column(db.String(100), nullable=False, comment='元器件制造商，如TI、ADI、ST、Infineon等')
    # 型号/料号
    part_number = db.Column(db.String(50), nullable=False, unique=True, comment='元器件型号/料号，具有唯一性')
    # 元器件描述
    description = db.Column(db.Text, comment='元器件详细描述和特性说明')
    # 封装类型
    package_type = db.Column(db.String(50), comment='元器件封装类型，如SOP-8、QFN-16、TO-220、0805等')
    # 最低工作温度
    operating_temperature_min = db.Column(db.Float, comment='最低工作温度，单位：°C')
    # 最高工作温度
    operating_temperature_max = db.Column(db.Float, comment='最高工作温度，单位：°C')
    # 元器件大类
    component_category = db.Column(db.String(20), nullable=False,
                                   comment='元器件大类：power(电源芯片)、mcu(MCU控制器)、memory(存储器)、discrete(分立器件)、passive(被动元件)等')
    # 元器件子类
    component_subcategory = db.Column(db.String(20), nullable=False, comment='元器件子类，具体类型取决于大类')
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='记录创建时间')
    # 更新时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='记录最后更新时间')

    __mapper_args__ = {
        'polymorphic_identity': 'electronic_component',
        'polymorphic_on': component_category
    }