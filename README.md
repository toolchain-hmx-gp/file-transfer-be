# File Transfer - 文件分片上传服务

基于 FastAPI 的文件分片上传服务，支持大文件分片上传、合并和下载。

## 功能特性

- 支持大文件分片上传
- 流式文件合并，内存占用低
- 自动清理临时文件
- RESTful API 设计
- 完善的错误处理
- Swagger API 文档

## 项目结构

```
file-transfer/
├── app/
│   ├── api/
│   │   ├── deps.py          # 依赖注入
│   │   ├── handlers.py      # 全局异常处理器
│   │   └── v1/
│   │       └── endpoints/
│   │           └── file.py  # 文件上传端点
│   ├── core/
│   │   ├── config.py        # 配置常量
│   │   └── exceptions.py     # 自定义异常类
│   ├── models/
│   │   ├── schema/
│   │   │   └── file_transfer.py  # Pydantic 数据模型
│   │   ├── orm/            # 预留 ORM 模型
│   │   └── repository/     # 预留数据仓库
│   ├── services/
│   │   └── file_service.py # 文件服务逻辑
│   └── utils/
│       ├── file_utils.py    # 文件操作工具
│       └── path_utils.py    # 路径处理工具
├── files/                  # 上传完成的文件存放目录
├── temp/                   # 临时文件存放目录
├── main.py                 # 应用入口
└── pyproject.toml          # 项目依赖配置
```

## 环境要求

- Python >= 3.12
- uv (依赖管理工具)

## 安装

本项目使用 [uv](https://github.com/astral-sh/uv) 管理依赖和虚拟环境。

```bash
# 克隆项目
git clone <repository-url>
cd file-transfer

# 使用 uv 同步依赖（自动创建 .venv 虚拟环境）
uv sync

# 激活虚拟环境（可选，uv run 会自动使用）
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
```

## 配置

配置项在 `app/core/config.py` 中定义：

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `MAX_FILE_SIZE` | 1GB | 最大文件上传大小 |
| `CHUNK_SIZE` | 8KB | 文件合并缓冲区大小 |

## 运行

```bash
# 开发模式（支持热重载）- 使用 uv
uv run uvicorn main:app --reload --port 8000

# 或直接运行（已激活虚拟环境时）
python main.py

# 生产模式 - 使用 uv
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# 或使用已安装的 uvicorn 命令
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

启动后访问：
- API 服务：http://localhost:8000
- API 文档：http://localhost:8000/docs

## API 接口

### 1. 上传文件分片

**接口：** `POST /api/file/chunk`

**请求参数：**
- `file` (file): 文件分片数据
- `file_name` (str): 完整文件名
- `chunk_index` (int): 当前分片索引（从 0 开始）
- `total_chunks` (int): 总分片数量

**请求示例 (cURL):**
```bash
curl -X POST "http://localhost:8000/api/file/chunk" \
  -F "file=@chunk0.dat" \
  -F "file_name=example.zip" \
  -F "chunk_index=0" \
  -F "total_chunks=5"
```

**响应示例：**
```json
{
  "code": 200,
  "message": "分片上传成功",
  "data": null
}
```

### 2. 合并文件

**接口：** `POST /api/file/merge`

**请求参数：**
- `fileName` (str): 文件名
- `totalChunks` (int): 总分片数量

**请求示例 (cURL):**
```bash
curl -X POST "http://localhost:8000/api/file/merge" \
  -H "Content-Type: application/json" \
  -d '{"fileName":"example.zip","totalChunks":5}'
```

**响应示例：**
```json
{
  "code": 200,
  "message": "文件合并成功",
  "data": {
    "fileUrl": "http://localhost:8000/uploads/example.zip",
    "fileSize": 1048576
  }
}
```

### 3. 下载文件

**接口：** `GET /uploads/{file_name}`

**请求示例 (cURL):**
```bash
curl -O http://localhost:8000/uploads/example.zip
```

## 客户端上传示例

### JavaScript (前端分片上传)

```javascript
async function uploadFile(file) {
  const CHUNK_SIZE = 5 * 1024 * 1024; // 5MB 每片
  const totalChunks = Math.ceil(file.size / CHUNK_SIZE);

  // 上传所有分片
  for (let i = 0; i < totalChunks; i++) {
    const start = i * CHUNK_SIZE;
    const end = Math.min(start + CHUNK_SIZE, file.size);
    const chunk = file.slice(start, end);

    const formData = new FormData();
    formData.append('file', chunk);
    formData.append('file_name', file.name);
    formData.append('chunk_index', i);
    formData.append('total_chunks', totalChunks);

    await fetch('http://localhost:8000/api/file/chunk', {
      method: 'POST',
      body: formData
    });
  }

  // 合并文件
  const response = await fetch('http://localhost:8000/api/file/merge', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      fileName: file.name,
      totalChunks: totalChunks
    })
  });

  return await response.json();
}
```

### Python (客户端上传)

```python
import os
import requests

def upload_file(file_path, chunk_size=5*1024*1024):
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    total_chunks = (file_size + chunk_size - 1) // chunk_size

    # 上传所有分片
    with open(file_path, 'rb') as f:
        for i in range(total_chunks):
            chunk = f.read(chunk_size)
            requests.post('http://localhost:8000/api/file/chunk', files={
                'file': chunk,
                'file_name': (None, file_name),
                'chunk_index': (None, str(i)),
                'total_chunks': (None, str(total_chunks))
            })

    # 合并文件
    response = requests.post('http://localhost:8000/api/file/merge', json={
        'fileName': file_name,
        'totalChunks': total_chunks
    })

    return response.json()
```

## 错误处理

服务会返回标准的错误响应：

```json
{
  "code": 400,
  "message": "错误描述",
  "data": null
}
```

常见错误：
- `400`: 请求参数错误
- `404`: 文件不存在
- `422`: 数据验证失败
- `500`: 服务器内部错误

## 技术栈

- FastAPI - Web 框架
- Uvicorn - ASGI 服务器
- Pydantic - 数据验证
- Python-multipart - 文件上传支持
- uv - 快速的 Python 包管理器和虚拟环境工具

## 许可证

MIT License
