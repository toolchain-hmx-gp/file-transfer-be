"""
自定义异常
"""


class FileUploadError(Exception):
    """文件上传错误基类"""

    def __init__(self, message: str = "文件上传失败"):
        self.message = message
        super().__init__(self.message)


class FileNotFound(FileUploadError):
    """文件不存在"""

    def __init__(self, message: str = "文件不存在"):
        self.message = message
        super().__init__(self.message)


class IncompleteChunks(FileUploadError):
    """分片不完整"""

    def __init__(self, missing_chunks: list[int] | None = None):
        self.missing_chunks = missing_chunks or []
        self.message = f"分片不完整，缺失的分片索引: {self.missing_chunks}"
        super().__init__(self.message)


class MergeFailed(FileUploadError):
    """文件合并失败"""

    def __init__(self, message: str = "文件合并失败"):
        self.message = message
        super().__init__(self.message)


class CleanupFailed(FileUploadError):
    """临时文件清理失败"""

    def __init__(self, message: str = "临时文件清理失败"):
        self.message = message
        super().__init__(self.message)
