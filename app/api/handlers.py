"""
全局异常处理器
"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from app.core.exceptions import FileUploadError, FileNotFound, IncompleteChunks


async def file_upload_exception_handler(request: Request, exc: FileUploadError):
    """文件上传异常处理器"""
    status_code = 500
    if isinstance(exc, FileNotFound):
        status_code = 404
    elif isinstance(exc, IncompleteChunks):
        status_code = 400

    return JSONResponse(
        status_code=status_code,
        content={
            "code": status_code,
            "message": exc.message,
            "data": None
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None
        }
    )
