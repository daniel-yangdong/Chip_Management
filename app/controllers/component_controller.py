from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from app.database.database import db
from app.models.discrete_devices import DiscreteDevice
from app.models.electronic_components import ElectronicComponent
from app.models.filters import Filter
from app.models.mcu_controllers import MCUController
from app.models.memory_chips import MemoryChip
from app.models.passive_components import PassiveComponent
from app.models.power_management_chips import PowerManagementChip, ACDCController, DCDCConverter, LDORegulator
from app.models.relays import Relay

# app = Flask(__name__)
# #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/electronic_components_db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/electronic_components_db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
#     'pool_recycle': 300,
#     'pool_pre_ping': True
# }
components_bp = Blueprint('components', __name__, url_prefix='/api/components')

# db.init_app(app)

# 创建数据库表
# with app.app_context():
#     db.create_all()


# 辅助函数
def component_to_dict(component):
    """将元器件对象转换为字典格式"""
    base_data = {
        'id': component.id,
        'name': component.name,
        'manufacturer': component.manufacturer,
        'part_number': component.part_number,
        'description': component.description,
        'package_type': component.package_type,
        'operating_temperature_min': component.operating_temperature_min,
        'operating_temperature_max': component.operating_temperature_max,
        'component_category': component.component_category,
        'component_subcategory': component.component_subcategory,
        'created_at': component.created_at.isoformat() if component.created_at else None,
        'updated_at': component.updated_at.isoformat() if component.updated_at else None
    }

    # 根据具体类型添加特定字段
    if isinstance(component, PowerManagementChip):
        base_data.update({
            'power_chip_type': component.power_chip_type
        })

        if isinstance(component, ACDCController):
            base_data.update({
                'input_voltage_min': component.input_voltage_min,
                'input_voltage_max': component.input_voltage_max,
                'output_voltage': component.output_voltage,
                'output_current_max': component.output_current_max,
                'output_power_max': component.output_power_max,
                'efficiency': component.efficiency,
                'switching_frequency': component.switching_frequency,
                'topology': component.topology,
                'has_pfc': component.has_pfc
            })
        elif isinstance(component, DCDCConverter):
            base_data.update({
                'input_voltage_min': component.input_voltage_min,
                'input_voltage_max': component.input_voltage_max,
                'output_voltage_min': component.output_voltage_min,
                'output_voltage_max': component.output_voltage_max,
                'output_current_max': component.output_current_max,
                'switching_frequency': component.switching_frequency,
                'efficiency': component.efficiency,
                'converter_type': component.converter_type
            })
        elif isinstance(component, LDORegulator):
            base_data.update({
                'input_voltage_min': component.input_voltage_min,
                'input_voltage_max': component.input_voltage_max,
                'output_voltage': component.output_voltage,
                'output_current_max': component.output_current_max,
                'dropout_voltage': component.dropout_voltage,
                'quiescent_current': component.quiescent_current
            })

    elif isinstance(component, MCUController):
        base_data.update({
            'core_architecture': component.core_architecture,
            'clock_frequency': component.clock_frequency,
            'flash_memory': component.flash_memory,
            'sram_memory': component.sram_memory,
            'operating_voltage': component.operating_voltage,
            'gpio_count': component.gpio_count,
            'adc_resolution': component.adc_resolution,
            'communication_interfaces': component.communication_interfaces
        })

    elif isinstance(component, MemoryChip):
        base_data.update({
            'memory_type': component.memory_type,
            'capacity': component.capacity,
            'capacity_unit': component.capacity_unit,
            'interface_type': component.interface_type,
            'speed': component.speed,
            'operating_voltage': component.operating_voltage
        })

    elif isinstance(component, DiscreteDevice):
        base_data.update({
            'device_type': component.device_type,
            'rated_voltage': component.rated_voltage,
            'rated_current': component.rated_current,
            'max_power_dissipation': component.max_power_dissipation,
            'forward_voltage': component.forward_voltage,
            'reverse_recovery_time': component.reverse_recovery_time
        })

    elif isinstance(component, PassiveComponent):
        base_data.update({
            'component_type': component.component_type,
            'nominal_value': component.nominal_value,
            'value_unit': component.value_unit,
            'tolerance': component.tolerance,
            'rated_voltage': component.rated_voltage,
            'temperature_coefficient': component.temperature_coefficient
        })

    elif isinstance(component, Filter):
        base_data.update({
            'filter_type': component.filter_type,
            'cutoff_frequency': component.cutoff_frequency,
            'impedance': component.impedance,
            'insertion_loss': component.insertion_loss,
            'bandwidth': component.bandwidth
        })

    elif isinstance(component, Relay):
        base_data.update({
            'relay_type': component.relay_type,
            'coil_voltage': component.coil_voltage,
            'contact_configuration': component.contact_configuration,
            'contact_current_rating': component.contact_current_rating,
            'contact_voltage_rating': component.contact_voltage_rating,
            'operate_time': component.operate_time
        })

    return base_data


# API路由
@components_bp.route('/components', methods=['GET'])
def get_all_components():
    """获取所有元器件列表"""
    category = request.args.get('category')
    subcategory = request.args.get('subcategory')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = ElectronicComponent.query

    if category:
        query = query.filter(ElectronicComponent.component_category == category)
    if subcategory:
        query = query.filter(ElectronicComponent.component_subcategory == subcategory)

    components = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'components': [component_to_dict(comp) for comp in components.items],
        'total': components.total,
        'pages': components.pages,
        'current_page': components.page
    })


