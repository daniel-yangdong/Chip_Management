# app/controllers/customer_controller.py
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from app.services.customer_service import CustomerService
from app.schemas.customer_schemas import CustomerCreate, CustomerResponse, CustomerDetailResponse
from app.database import db
from app.utils.response import APIResponse
from app.utils.validators import validate_json

# 创建蓝图，用于组织相关的路由
customer_bp = Blueprint('customers', __name__)

@customer_bp.route('/customers', methods=['POST'])
@validate_json(CustomerCreate)  # 使用装饰器验证JSON数据
def create_customer():
    """创建新客户 - RESTful API端点"""
    # 获取数据库会话
    session = db.get_session()
    
    try:
        # 解析和验证请求数据
        customer_data = CustomerCreate(**request.get_json())
        # 创建客户服务实例
        customer_service = CustomerService(session)
        
        # 调用服务层创建客户
        customer = customer_service.create_customer(customer_data)
        
        # 构建响应数据：将ORM对象转换为Pydantic模型，再转换为字典
        response_data = CustomerDetailResponse.from_orm(customer)
        
        # 返回成功响应，HTTP状态码201表示资源创建成功
        return APIResponse.created(
            data=response_data.dict(),  # 响应数据
            message="客户创建成功"  # 成功消息
        )
        
    except ValueError as e:
        # 处理业务逻辑错误（如客户代码重复）
        return APIResponse.error(str(e), 400)  # 400表示客户端错误
    except Exception as e:
        # 处理其他未知错误
        return APIResponse.error(f"创建客户失败: {str(e)}", 500)  # 500表示服务器错误
    finally:
        # 确保数据库会话被关闭，避免连接泄漏
        session.close()

@customer_bp.route('/customers', methods=['GET'])
def list_customers():
    """获取客户列表 - RESTful API端点"""
    session = db.get_session()
    
    try:
        # 获取查询参数，设置默认值
        page = request.args.get('page', 1, type=int)  # 页码，默认为1
        page_size = request.args.get('page_size', 20, type=int)  # 每页大小，默认为20
        status = request.args.get('status', type=str)  # 状态过滤参数
        
        # 验证和调整分页参数
        if page < 1:
            page = 1  # 页码不能小于1
        if page_size < 1 or page_size > 100:
            page_size = 20  # 每页大小限制在1-100之间
        
        # 计算要跳过的记录数
        skip = (page - 1) * page_size
        
        # 创建服务实例并获取客户列表
        customer_service = CustomerService(session)
        customers = customer_service.list_customers(skip, page_size, status)
        
        # 构建响应数据：将每个客户对象转换为响应模型
        customers_data = [CustomerResponse.from_orm(customer).dict() for customer in customers]
        
        # 返回成功响应
        return APIResponse.success(
            data={
                'items': customers_data,  # 客户列表
                'page': page,  # 当前页码
                'page_size': page_size,  # 每页大小
                'total': len(customers_data)  # 总记录数
            },
            message="获取客户列表成功"
        )
        
    except Exception as e:
        # 处理服务器错误
        return APIResponse.error(f"获取客户列表失败: {str(e)}", 500)
    finally:
        # 关闭数据库会话
        session.close()

@customer_bp.route('/customers/<string:customer_id>', methods=['GET'])
def get_customer(customer_id: str):
    """获取客户详情 - RESTful API端点"""
    session = db.get_session()
    
    try:
        # 创建服务实例
        customer_service = CustomerService(session)
        # 根据ID获取客户
        customer = customer_service.get_customer(customer_id)
        
        # 检查客户是否存在
        if not customer:
            return APIResponse.error("客户不存在", 404)  # 404表示资源未找到
        
        # 构建响应数据
        response_data = CustomerDetailResponse.from_orm(customer)
        
        # 返回成功响应
        return APIResponse.success(
            data=response_data.dict(),
            message="获取客户详情成功"
        )
        
    except Exception as e:
        # 处理服务器错误
        return APIResponse.error(f"获取客户详情失败: {str(e)}", 500)
    finally:
        # 关闭数据库会话
        session.close()

@customer_bp.route('/customers/<string:customer_id>/status', methods=['PUT'])
def update_customer_status(customer_id: str):
    """更新客户状态 - RESTful API端点"""
    session = db.get_session()
    
    try:
        # 解析请求数据
        data = request.get_json()
        # 验证必需字段
        if not data or 'status' not in data:
            return APIResponse.error("状态字段是必需的", 400)
        
        # 创建服务实例并更新客户状态
        customer_service = CustomerService(session)
        customer = customer_service.update_customer_status(customer_id, data['status'])
        
        # 检查客户是否存在
        if not customer:
            return APIResponse.error("客户不存在", 404)
        
        # 构建响应数据
        response_data = CustomerResponse.from_orm(customer)
        
        # 返回成功响应
        return APIResponse.success(
            data=response_data.dict(),
            message="客户状态更新成功"
        )
        
    except ValueError as e:
        # 处理业务逻辑错误
        return APIResponse.error(str(e), 400)
    except Exception as e:
        # 处理服务器错误
        return APIResponse.error(f"更新客户状态失败: {str(e)}", 500)
    finally:
        # 关闭数据库会话
        session.close()