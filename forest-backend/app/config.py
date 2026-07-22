"""
应用配置 — 集中管理数据库连接、JWT密钥、上传路径等配置项
"""
import os


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
            # SQLite 文件数据库，自动创建在项目根目录
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "forest.db")
            return f"sqlite:///{db_path}"

    # ── JWT ──
    SECRET_KEY: str = os.getenv("SECRET_KEY", "forest-backend-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24小时

    # ── 文件上传 ──
    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB


settings = Settings()
