from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app.models.electronic_components import ElectronicComponent

from app.database.database import db
class Filter(ElectronicComponent):
    """滤波器大类"""
    __tablename__ = 'filters'

    id = db.Column(db.Integer, db.ForeignKey('electronic_components.id'), primary_key=True,
                   comment='外键关联基础元器件ID')
    # 滤波器类型
    filter_type = db.Column(db.String(50),
                            comment='滤波器类型：low_pass(低通)、high_pass(高通)、band_pass(带通)、band_stop(带阻)')
    # 截止频率
    cutoff_frequency = db.Column(db.Float, comment='截止频率，单位：Hz')
    # 阻抗
    impedance = db.Column(db.Float, comment='特征阻抗，单位：Ω')
    # 插入损耗
    insertion_loss = db.Column(db.Float, comment='插入损耗，单位：dB')
    # 带宽
    bandwidth = db.Column(db.Float, comment='带宽，单位：Hz')

    __mapper_args__ = {
        'polymorphic_identity': 'filter'
    }