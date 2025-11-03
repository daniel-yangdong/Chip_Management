# app/models/customer.py

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from app.models.base_model import BaseModel, Base
import enum

class CustomerType(enum.Enum):
    """客户类型枚举"""
    DIRECT = "direct"          # 直接客户
    DISTRIBUTOR = "distributor" # 分销商
    AGENT = "agent"            # 代理商

class CustomerStatus(enum.Enum):
    """客户状态枚举"""
    ACTIVE = "active"      # 活跃
    INACTIVE = "inactive"  # 非活跃
    PENDING = "pending"    # 待审核

class Customer(BaseModel):
    """客户模型（采购方）"""
    __tablename__ = 'customers'  # 数据库表名
    
    # 客户基本信息
    name = Column(String(200), nullable=False, index=True)  # 公司名称，建立索引便于搜索
    code = Column(String(50), unique=True, nullable=False, index=True)  # 客户代码，唯一且建立索引
    customer_type = Column(ENUM(CustomerType), default=CustomerType.DIRECT, nullable=False)  # 客户类型，使用枚举
    status = Column(ENUM(CustomerStatus), default=CustomerStatus.PENDING, nullable=False)  # 客户状态
    
    # 公司信息
    company_address = Column(Text, nullable=False)  # 公司地址，使用Text类型存储长文本
    company_phone = Column(String(50))  # 公司电话
    company_email = Column(String(100))  # 公司邮箱
    website = Column(String(200))  # 公司网站
    
    # 营业执照信息
    business_license_number = Column(String(100))  # 营业执照号
    tax_identification_number = Column(String(100))  # 税务登记号
    registered_capital = Column(String(100))  # 注册资本，使用字符串存储因为可能有单位
    
    # 商务信息
    payment_terms = Column(String(100), default="Net 30")  # 付款条款
    credit_limit = Column(String(100))  # 信用额度
    currency_preference = Column(String(10), default="CNY")  # 货币偏好
    
    # 定义关系：一个客户可以有多个联系人
    contacts = relationship("CustomerContact", back_populates="customer", cascade="all, delete-orphan")
    # 定义关系：一个客户可以有多个采购订单
    purchase_orders = relationship("PurchaseOrder", back_populates="customer")
    
    # 数据库表级别的约束和索引
    __table_args__ = (
        Index('idx_customer_name', 'name'),  # 为公司名字段创建索引
        Index('idx_customer_status', 'status'),  # 为状态字段创建索引
    )

class CustomerContact(BaseModel):
    """客户联系人模型"""
    __tablename__ = 'customer_contacts'  # 数据库表名
    
    # 外键关联到客户表，ondelete='CASCADE'表示客户删除时联系人也会被删除
    customer_id = Column(String(36), ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)
    
    # 联系人信息
    name = Column(String(100), nullable=False)  # 联系人姓名
    position = Column(String(100))  # 职位
    department = Column(String(100))  # 部门
    is_purchaser = Column(Boolean, default=False)  # 是否是采购员
    is_primary = Column(Boolean, default=False)  # 是否是主要联系人
    
    # 联系信息
    phone = Column(String(50))  # 办公电话
    mobile = Column(String(50))  # 手机号码
    email = Column(String(100))  # 电子邮箱
    wechat = Column(String(100))  # 微信号
    
    # 备注信息
    notes = Column(Text)  # 备注，使用Text类型存储可能的长文本
    
    # 定义关系：联系人属于一个客户
    customer = relationship("Customer", back_populates="contacts")
    
    # 数据库表级别的索引
    __table_args__ = (
        Index('idx_contact_customer', 'customer_id'),  # 为客户ID字段创建索引
    )