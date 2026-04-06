## Context

当前系统需要支持大文件上传功能，避免一次性加载大文件到内存中导致内存溢出。前端采用分片上传的方式将文件拆分成多个小块，后端需要接收这些分片并重组为完整文件。

## 技术栈

- Web框架：FastAPI
- 文件存储：本地文件系统
- 临时目录：项目根目录下的 `temp/`
- 最终文件目录：项目根目录下的 `files/`
- 架构模式：MVC分层架构

## Goals / Non-Goals

**Goals:**
- 实现大文件的分片上传和重组功能
- 使用流式处理避免内存溢出
- 提供清晰的API接口供前端调用
- 确保文件完整性和正确性
- 采用MVC分层架构组织代码

**Non-Goals:**
- 文件加密功能
- 断点续传功能
- 云存储集成
- 文件去重

## Decisions

### 1. 使用FastAPI作为Web框架
**选择原因**：FastAPI是现代高性能的Python Web框架，具有异步支持、自动API文档生成、类型提示等优点，适合处理文件上传等I/O密集型操作。

**替代方案考虑**：
- Flask：性能不如FastAPI，需要额外配置异步支持
- Django：过于重量级，对于简单的文件上传功能来说太复杂

### 2. 采用MVC分层架构
**选择原因**：将代码按职责分层，提高可维护性、可测试性和可扩展性。

**分层说明**：
- **API层**：路由控制器，处理HTTP请求/响应
- **Service层**：业务逻辑，处理文件上传的核心逻辑
- **Models层**：
  - `schema.py`: Pydantic请求/响应模型
  - `orm.py`: ORM模型（预留）
  - `factory.py`: 数据库操作工厂（预留）
- **Utils层**：通用工具函数
- **Core层**：配置和异常定义

### 3. 临时文件存储策略
**选择原因**：将每个上传文件的分片存储在 `temp/<file_name>/` 下的独立目录中，便于管理同一文件的所有分片，并在合并后整体清理。

**替代方案考虑**：
- 将所有分片放在同一目录：会导致文件管理混乱，难以区分不同文件
- 使用内存存储：对于大文件会导致内存溢出

### 4. 文件流式处理
**选择原因**：使用文件流（pipe）将分片依次写入目标文件，避免将整个文件加载到内存中，特别适合处理大文件。

**替代方案考虑**：
- 一次性读取所有分片到内存再写入：会导致内存溢出
- 同步读写：性能较差，FastAPI支持异步操作

## 架构设计

### MVC分层架构

```
┌─────────────────────────────────────────────────────────────────┐
│                          分层架构                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Client                                                          │
│      │                                                            │
│      ▼                                                            │
│   ┌─────────────────────┐                                        │
│   │  API Layer           │  api/v1/endpoints/file.py            │
│   │                      │  - 路由定义                           │
│   │  路由控制器           │  - 请求验证                           │
│   │                      │  - 调用Service                        │
│   │                      │  - 响应转换                           │
│   └─────────────────────┘                                        │
│      │                                                            │
│      ▼                                                            │
│   ┌─────────────────────┐                                        │
│   │  Service Layer       │  services/file_service.py             │
│   │                      │                                        │
│   │  业务逻辑             │  - upload_chunk()                   │
│   │                      │  - validate_chunks()                │
│   │  FileService         │  - merge_file()                     │
│   │                      │  - cleanup_temp()                   │
│   └─────────────────────┘                                        │
│      │                                                            │
│      ▼                                                            │
│   ┌─────────────────────┐                                        │
│   │  Utils Layer         │  utils/                               │
│   │                      │  - path_utils.py (路径计算)           │
│   │  通用工具             │  - file_utils.py (文件读写)           │
│   └─────────────────────┘                                        │
│                                                                  │
│   ───────────────── Models层 ─────────────────                   │
│                                                                  │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐                      │
│   │   orm    │  │ factory  │  │  schema  │                      │
│   │          │  │          │  │          │                      │
│   │ ORM模型   │  │ DB工厂   │  │ 请求/响应 │                      │
│   │ (预留)    │  │ (预留)    │  │ 模型      │                      │
│   └──────────┘  └──────────┘  └──────────┘                      │
│                                                                  │
│   ┌─────────────────────┐  ┌─────────────────────┐             │
│   │      core          │  │     exceptions      │             │
│   │      config.py     │  │       .py          │             │
│   └─────────────────────┘  └─────────────────────┘             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 目录结构

```
app/
├── __init__.py
├── api/
│   ├── __init__.py
│   ├── deps.py            # 依赖注入
│   └── v1/
│       ├── __init__.py
│       └── endpoints/
│           ├── __init__.py
│           └── file.py    # 文件上传端点
│
├── core/
│   ├── __init__.py
│   ├── config.py          # 配置常量（TEMP_DIR, FILES_DIR等）
│   └── exceptions.py       # 自定义异常
│
├── models/
│   ├── __init__.py
│   ├── orm.py             # ORM模型（预留）
│   ├── factory.py         # 数据库操作工厂（预留）
│   └── schema.py          # Pydantic请求/响应模型
│
├── services/
│   ├── __init__.py
│   └── file_service.py    # FileService类
│
└── utils/
    ├── __init__.py
    ├── path_utils.py       # 路径处理工具
    └── file_utils.py       # 文件操作工具