@components_bp.route('/<int:component_id>', methods=['GET'])
def get_component(component_id):
    """获取特定元器件详情"""
    component = ElectronicComponent.query.get(component_id)
    if not component:
        return jsonify({'error': 'Component not found'}), 404

    return jsonify(component_to_dict(component))


# 电源芯片相关API
@components_bp.route('/power/ac-dc', methods=['POST'])
def create_ac_dc_controller():
    """创建AC-DC控制器"""
    try:
        data = request.get_json()
        chip = ACDCController(
            name=data['name'],
            manufacturer=data['manufacturer'],
            part_number=data['part_number'],
            description=data.get('description'),
            package_type=data.get('package_type'),
            operating_temperature_min=data.get('operating_temperature_min'),
            operating_temperature_max=data.get('operating_temperature_max'),
            component_category='power',
            component_subcategory='ac_dc_controller',
            power_chip_type='ac_dc',
            input_voltage_min=data.get('input_voltage_min'),
            input_voltage_max=data.get('input_voltage_max'),
            output_voltage=data.get('output_voltage'),
            output_current_max=data.get('output_current_max'),
            output_power_max=data.get('output_power_max'),
            efficiency=data.get('efficiency'),
            switching_frequency=data.get('switching_frequency'),
            topology=data.get('topology'),
            has_pfc=data.get('has_pfc', False)
        )
        db.session.add(chip)
        db.session.commit()
        return jsonify(component_to_dict(chip)), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error creating AC-DC controller: {e}")  # 添加日志输出
        return jsonify({'error': str(e)}), 500


@components_bp.route('/power/dc-dc', methods=['POST'])
def create_dc_dc_converter():
    """创建DC-DC稳压器"""
    data = request.get_json()

    chip = DCDCConverter(
        name=data['name'],
        manufacturer=data['manufacturer'],
        part_number=data['part_number'],
        description=data.get('description'),
        package_type=data.get('package_type'),
        operating_temperature_min=data.get('operating_temperature_min'),
        operating_temperature_max=data.get('operating_temperature_max'),
        component_category='power',
        component_subcategory='dc_dc_converter',
        power_chip_type='dc_dc',
        input_voltage_min=data.get('input_voltage_min'),
        input_voltage_max=data.get('input_voltage_max'),
        output_voltage_min=data.get('output_voltage_min'),
        output_voltage_max=data.get('output_voltage_max'),
        output_current_max=data.get('output_current_max'),
        switching_frequency=data.get('switching_frequency'),
        efficiency=data.get('efficiency'),
        converter_type=data.get('converter_type')
    )

    db.session.add(chip)
    db.session.commit()

    return jsonify(component_to_dict(chip)), 201


@components_bp.route('/power/ldo', methods=['POST'])
def create_ldo_regulator():
    """创建LDO稳压器"""
    data = request.get_json()

    chip = LDORegulator(
        name=data['name'],
        manufacturer=data['manufacturer'],
        part_number=data['part_number'],
        description=data.get('description'),
        package_type=data.get('package_type'),
        operating_temperature_min=data.get('operating_temperature_min'),
        operating_temperature_max=data.get('operating_temperature_max'),
        component_category='power',
        component_subcategory='ldo_regulator',
        power_chip_type='ldo',
        input_voltage_min=data.get('input_voltage_min'),
        input_voltage_max=data.get('input_voltage_max'),
        output_voltage=data.get('output_voltage'),
        output_current_max=data.get('output_current_max'),
        dropout_voltage=data.get('dropout_voltage'),
        quiescent_current=data.get('quiescent_current')
    )

    db.session.add(chip)
    db.session.commit()

    return jsonify(component_to_dict(chip)), 201


# MCU控制器API
@components_bp.route('/mcu', methods=['POST'])
def create_mcu_controller():
    """创建MCU控制器"""
    data = request.get_json()

    mcu = MCUController(
        name=data['name'],
        manufacturer=data['manufacturer'],
        part_number=data['part_number'],
        description=data.get('description'),
        package_type=data.get('package_type'),
        operating_temperature_min=data.get('operating_temperature_min'),
        operating_temperature_max=data.get('operating_temperature_max'),
        component_category='mcu',
        component_subcategory=data.get('subcategory', 'mcu_controller'),
        core_architecture=data.get('core_architecture'),
        clock_frequency=data.get('clock_frequency'),
        flash_memory=data.get('flash_memory'),
        sram_memory=data.get('sram_memory'),
        operating_voltage=data.get('operating_voltage'),
        gpio_count=data.get('gpio_count'),
        adc_resolution=data.get('adc_resolution'),
        communication_interfaces=data.get('communication_interfaces')
    )

    db.session.add(mcu)
    db.session.commit()

    return jsonify(component_to_dict(mcu)), 201


# 其他元器件大类的API可以类似实现...

@components_bp.route('/<int:component_id>', methods=['PUT'])
def update_component(component_id):
    """更新元器件信息"""
    component = ElectronicComponent.query.get(component_id)
    if not component:
        return jsonify({'error': 'Component not found'}), 404

    data = request.get_json()

    # 更新通用字段
    for field in ['name', 'manufacturer', 'description', 'package_type']:
        if field in data:
            setattr(component, field, data[field])

    # 这里可以根据具体类型实现特定字段的更新
    # 由于篇幅限制，省略具体实现...

    db.session.commit()
    return jsonify(component_to_dict(component))


@components_bp.route('/<int:component_id>', methods=['DELETE'])
def delete_component(component_id):
    """删除元器件"""
    component = ElectronicComponent.query.get(component_id)
    if not component:
        return jsonify({'error': 'Component not found'}), 404

    db.session.delete(component)
    db.session.commit()

    return jsonify({'message': 'Component deleted successfully'})


