'''
@author: chengshun
@date: 2025-10-24 
@version: v0.0.1
@description: 
    baseAgent.py
    实现基础的智能体抽象类
'''

from abc import ABC, abstractmethod 
import json
import pymysql

class BaseAgent(ABC):
    '''
    基础智能体，提供所有智能体agent的共有功能
    描述：
        定义智能体的基本属性和方法
    基本属性：
        - name: 智能体名称
        - session_id: 会话ID
        - json_path: json文件路径
        - prompt_file: 提示文件路径(system prompt)
        - mysql_host: mysql主机地址
        - mysql_user: mysql用户名
        - mysql_password: mysql密码
        - mysql_db: mysql数据库名称


    基本方法：
        数据：
            数据的读取
            数据的存储/保存-持久化
                - json加载读取
                - json保存写入
            数据库的访问（v0.0.1版本先做mysql）
                - sqlite
                - mysql
                - elasticsearch
                - redis

        初始化问诊机器人clinical_bot

    '''
    def __init__(self, name, session_id, json_path, prompt_file,
                 mysql_host, mysql_user, mysql_password, mysql_db):
        self.name = name
        self.session_id = session_id

        self.json_path = json_path
        self.prompt_file = prompt_file

        # MySQL数据库连接参数(V0.0.1版本先做mysql)
        # TODO: 优化数据库参数的导入 - 如从yaml/.env配置文件导入等方法
        self.mysql_host = mysql_host
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_db = mysql_db
    
    
    
    def load_json(self):
        try:
            with open(self.json_path, 'r') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            print(f"File '{self.json_path}' not found.")
            return None

    def save_json(self):
        pass

    def visit_mysql(self):
        '''
        访问数据库
        '''
        try:
            # 建立数据库连接
            connection = pymysql.connect(
                host=self.mysql_host,           
                user=self.mysql_user,           
                password=self.mysql_password,   
                database=self.mysql_db,         
                charset='utf8'                  # 字符集
            )
            # 创建游标对象
            cursor = connection.cursor()
            
            #测试连接
            # cursor.execute("SELECT VERSION()")
            # version = cursor.fetchone()
            # print(f"成功连接到MySQL数据库，版本: {version[0]}")

            # #测试数据库中内容
            # cursor.execute("SHOW TABLES")
            # #打印表中内容
            # for table in cursor:
            #     print(table)
            
            # 关闭游标和连接
            cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(f"连接MySQL数据库失败: {e}")
            return False


if __name__ == "__main__":
    test_agent = BaseAgent(
        name="TestAgent",
        session_id="session_001",
        json_path="data/test_data.json",
        prompt_file="prompts/test_prompt.txt",
        mysql_host="localhost",
        mysql_user="root",
        mysql_password="wo200146",
        mysql_db="book_libs"
    )
    print(test_agent.visit_mysql())