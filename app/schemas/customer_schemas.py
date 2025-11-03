# app/schemas/customer_schemas.py
from pydantic import BaseModel, Field, validator, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum

class CustomerType(str, Enum):
    """客户类型枚举（用于API）"""
    DIRECT = "direct"
    DISTRIBUTOR = "distributor"
    AGENT = "agent"

class CustomerStatus(str, Enum):
    """客户状态枚举（用于API）"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

class ContactCreate(BaseModel):
    """创建联系人请求模型"""
    name: str = Field(..., min_length=1, max_length=100, description="联系人姓名")
    position: Optional[str] = Field(None, max_length=100, description="职位")
    department: Optional[str] = Field(None, max_length=100, description="部门")
    is_purchaser: bool = Field(False, description="是否是采购员")
    is_primary: bool = Field(False, description="是否是主要联系人")
    phone: Optional[str] = Field(None, max_length=50, description="电话")
    mobile: Optional[str] = Field(None, max_length=50, description="手机")
    email: Optional[EmailStr] = Field(None, description="邮箱")  # 使用EmailStr自动验证邮箱格式
    wechat: Optional[str] = Field(None, max_length=100, description="微信")
    notes: Optional[str] = Field(None, description="备注")

class CustomerCreate(BaseModel):
    """创建客户请求模型"""
    name: str = Field(..., min_length=1, max_length=200, description="公司名称")
    code: str = Field(..., min_length=1, max_length=50, description="客户代码")
    customer_type: CustomerType = Field(CustomerType.DIRECT, description="客户类型")
    
    # 公司信息字段
    company_address: str = Field(..., min_length=1, description="公司地址")
    company_phone: Optional[str] = Field(None, max_length=50, description="公司电话")
    company_email: Optional[EmailStr] = Field(None, description="公司邮箱")
    website: Optional[str] = Field(None, max_length=200, description="网站")
    
    # 营业执照信息字段
    business_license_number: Optional[str] = Field(None, max_length=100, description="营业执照号")
    tax_identification_number: Optional[str] = Field(None, max_length=100, description="税号")
    registered_capital: Optional[str] = Field(None, max_length=100, description="注册资本")
    
    # 商务信息字段
    payment_terms: str = Field("Net 30", max_length=100, description="付款条款")
    credit_limit: Optional[str] = Field(None, max_length=100, description="信用额度")
    currency_preference: str = Field("CNY", max_length=10, description="货币偏好")
    
    # 联系人列表，必须至少有一个联系人
    contacts: List[ContactCreate] = Field(..., min_items=1, description="联系人列表")
    
    @validator('code')
    def validate_code(cls, v):
        """验证客户代码格式"""
        # 检查客户代码是否只包含字母、数字、下划线和连字符
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('客户代码只能包含字母、数字、下划线和连字符')
        # 转换为大写返回
        return v.upper()

class CustomerResponse(BaseModel):
    """客户响应模型"""
    id: str  # 客户ID
    name: str  # 公司名称
    code: str  # 客户代码
    customer_type: CustomerType  # 客户类型
    status: CustomerStatus  # 客户状态
    company_address: str  # 公司地址
    company_phone: Optional[str]  # 公司电话
    company_email: Optional[str]  # 公司邮箱
    website: Optional[str]  # 网站
    business_license_number: Optional[str]  # 营业执照号
    tax_identification_number: Optional[str]  # 税号
    registered_capital: Optional[str]  # 注册资本
    payment_terms: str  # 付款条款
    credit_limit: Optional[str]  # 信用额度
    currency_preference: str  # 货币偏好
    created_at: datetime  # 创建时间
    updated_at: datetime  # 更新时间
    
    class Config:
        # 允许从ORM对象创建Pydantic模型
        from_attributes = True

class CustomerContactResponse(BaseModel):
    """客户联系人响应模型"""
    id: str  # 联系人ID
    name: str  # 联系人姓名
    position: Optional[str]  # 职位
    department: Optional[str]  # 部门
    is_purchaser: bool  # 是否是采购员
    is_primary: bool  # 是否是主要联系人
    phone: Optional[str]  # 电话
    mobile: Optional[str]  # 手机
    email: Optional[str]  # 邮箱
    wechat: Optional[str]  # 微信
    notes: Optional[str]  # 备注
    created_at: datetime  # 创建时间
    
    class Config:
        # 允许从ORM对象创建Pydantic模型
        from_attributes = True

class CustomerDetailResponse(CustomerResponse):
    """客户详情响应模型，包含联系人信息"""
    contacts: List[CustomerContactResponse]  # 联系人列表