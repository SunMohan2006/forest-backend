-- ============================================
-- 林业资源信息管理后台 — 数据库初始化脚本
-- 数据库名: forest_db
-- ============================================

CREATE DATABASE IF NOT EXISTS forest_db DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE forest_db;

-- 1. 用户表
CREATE TABLE IF NOT EXISTS user (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(50)  NOT NULL UNIQUE COMMENT '用户名',
    password    VARCHAR(255) NOT NULL COMMENT '密码（bcrypt加密）',
    role        VARCHAR(20)  NOT NULL DEFAULT 'USER' COMMENT '角色: ADMIN / USER',
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 2. 林地表
CREATE TABLE IF NOT EXISTS forest_land (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL COMMENT '林地名称',
    area        DECIMAL(10,2) COMMENT '面积（亩）',
    location    VARCHAR(255) COMMENT '地理位置',
    land_type   VARCHAR(50)  COMMENT '类型: 用材林/防护林/经济林/薪炭林/特用林',
    description TEXT COMMENT '描述',
    status      VARCHAR(20)  NOT NULL DEFAULT 'ACTIVE' COMMENT '状态: ACTIVE/INACTIVE',
    created_by  BIGINT COMMENT '创建人用户ID',
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at  DATETIME     ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (created_by) REFERENCES user(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='林地表';

-- 3. 遥感图片表
CREATE TABLE IF NOT EXISTS forest_image (
    id            BIGINT AUTO_INCREMENT PRIMARY KEY,
    land_id       BIGINT NOT NULL COMMENT '所属林地ID',
    image_url     VARCHAR(500) NOT NULL COMMENT '图片存储路径',
    original_name VARCHAR(255) COMMENT '原始文件名',
    file_size     BIGINT COMMENT '文件大小（字节）',
    uploaded_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',
    FOREIGN KEY (land_id) REFERENCES forest_land(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='遥感图片表';

-- 4. 操作日志表
CREATE TABLE IF NOT EXISTS operation_log (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id     BIGINT COMMENT '操作人用户ID',
    action      VARCHAR(50)  COMMENT '操作类型: CREATE/UPDATE/DELETE',
    target      VARCHAR(100) COMMENT '操作对象: forest_land/forest_image',
    target_id   BIGINT COMMENT '操作对象ID',
    detail      VARCHAR(500) COMMENT '操作详情',
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='操作日志表';

-- 插入测试管理员账号（密码: admin123，bcrypt加密）
INSERT INTO user (username, password, role) VALUES
('admin', '$2b$12$LJ3m4ys3Lk0TSwHCpNqrDOZ4b0Z.YbF6JV/lqGwUOFqW6MD7qJpXq', 'ADMIN');
