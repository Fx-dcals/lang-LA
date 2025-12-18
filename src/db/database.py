"""
数据库连接和初始化模块
"""
import os
import pymysql
from dotenv import load_dotenv
from contextlib import contextmanager
from typing import Optional

load_dotenv()

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'lang_la'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


@contextmanager
def get_db_connection():
    """获取数据库连接的上下文管理器"""
    conn = None
    try:
        conn = pymysql.connect(**DB_CONFIG)
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


def init_database():
    """初始化数据库表结构"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 创建学习点记录表
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS learning_points (
            id INT AUTO_INCREMENT PRIMARY KEY,
            thread_id VARCHAR(255) NOT NULL,
            topic VARCHAR(500) NOT NULL,
            difficulty_level ENUM('easy', 'medium', 'hard') NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_thread_id (thread_id),
            INDEX idx_topic (topic(255)),
            INDEX idx_difficulty (difficulty_level),
            INDEX idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        cursor.execute(create_table_sql)
        conn.commit()
        print("数据库表初始化完成")


if __name__ == "__main__":
    init_database()