```

### 核心类和接口

#### models/schema.py

```python
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
```

#### core/exceptions.py

```python
class FileUploadError(Exception):
    """文件上传错误基类"""

class FileNotFound(FileUploadError):
    """文件不存在"""

class IncompleteChunks(FileUploadError):
    """分片不完整"""

class MergeFailed(FileUploadError):
    """文件合并失败"""

class CleanupFailed(FileUploadError):
    """临时文件清理失败"""
```

#### services/file_service.py

```python
class FileService:
    """文件服务"""

    async def upload_chunk(
        self,
        file_stream,
        file_name: str,
        chunk_index: int,
        total_chunks: int
    ) -> None:
        """上传文件分片"""

    async def validate_chunks(
        self,
        file_name: str,
        total_chunks: int
    ) -> tuple[bool, list[int]]:
        """验证分片完整性"""

    async def merge_file(
        self,
        file_name: str,
        total_chunks: int
    ) -> tuple[str, int]:
        """合并文件分片"""

    async def cleanup_temp(
        self,
        file_name: str
    ) -> None:
        """清理临时文件"""
```

#### utils/path_utils.py

```python
def get_temp_file_dir(file_name: str) -> Path
def get_temp_chunk_path(file_name: str, chunk_index: int) -> Path
def get_final_file_path(file_name: str) -> Path
def get_file_url(file_name: str) -> str
```

#### utils/file_utils.py

```python
def save_chunk(file_stream, chunk_path: Path) -> None
def merge_chunks_stream(file_name: str, total_chunks: int) -> tuple[Path, int]
def cleanup_temp_files(file_name: str) -> bool
```

### API端点设计

1. **POST /api/file/chunk**
   - 功能：上传单个文件分片
   - 请求方式：FormData
   - 参数：
     - `file`: 文件流
     - `file_name`: 文件名
     - `chunk_index`: 分片索引
     - `total_chunks`: 总分片数
   - 响应：成功或失败信息

2. **POST /api/file/merge**
   - 功能：合并所有分片为完整文件
   - 请求方式：JSON
   - 请求参数：
     - `fileName`: 文件名
     - `totalChunks`: 总分片数
   - 响应：
     ```json
     {
       "code": 200,
       "message": "文件合并成功",
       "data": {
         "fileUrl": "/uploads/文件名",
         "fileSize": 文件大小（字节）
       }
     }
     ```

### 文件处理流程

1. **上传分片阶段**：
   - 前端调用 `/api/file/chunk` 上传分片
   - 后端在 `temp/<file_name>/` 目录下创建分片文件，命名为 `{chunk_index}`
   - 每个分片独立存储

2. **合并文件阶段**：
   - 前端调用 `/api/file/merge` 请求合并，发送fileName和totalChunks
   - 后端检查临时文件夹是否存在
   - 后端校验分片完整性（检查分片数量是否等于totalChunks）
   - 按分片索引排序所有分片
   - 在 `files/` 目录下创建目标文件的可写流
   - 使用管道将分片依次写入目标文件
   - 计算合并后的文件大小
   - 删除 `temp/<file_name>/` 临时目录
   - 返回包含fileUrl和fileSize的成功响应

## Risks / Trade-offs

### 风险

**[并发上传冲突]** → 使用文件名作为临时目录的唯一标识，同一文件的同时上传会产生冲突
**缓解措施**：在上传前检查是否已有同名文件的临时目录存在，或生成唯一标识符

**[磁盘空间不足]** → 临时文件和最终文件占用磁盘空间
**缓解措施**：在合并前检查可用磁盘空间，设置最大文件大小限制

**[分片丢失]** → 网络传输过程中某些分片可能丢失
**缓解措施**：前端实现重试机制，后端在校验时返回缺失的分片索引信息

**[文件权限问题]** → 临时目录和目标目录可能没有写入权限
**缓解措施**：在启动时检查并创建必要的目录，设置适当的权限

### 权衡

**内存使用 vs 性能**：选择流式处理牺牲了一定的性能（相比内存操作），但获得了更好的内存管理，能够处理更大的文件

**简单性 vs 可靠性**：使用本地文件系统实现简单，但相比专业存储服务缺少分布式支持。对于单机应用场景足够。

**代码结构 vs 开发速度**：采用MVC分层架构增加了代码结构的复杂度，但提高了可维护性和可测试性，适合长期维护的项目。

## 安全考虑

1. **文件名验证**：验证文件名，防止路径遍历攻击
2. **文件大小限制**：设置最大文件大小限制
3. **文件类型验证**：可选：验证文件MIME类型
4. **清理机制**：设置定时任务清理过期的临时文件

## Open Questions

- 是否需要支持断点续传？
- 是否需要实现上传进度查询接口？
- 是否需要限制同时上传的文件数量？
- 是否需要实现文件去重功能？
