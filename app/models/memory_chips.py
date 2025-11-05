from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app.models.electronic_components import ElectronicComponent

from app.database.database import db


class MemoryChip(ElectronicComponent):
    """存储器芯片大类"""
    __tablename__ = 'memory_chips'

    id = db.Column(db.Integer, db.ForeignKey('electronic_components.id'), primary_key=True,
                   comment='外键关联基础元器件ID')
    # 存储器类型
    memory_type = db.Column(db.String(50),
                            comment='存储器类型：Flash(闪存)、SRAM(静态随机存储器)、DRAM(动态随机存储器)、EEPROM(电可擦可编程只读存储器)等')
    # 存储容量
    capacity = db.Column(db.Integer, comment='存储容量，单位：KB/MB/GB')
    # 容量单位
    capacity_unit = db.Column(db.String(10), comment='容量单位：KB、MB、GB')
    # 接口类型
    interface_type = db.Column(db.String(50), comment='接口类型：SPI、I2C、Parallel、SDIO等')
    # 读写速度
    speed = db.Column(db.Float, comment='读写速度，单位：MHz或MB/s')
    # 工作电压
    operating_voltage = db.Column(db.Float, comment='工作电压，单位：V')

    __mapper_args__ = {
        'polymorphic_identity': 'memory'
    }