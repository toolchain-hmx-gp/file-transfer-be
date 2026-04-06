"""
文件传输相关的Pydantic数据模型
"""
from pydantic import BaseModel


class FileChunkRequest(BaseModel):
    """文件分片上传请求"""
    file_name: str
    chunk_index: int
    total_chunks: int


class MergeRequest(BaseModel):
    """文件合并请求"""
    fileName: str
    totalChunks: int


class DataModel(BaseModel):
    """响应数据"""
    fileUrl: str
    fileSize: int


class ResponseModel(BaseModel):
    """统一响应格式"""
    code: int
    message: str
    data: DataModel | None = None
