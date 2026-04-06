"""
文件上传端点
"""
from fastapi import APIRouter, UploadFile, Form, File, HTTPException, Depends
from fastapi.responses import FileResponse
from pathlib import Path

from app.models.schema.file_transfer import ResponseModel, MergeRequest
from app.core.exceptions import FileUploadError, FileNotFound, IncompleteChunks
from app.api.deps import get_file_service


router = APIRouter()


@router.post("/api/file/chunk")
async def upload_chunk(
    file: UploadFile = File(...),
    file_name: str = Form(...),
    chunk_index: int = Form(...),
    total_chunks: int = Form(...),
    file_service = Depends(get_file_service)
):
    """
    上传文件分片
    """
    return await file_service.upload_chunk(
        file_stream=file.file,
        file_name=file_name,
        chunk_index=chunk_index,
        total_chunks=total_chunks
    )


@router.post("/api/file/merge")
async def merge_file(
    request: MergeRequest,
    file_service = Depends(get_file_service)
):
    """
    合并文件文件分片
    """
    file_name = request.fileName
    total_chunks = request.totalChunks

    return await file_service.merge_file(file_name, total_chunks)


@router.get("/uploads/{file_name}")
async def get_file(file_name: str):
    """
    获取上传的文件
    """
    from app.core.config import UPLOADS_DIR, FILES_DIR

    file_path = UPLOADS_DIR / file_name
    if not file_path.exists():
        file_path = FILES_DIR / file_name

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件未找到")

    return FileResponse(file_path)
