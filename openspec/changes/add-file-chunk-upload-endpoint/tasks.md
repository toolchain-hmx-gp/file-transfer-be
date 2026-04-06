## 1. 项目结构搭建

- [x] 1.1 创建FastAPI项目基础结构
- [x] 1.2 创建temp和files目录
- [x] 1.3 安装FastAPI及必要依赖

## 2. MVC分层架构搭建

### 2.1 创建app目录结构
- [x] 2.1.1 创建app/__init__.py
- [x] 2.1.2 创建app/api/目录及初始化文件
- [x] 2.1.3 创建app/api/v1/目录及初始化文件
- [x] 2.1.4 创建app/api/v1/endpoints/目录及初始化文件
- [x] 2.1.5 创建app/core/目录及初始化文件
- [x] 2.1.6 创建app/models/目录及初始化文件
- [x] 2.1.7 创建app/services/目录及初始化文件
- [x] 2.1.8 创建app/utils/目录及初始化文件

### 2.2 Core层实现
- [x] 2.2.1 创建core/config.py，定义配置常量（TEMP_DIR, FILES_DIR, UPLOADS_DIR等）
- [x] 2.2.2 创建core/exceptions.py，定义自定义异常类
  - FileUploadError（基类）
  - FileNotFound
  - IncompleteChunks
  - MergeFailed
  - CleanupFailed

### 2.3 Models层实现
- [x] 2.3.1 创建models/schema目录，定义Pydantic数据模型
  - FileChunkRequest（文件分片上传请求）
  - MergeRequest（文件合并请求）
  - DataModel（响应数据）
  - ResponseModel（统一响应格式）
- [x] 2.3.2 创建models/orm目录（预留ORM模型）
- [x] 2.3.3 创建models/repository目录（预留数据库Repository）

### 2.4 Utils层实现
- [x] 2.4.1 创建utils/path_utils.py，实现路径处理工具
  - get_temp_file_dir()
  - get_temp_chunk_path()
  - get_final_file_path()
  - get_file_url()
- [x] 2.4.2 创建utils/file_utils.py，实现文件操作工具
  - save_chunk() - 保存分片文件
  - validate_chunks() - 验证分片完整性
  - merge_chunks_stream() - 流式合并分片
  - cleanup_temp_files() - 清理临时文件

### 2.5 Service层实现
- [x] 2.5.1 创建services/file_service.py，实现FileService类
  - upload_chunk() - 上传文件分片
  - validate_chunks() - 验证分片完整性（调用utils）
  - merge_file() - 合并文件分片
  - cleanup_temp() - 清理临时文件

### 2.6 API层实现
- [x] 2.6.1 创建api/deps.py，实现依赖注入
  - get_file_service() - 注入FileService实例
- [x] 2.6.2 创建api/v1/endpoints/file.py，实现文件上传端点
  - POST /api/file/chunk - 上传文件分片
  - POST /api/file/merge - 合并文件
  - GET /uploads/{file_name} - 获取上传的文件

## 3. 错误处理实现

- [x] 3.1 在API层添加全局异常处理器
- [x] 3.2 实现FileNotFound异常处理
- [x] 3.3 实现IncompleteChunks异常处理
- [x] 3.4 实现MergeFailed异常处理
- [x] 3.5 实现CleanupFailed异常处理

## 4. 更新主应用文件

- [x] 4.1 更新main.py，使用新的分层架构
- [x] 4.2 注册API路由
- [x] 4.3 配置全局异常处理器
- [x] 4.4 更新启动事件

## 5. 迁移旧代码

- [x] 5.1 迁移models.py中的模型到models/schema.py
- [x] 5.2 迁移utils.py中的工具函数到相应层
- [x] 5.3 删除旧的models.py、utils.py文件（main.py已备份为main.py.backup）

## 6. 测试和验证

- [x] 6.1 测试单个分片上传功能
- [x] 6.2 测试多个分片上传功能
- [x] 6.3 测试文件合并功能
- [x] 6.4 测试分片不完整的错误场景
- [x] 6.5 测试大文件上传（验证流式处理）
- [x] 6.6 测试临时文件清理功能
- [x] 6.7 测试各种异常情况（文件不存在、权限错误等）
