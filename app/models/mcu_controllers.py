from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app.models.electronic_components import ElectronicComponent

from app.database.database import db


class MCUController(ElectronicComponent):
    """MCU控制器大类 - 微控制器单元"""
    __tablename__ = 'mcu_controllers'

    id = db.Column(db.Integer, db.ForeignKey('electronic_components.id'), primary_key=True,
                   comment='外键关联基础元器件ID')
    # 内核架构
    core_architecture = db.Column(db.String(50), comment='MCU内核架构：ARM Cortex-M0/M3/M4/M7、RISC-V、8051等')
    # 主频
    clock_frequency = db.Column(db.Float, comment='最大工作频率，单位：MHz')
    # 闪存容量
    flash_memory = db.Column(db.Integer, comment='内置闪存容量，单位：KB')
    # RAM容量
    sram_memory = db.Column(db.Integer, comment='内置SRAM容量，单位：KB')
    # 工作电压
    operating_voltage = db.Column(db.Float, comment='工作电压范围，单位：V')
    # GPIO数量
    gpio_count = db.Column(db.Integer, comment='通用输入输出引脚数量')
    # ADC分辨率
    adc_resolution = db.Column(db.Integer, comment='ADC分辨率，单位：bit')
    # 通信接口
    communication_interfaces = db.Column(db.String(200), comment='支持的通信接口：I2C、SPI、UART、USB、CAN等')

    __mapper_args__ = {
        'polymorphic_identity': 'mcu'
    }