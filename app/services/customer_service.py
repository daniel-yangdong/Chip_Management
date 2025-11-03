# app/services/customer_service.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.customer import Customer, CustomerContact, CustomerStatus
from app.schemas.customer_schemas import CustomerCreate, CustomerResponse, CustomerDetailResponse
from app.utils.response import APIResponse

class CustomerService:
    """客户服务类，处理所有客户相关的业务逻辑"""
    
    def __init__(self, db: Session):
        """初始化服务类，注入数据库会话"""
        self.db = db  # 数据库会话对象

    def create_customer(self, customer_data: CustomerCreate) -> Customer:
        """创建新客户"""
        # 检查客户代码是否已存在
        existing_customer = self.db.query(Customer).filter(
            Customer.code == customer_data.code  # 根据客户代码查询
        ).first()  # 获取第一个匹配的结果
        
        if existing_customer:
            # 如果客户代码已存在，抛出异常
            raise ValueError(f"客户代码 {customer_data.code} 已存在")
        
        # 创建客户对象，排除contacts字段（需要单独处理）
        customer_dict = customer_data.dict(exclude={'contacts'})
        customer = Customer(**customer_dict)  # 使用字典解包创建客户实例
        
        # 添加联系人信息
        for contact_data in customer_data.contacts:
            # 为每个联系人数据创建联系人对象
            contact = CustomerContact(**contact_data.dict())
            # 将联系人添加到客户的联系人列表中
            customer.contacts.append(contact)
        
        # 将客户对象添加到数据库会话
        self.db.add(customer)
        # 提交事务，将数据保存到数据库
        self.db.commit()
        # 刷新对象，获取数据库生成的ID等字段
        self.db.refresh(customer)
        
        return customer  # 返回创建的客户对象

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """根据ID获取客户"""
        # 查询指定ID的客户
        return self.db.query(Customer).filter(Customer.id == customer_id).first()

    def get_customer_by_code(self, code: str) -> Optional[Customer]:
        """根据客户代码获取客户"""
        # 查询指定客户代码的客户
        return self.db.query(Customer).filter(Customer.code == code).first()

    def list_customers(self, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[Customer]:
        """获取客户列表"""
        # 构建基础查询
        query = self.db.query(Customer)
        
        # 如果提供了状态参数，添加状态过滤条件
        if status:
            query = query.filter(Customer.status == CustomerStatus(status))
        
        # 执行分页查询：跳过指定数量的记录，限制返回的记录数
        return query.offset(skip).limit(limit).all()

    def update_customer_status(self, customer_id: str, status: CustomerStatus) -> Optional[Customer]:
        """更新客户状态"""
        # 获取指定ID的客户
        customer = self.get_customer(customer_id)
        if not customer:
            return None  # 如果客户不存在，返回None
        
        # 更新客户状态
        customer.status = status
        # 提交事务
        self.db.commit()
        # 刷新对象
        self.db.refresh(customer)
        
        return customer  # 返回更新后的客户对象

    def delete_customer(self, customer_id: str) -> bool:
        """删除客户"""
        # 获取指定ID的客户
        customer = self.get_customer(customer_id)
        if not customer:
            return False  # 如果客户不存在，返回False
        
        # 从数据库中删除客户（由于外键约束，关联的联系人也会被删除）
        self.db.delete(customer)
        # 提交事务
        self.db.commit()
        return True  # 删除成功，返回True