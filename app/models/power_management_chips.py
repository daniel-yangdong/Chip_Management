from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app.models.electronic_components import ElectronicComponent

from app.database.database import db



class PowerManagementChip(ElectronicComponent):
    """电源管理芯片大类 - 继承自电子元器件基类"""
    __tablename__ = 'power_management_chips'

    # 外键关联基础元器件表
    id = db.Column(db.Integer, db.ForeignKey('electronic_components.id'), primary_key=True,
                   comment='外键关联基础元器件ID')
    # 电源芯片类型
    power_chip_type = db.Column(db.String(20), nullable=False,
                                comment='电源芯片类型：ac_dc(AC-DC控制器)、dc_dc(DC-DC稳压器)、ldo(LDO稳压器)、pmic(电源管理IC)等')

    __mapper_args__ = {
        'polymorphic_identity': 'power'
        , 'polymorphic_on': power_chip_type
    }


# AC-DC控制器
class ACDCController(PowerManagementChip):
    """AC-DC控制器 - 用于交流转直流的电源管理芯片"""
    __tablename__ = 'ac_dc_controllers'

    id = db.Column(db.Integer, db.ForeignKey('power_management_chips.id'), primary_key=True,
                   comment='外键关联电源芯片ID')
    # 最小输入电压
    input_voltage_min = db.Column(db.Float, comment='最小输入电压，单位：V（交流有效值）')
    # 最大输入电压
    input_voltage_max = db.Column(db.Float, comment='最大输入电压，单位：V（交流有效值）')
    # 输出电压
    output_voltage = db.Column(db.Float, comment='额定输出电压，单位：V（直流）')
    # 最大输出电流
    output_current_max = db.Column(db.Float, comment='最大输出电流，单位：A')
    # 最大输出功率
    output_power_max = db.Column(db.Float, comment='最大输出功率，单位：W')
    # 转换效率
    efficiency = db.Column(db.Float, comment='典型转换效率，单位：%')
    # 开关频率
    switching_frequency = db.Column(db.Float, comment='开关频率，单位：Hz')
    # 拓扑结构
    topology = db.Column(db.String(50), comment='电源拓扑结构：Flyback(反激)、Forward(正激)、LLC等')
    # 是否支持功率因数校正
    has_pfc = db.Column(db.Boolean, default=False, comment='是否支持功率因数校正(PFC)功能')

    __mapper_args__ = {
        'polymorphic_identity': 'ac_dc'
    }


# DC-DC稳压器
class DCDCConverter(PowerManagementChip):
    """DC-DC稳压器 - 用于直流转直流的电源管理芯片"""
    __tablename__ = 'dc_dc_converters'

    id = db.Column(db.Integer, db.ForeignKey('power_management_chips.id'), primary_key=True,
                   comment='外键关联电源芯片ID')
    # 最小输入电压
    input_voltage_min = db.Column(db.Float, comment='最小输入电压，单位：V（直流）')
    # 最大输入电压
    input_voltage_max = db.Column(db.Float, comment='最大输入电压，单位：V（直流）')
    # 最小输出电压
    output_voltage_min = db.Column(db.Float, comment='最小输出电压（可调输出），单位：V（直流）')
    # 最大输出电压
    output_voltage_max = db.Column(db.Float, comment='最大输出电压（可调输出），单位：V（直流）')
    # 最大输出电流
    output_current_max = db.Column(db.Float, comment='最大输出电流，单位：A')
    # 开关频率
    switching_frequency = db.Column(db.Float, comment='开关频率，单位：Hz')
    # 转换效率
    efficiency = db.Column(db.Float, comment='典型转换效率，单位：%')
    # 转换器类型
    converter_type = db.Column(db.String(20), comment='转换器类型：BUCK(降压)、BOOST(升压)、BUCK-BOOST(升降压)')


# LDO稳压器
class LDORegulator(PowerManagementChip):
    """LDO稳压器 - 低压差线性稳压器"""
    __tablename__ = 'ldo_regulators'

    id = db.Column(db.Integer, db.ForeignKey('power_management_chips.id'), primary_key=True,
                   comment='外键关联电源芯片ID')
    # 最小输入电压
    input_voltage_min = db.Column(db.Float, comment='最小输入电压，单位：V（直流）')
    # 最大输入电压
    input_voltage_max = db.Column(db.Float, comment='最大输入电压，单位：V（直流）')
    # 输出电压
    output_voltage = db.Column(db.Float, comment='额定输出电压，单位：V（直流）')
    # 最大输出电流
    output_current_max = db.Column(db.Float, comment='最大输出电流，单位：A')
    # 压差电压
    dropout_voltage = db.Column(db.Float, comment='压差电压（输入输出最小差值），单位：V')
    # 静态电流
    quiescent_current = db.Column(db.Float, comment='静态工作电流（无负载时），单位：A')