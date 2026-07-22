"""
应用配置 — 集中管理数据库连接、JWT密钥、上传路径等配置项
"""
import os
import secrets


def _get_secret_key() -> str:
    """
    JWT 签名密钥获取策略（按优先级）：
    1. 环境变量 SECRET_KEY（生产环境推荐）
    2. .secret_key 文件（开发环境持久化，重启不失效）
    3. 随机生成 → 写入 .secret_key 文件（首次启动自动创建）
    """
    env_key = os.getenv("SECRET_KEY")
    if env_key:
        return env_key

    key_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".secret_key")
    if os.path.exists(key_file):
        with open(key_file, "r") as f:
            return f.read().strip()

    # 首次启动：生成强随机密钥并持久化
    key = secrets.token_urlsafe(32)
    with open(key_file, "w") as f:
        f.write(key)
    print(f"[SECURITY] SECRET_KEY 未设置，已随机生成并保存到 {key_file}")
    print("[SECURITY] 生产环境请通过环境变量 SECRET_KEY 设置固定密钥")
    return key


class Settings:
    # ── 数据库（设 DB_TYPE=mysql 则连 MySQL，默认 SQLite 免配置直接跑） ──
    DB_TYPE: str = os.getenv("DB_TYPE", "sqlite")

    # MySQL 配置（仅 DB_TYPE=mysql 时生效）
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "root")
    DB_NAME: str = os.getenv("DB_NAME", "forest_db")

    @property
    def DATABASE_URL(self) -> str:
        """数据库连接地址：默认 SQLite（免配置），设 DB_TYPE=mysql 则用 MySQL"""
        if self.DB_TYPE == "mysql":
            return (
                f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
                "?charset=utf8mb4"
            )
        else:
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "forest.db")
            return f"sqlite:///{db_path}"

    # ── JWT ──
    SECRET_KEY: str = _get_secret_key()
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24小时

    # ── 文件上传 ──
    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB


settings = Settings()
