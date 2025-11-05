-- 创建数据库
CREATE DATABASE IF NOT EXISTS electronic_components_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE electronic_components_db;

-- 电子元器件基础表
CREATE TABLE electronic_components (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '元器件唯一标识ID',
    name VARCHAR(100) NOT NULL COMMENT '元器件显示名称',
    manufacturer VARCHAR(100) NOT NULL COMMENT '元器件制造商',
    part_number VARCHAR(50) NOT NULL UNIQUE COMMENT '元器件型号/料号',
    description TEXT COMMENT '元器件详细描述和特性说明',
    package_type VARCHAR(50) COMMENT '元器件封装类型',
    operating_temperature_min FLOAT COMMENT '最低工作温度，单位：°C',
    operating_temperature_max FLOAT COMMENT '最高工作温度，单位：°C',
    component_category VARCHAR(20) NOT NULL COMMENT '元器件大类',
    component_subcategory VARCHAR(20) NOT NULL COMMENT '元器件子类',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录最后更新时间',
    INDEX idx_category (component_category),
    INDEX idx_subcategory (component_subcategory),
    INDEX idx_manufacturer (manufacturer),
    INDEX idx_part_number (part_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='电子元器件基础表';

-- 电源管理芯片表
CREATE TABLE power_management_chips (
    id INT PRIMARY KEY COMMENT '外键关联基础元器件ID',
    power_chip_type VARCHAR(20) NOT NULL COMMENT '电源芯片类型',
    FOREIGN KEY (id) REFERENCES electronic_components(id) ON DELETE CASCADE,
    INDEX idx_power_type (power_chip_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='电源管理芯片表';

-- AC-DC控制器表
CREATE TABLE ac_dc_controllers (
    id INT PRIMARY KEY COMMENT '外键关联电源芯片ID',
    input_voltage_min FLOAT COMMENT '最小输入电压，单位：V（交流有效值）',
    input_voltage_max FLOAT COMMENT '最大输入电压，单位：V（交流有效值）',
    output_voltage FLOAT COMMENT '额定输出电压，单位：V（直流）',
    output_current_max FLOAT COMMENT '最大输出电流，单位：A',
    output_power_max FLOAT COMMENT '最大输出功率，单位：W',
    efficiency FLOAT COMMENT '典型转换效率，单位：%',
    switching_frequency FLOAT COMMENT '开关频率，单位：Hz',
    topology VARCHAR(50) COMMENT '电源拓扑结构',
    has_pfc BOOLEAN DEFAULT FALSE COMMENT '是否支持功率因数校正(PFC)功能',
    FOREIGN KEY (id) REFERENCES power_management_chips(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AC-DC控制器表';

-- DC-DC稳压器表
CREATE TABLE dc_dc_converters (
    id INT PRIMARY KEY COMMENT '外键关联电源芯片ID',
    input_voltage_min FLOAT COMMENT '最小输入电压，单位：V（直流）',
    input_voltage_max FLOAT COMMENT '最大输入电压，单位：V（直流）',
    output_voltage_min FLOAT COMMENT '最小输出电压，单位：V（直流）',
    output_voltage_max FLOAT COMMENT '最大输出电压，单位：V（直流）',
    output_current_max FLOAT COMMENT '最大输出电流，单位：A',
    switching_frequency FLOAT COMMENT '开关频率，单位：Hz',
    efficiency FLOAT COMMENT '典型转换效率，单位：%',
    converter_type VARCHAR(20) COMMENT '转换器类型',
    FOREIGN KEY (id) REFERENCES power_management_chips(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='DC-DC稳压器表';

-- LDO稳压器表
CREATE TABLE ldo_regulators (
    id INT PRIMARY KEY COMMENT '外键关联电源芯片ID',
    input_voltage_min FLOAT COMMENT '最小输入电压，单位：V（直流）',
    input_voltage_max FLOAT COMMENT '最大输入电压，单位：V（直流）',
    output_voltage FLOAT COMMENT '额定输出电压，单位：V（直流）',
    output_current_max FLOAT COMMENT '最大输出电流，单位：A',
    dropout_voltage FLOAT COMMENT '压差电压，单位：V',
    quiescent_current FLOAT COMMENT '静态工作电流，单位：A',
    FOREIGN KEY (id) REFERENCES power_management_chips(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='LDO稳压器表';

-- MCU控制器表
CREATE TABLE mcu_controllers (
    id INT PRIMARY KEY COMMENT '外键关联基础元器件ID',
    core_architecture VARCHAR(50) COMMENT 'MCU内核架构',
    clock_frequency FLOAT COMMENT '最大工作频率，单位：MHz',
    flash_memory INT COMMENT '内置闪存容量，单位：KB',
    sram_memory INT COMMENT '内置SRAM容量，单位：KB',
    operating_voltage FLOAT COMMENT '工作电压范围，单位：V',
    gpio_count INT COMMENT '通用输入输出引脚数量',
    adc_resolution INT COMMENT 'ADC分辨率，单位：bit',
    communication_interfaces VARCHAR(200) COMMENT '支持的通信接口',
    FOREIGN KEY (id) REFERENCES electronic_components(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='MCU控制器表';

-- 存储器芯片表
CREATE TABLE memory_chips (
    id INT PRIMARY KEY COMMENT '外键关联基础元器件ID',
    memory_type VARCHAR(50) COMMENT '存储器类型',
    capacity INT COMMENT '存储容量',
    capacity_unit VARCHAR(10) COMMENT '容量单位',
    interface_type VARCHAR(50) COMMENT '接口类型',
    speed FLOAT COMMENT '读写速度，单位：MHz或MB/s',
    operating_voltage FLOAT COMMENT '工作电压，单位：V',
    FOREIGN KEY (id) REFERENCES electronic_components(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='存储器芯片表';

-- 分立器件表
CREATE TABLE discrete_devices (
    id INT PRIMARY KEY COMMENT '外键关联基础元器件ID',
    device_type VARCHAR(50) COMMENT '器件类型',
    rated_voltage FLOAT COMMENT '额定电压，单位：V',
    rated_current FLOAT COMMENT '额定电流，单位：A',
    max_power_dissipation FLOAT COMMENT '最大功耗，单位：W',
    forward_voltage FLOAT COMMENT '正向压降，单位：V',
    reverse_recovery_time FLOAT COMMENT '反向恢复时间，单位：ns',
    FOREIGN KEY (id) REFERENCES electronic_components(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='分立器件表';

-- 被动元件表
CREATE TABLE passive_components (
    id INT PRIMARY KEY COMMENT '外键关联基础元器件ID',
    component_type VARCHAR(50) COMMENT '元件类型',
    nominal_value FLOAT COMMENT '额定值',
    value_unit VARCHAR(10) COMMENT '数值单位',
    tolerance FLOAT COMMENT '容差，单位：%',
    rated_voltage FLOAT COMMENT '额定电压，单位：V',
    temperature_coefficient VARCHAR(50) COMMENT '温度系数',
    FOREIGN KEY (id) REFERENCES electronic_components(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='被动元件表';

-- 滤波器表
CREATE TABLE filters (
    id INT PRIMARY KEY COMMENT '外键关联基础元器件ID',
    filter_type VARCHAR(50) COMMENT '滤波器类型',
    cutoff_frequency FLOAT COMMENT '截止频率，单位：Hz',
    impedance FLOAT COMMENT '特征阻抗，单位：Ω',
    insertion_loss FLOAT COMMENT '插入损耗，单位：dB',
    bandwidth FLOAT COMMENT '带宽，单位：Hz',
    FOREIGN KEY (id) REFERENCES electronic_components(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='滤波器表';

-- 继电器表
CREATE TABLE relays (
    id INT PRIMARY KEY COMMENT '外键关联基础元器件ID',
    relay_type VARCHAR(50) COMMENT '继电器类型',
    coil_voltage FLOAT COMMENT '线圈电压，单位：V',
    contact_configuration VARCHAR(50) COMMENT '触点配置',
    contact_current_rating FLOAT COMMENT '触点额定电流，单位：A',
    contact_voltage_rating FLOAT COMMENT '触点额定电压，单位：V',
    operate_time FLOAT COMMENT '操作时间，单位：ms',
    FOREIGN KEY (id) REFERENCES electronic_components(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='继电器表';