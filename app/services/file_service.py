"""
文件服务
"""
from app.core.exceptions import FileNotFound, IncompleteChunks
from app.models.schema.file_transfer import ResponseModel, DataModel
from app.utils.path_utils import get_file_url
from app.utils.file_utils import (
    save_chunk,
    get_temp_chunk_path,
    validate_chunks,
    merge_chunks_stream,
    cleanup_temp_files
)


class FileService:
    """文件服务"""

    async def upload_chunk(
        self,
        file_stream,
        file_name: str,
        chunk_index: int,
        total_chunks: int
    ) -> ResponseModel:
        """
        上传文件分片

        Args:
            file_stream: 文件流
            file_name: 文件名
            chunk_index: 分片索引
            total_chunks: 总分片数

        Returns:
            响应模型
        """
        chunk_path = get_temp_chunk_path(file_name, chunk_index)
        save_chunk(file_stream, chunk_path)

        return ResponseModel(
            code=200,
            message=f"分片 {chunk_index} 上传成功",
            data=None
        )

    async def validate_chunks(
        self,
        file_name: str,
        total_chunks: int
    ) -> tuple[bool, list[int]]:
        """
        验证分片完整性

        Args:
            file_name: 文件名
            total_chunks: 总分片数

        Returns:
            (是否完整, 缺失的分片索引列表)
        """
        return validate_chunks(file_name, total_chunks)

    async def merge_file(
        self,
        file_name: str,
        total_chunks: int
    ) -> ResponseModel:
        """
        合并文件分片

        Args:
            file_name: 文件名
            total_chunks: 总分片数

        Returns:
            响应模型，包含文件URL和大小
        """
        from app.utils.path_utils import get_temp_file_dir

        # 检查临时目录是否存在
        temp_dir = get_temp_file_dir(file_name)
        if not temp_dir.exists():
            raise FileNotFound(f"文件未找到，请先上传分片")

        # 验证分片完整性
        is_complete, missing_chunks = await self.validate_chunks(file_name, total_chunks)
        if not is_complete:
            raise IncompleteChunks(missing_chunks)

        # 合并分片
        final_path, file_size = merge_chunks_stream(file_name, total_chunks)

        # 清理临时文件
        cleanup_temp_files(file_name)

        return ResponseModel(
            code=200,
            message="文件合并成功",
            data=DataModel(
                fileUrl=get_file_url(file_name),
                fileSize=file_size
            )
        )

    async def cleanup_temp(self, file_name: str) -> bool:
        """
        清理临时文件

        Args:
            file_name: 文件名

        Returns:
            是否清理成功
        """
        return cleanup_temp_files(file_name)
