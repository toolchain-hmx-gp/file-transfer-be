"""
CORS 跨域中间件配置
"""
from fastapi.middleware.cors import CORSMiddleware


def setup_cors_middleware(app):
    """
    配置 CORS 中间件

    Args:
        app: FastAPI 应用实例
    """
    app.add_middleware(
        CORSMiddleware,
        # 允许的源列表，开发环境使用 * 允许所有源
        # 生产环境建议指定具体域名，如: ["http://localhost:3000", "https://example.com"]
        allow_origins=["*"],

        # 允许的域名模式（正则表达式），可选
        # allow_origin_regex=r"https://.*\.example\.com",

        # 允许携带凭证（cookies、authorization headers 等）
        # 如果设置为 True，allow_origins 不能设置为 "*"
        allow_credentials=False,

        # 允许的 HTTP 方法
        allow_methods=["*"],

        # 允许的请求头
        allow_headers=["*"],

        # 允许浏览器暴露给前端的响应头
        expose_headers=["*"],

        # 预检请求缓存时间（秒）
        max_age=600,
    )
