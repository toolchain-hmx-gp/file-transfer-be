"""
文件操作工具
"""
import shutil
from pathlib import Path

from app.core.config import CHUNK_SIZE
from app.core.exceptions import IncompleteChunks
from app.utils.path_utils import get_temp_file_dir, get_temp_chunk_path, get_final_file_path


def ensure_directories():
    """确保必要的目录存在"""
    from app.core.config import TEMP_DIR, FILES_DIR
    TEMP_DIR.mkdir(exist_ok=True)
    FILES_DIR.mkdir(exist_ok=True)


def save_chunk(file_stream, chunk_path: Path) -> None:
    """保存分片文件"""
    chunk_path.parent.mkdir(parents=True, exist_ok=True)
    with open(chunk_path, 'wb') as f:
        shutil.copyfileobj(file_stream, f)


def validate_chunks(file_name: str, total_chunks: int) -> tuple[bool, list[int]]:
    """
    验证文件分片完整性

    Args:
        file_name: 文件名
        total_chunks: 总分片数

    Returns:
        (是否完整, 缺失的分片索引列表)
    """
    temp_dir = get_temp_file_dir(file_name)

    if not temp_dir.exists():
        return False, list(range(total_chunks))

    existing_chunks = set()
    for chunk_file in temp_dir.iterdir():
        if chunk_file.is_file() and chunk_file.name.isdigit():
            existing_chunks.add(int(chunk_file.name))

    missing_chunks = []
    for i in range(total_chunks):
        if i not in existing_chunks:
            missing_chunks.append(i)

    return len(missing_chunks) == 0, missing_chunks


def merge_chunks_stream(file_name: str, total_chunks: int) -> tuple[Path, int]:
    """
    流式合并文件分片

    Args:
        file_name: 文件名
        total_chunks: 总分片数

    Returns:
        (最终文件路径, 文件大小)
    """
    temp_dir = get_temp_file_dir(file_name)
    final_path = get_final_file_path(file_name)

    # 获取所有分片并按索引排序
    chunks = []
    for i in range(total_chunks):
        chunk_path = temp_dir / str(i)
        if chunk_path.exists():
            chunks.append((i, chunk_path))

    # 按索引排序
    chunks.sort(key=lambda x: x[0])

    # 流式写入目标文件
    file_size = 0
    with open(final_path, 'wb') as target_file:
        for chunk_index, chunk_path in chunks:
            with open(chunk_path, 'rb') as source_file:
                while True:
                    chunk = source_file.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    target_file.write(chunk)
                    file_size += len(chunk)

    return final_path, file_size


def cleanup_temp_files(file_name: str) -> bool:
    """
    清理临时文件

    Args:
        file_name: 文件名

    Returns:
        是否清理成功
    """
    temp_dir = get_temp_file_dir(file_name)
    if temp_dir.exists():
        try:
            shutil.rmtree(temp_dir)
            return True
        except Exception:
            return False
    return True
