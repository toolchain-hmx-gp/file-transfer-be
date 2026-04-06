"""
文件分片上传服务
"""
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.v1.endpoints.file import router as file_router
from app.api.handlers import file_upload_exception_handler, http_exception_handler
from app.core.exceptions import FileUploadError
from app.utils.file_utils import ensure_directories
from app.middleware.cors import setup_cors_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时确保目录存在
    ensure_directories()
    yield
    # shutdown logic here if needed


app = FastAPI(title="文件分片上传服务", lifespan=lifespan)


# 配置 CORS 中间件
setup_cors_middleware(app)


# 注册异常处理器
app.add_exception_handler(FileUploadError, file_upload_exception_handler)


# 注册路由
app.include_router(file_router)


@app.get("/")
async def root():
    return {"message": "文件分片上传服务运行中"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
