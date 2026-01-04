"""
数据库连接模块
负责PostgreSQL数据库连接和查询
"""

import psycopg2
import pandas as pd
from typing import Dict, List, Optional
from loguru import logger


class DatabaseConnector:
    """数据库连接器"""

    def __init__(self, config: Dict):
        """
        初始化数据库连接器

        Args:
            config: 配置字典,包含数据库连接信息
        """
        self.config = config['database']
        self.connection = None

    def connect(self):
        """建立数据库连接"""
        try:
            logger.info(f"连接数据库: {self.config['host']}:{self.config['port']}")
            self.connection = psycopg2.connect(
                host=self.config['host'],
                port=self.config['port'],
                database=self.config['database'],
                user=self.config['user'],
                password=self.config['password']
            )
            logger.info("数据库连接成功 ✓")
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise

    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()
            logger.info("数据库连接已关闭")

    def execute_query(self, query: str, params: Optional[tuple] = None) -> pd.DataFrame:
        """
        执行SQL查询并返回DataFrame

        Args:
            query: SQL查询语句
            params: 查询参数

        Returns:
            pd.DataFrame: 查询结果
        """
        if not self.connection:
            raise ConnectionError("数据库未连接")

        try:
            logger.info(f"执行SQL查询...")
            logger.debug(f"SQL: {query}")

            df = pd.read_sql_query(query, self.connection, params=params)

            logger.info(f"查询完成: 返回 {len(df)} 行数据")
            return df

        except Exception as e:
            logger.error(f"查询执行失败: {e}")
            raise

    def table_exists(self, schema: str, table_name: str) -> bool:
        """
        检查表是否存在

        Args:
            schema: Schema名称
            table_name: 表名

        Returns:
            bool: 表是否存在
        """
        query = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = %s
            AND table_name = %s
        );
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (schema, table_name))
            exists = cursor.fetchone()[0]
            cursor.close()
            return exists
        except Exception as e:
            logger.error(f"检查表是否存在失败: {e}")
            return False

    def get_table_columns(self, schema: str, table_name: str) -> List[str]:
        """
        获取表的列名

        Args:
            schema: Schema名称
            table_name: 表名

        Returns:
            List[str]: 列名列表
        """
        query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = %s
        AND table_name = %s
        ORDER BY ordinal_position;
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (schema, table_name))
            columns = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return columns
        except Exception as e:
            logger.error(f"获取表列名失败: {e}")
            return []
