"""
应用配置
"""
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.parent.parent

# 目录配置
TEMP_DIR = BASE_DIR / "temp"
FILES_DIR = BASE_DIR / "files"
UPLOADS_DIR = BASE_DIR / "uploads"

# 文件上传配置
MAX_FILE_SIZE = 1024 * 1024 * 1024  # 1GB
CHUNK_SIZE = 8192  # 8KB 缓冲区
