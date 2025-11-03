# app/utils/response.py
from typing import Any, Dict, List, Optional
from flask import jsonify

class APIResponse:
    """统一的API响应工具类"""
    
    @staticmethod
    def success(data: Any = None, message: str = "Success", status_code: int = 200):
        """成功响应"""
        response = {
            "success": True,  # 表示请求成功
            "message": message,  # 成功消息
            "data": data  # 响应数据
        }
        # 返回Flask JSON响应和HTTP状态码
        return jsonify(response), status_code

    @staticmethod
    def error(message: str = "Error", status_code: int = 400, details: Optional[List] = None):
        """错误响应"""
        response = {
            "success": False,  # 表示请求失败
            "message": message,  # 错误消息
            "details": details or []  # 错误详情列表
        }
        return jsonify(response), status_code

    @staticmethod
    def created(data: Any = None, message: str = "Resource created"):
        """资源创建成功响应"""
        return APIResponse.success(data, message, 201)  # 201表示资源创建成功

    @staticmethod
    def no_content():
        """无内容响应（用于删除操作）"""
        return "", 204  # 204表示成功但无内容返回

    @staticmethod
    def paginated(items: List, total_count: int, page: int, page_size: int, links: List[Dict]):
        """分页响应"""
        data = {
            "items": items,  # 数据列表
            "total_count": total_count,  # 总记录数
            "page": page,  # 当前页码
            "page_size": page_size,  # 每页大小
            "total_pages": (total_count + page_size - 1) // page_size,  # 总页数
            "_links": links  # HATEOAS链接
        }
        return APIResponse.success(data)