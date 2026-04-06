"""
依赖注入
"""
from fastapi import Depends
from app.services.file_service import FileService


# 创建全局服务实例
_file_service_instance = None


def get_file_service() -> FileService:
    """获取文件服务实例"""
    global _file_service_instance
    if _file_service_instance is None:
        _file_service_instance = FileService()
    return _file_service_instance
