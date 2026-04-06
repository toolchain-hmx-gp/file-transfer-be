"""
路径处理工具
"""
from pathlib import Path

from app.core.config import TEMP_DIR, FILES_DIR


def get_temp_file_dir(file_name: str) -> Path:
    """获取文件的临时目录路径"""
    return TEMP_DIR / file_name


def get_temp_chunk_path(file_name: str, chunk_index: int) -> Path:
    """获取临时分片文件路径"""
    return get_temp_file_dir(file_name) / str(chunk_index)


def get_final_file_path(file_name: str) -> Path:
    """获取最终文件路径"""
    return FILES_DIR / file_name


def get_file_url(file_name: str) -> str:
    """获取文件访问URL"""
    return f"/uploads/{file_name}"
