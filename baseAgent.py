'''
@author: chengshun
@date: 2025-10-24 
@version: v0.0.1
@description: 
    baseAgent.py
    实现基础的智能体抽象类
'''

from abc import ABC, abstractmethod 
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # 导入提示模板相关类
import json
import pymysql
from langchain_openai import ChatOpenAI #后续考虑使用import openai
from langchain_core.runnables.history import RunnableWithMessageHistory  # 导入带有消息历史的可运行类
from langchain_core.messages import HumanMessage


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
    def __init__(self, name, session_id, 
                 llm_config,
                 json_path, prompt_file,
                 mysql_host, mysql_user, mysql_password, mysql_db):
        self.name = name
        self.session_id = session_id


        self.llm_config = llm_config    

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
        
    ## clinicalBot相关 ##
    def create_clinicalBot(self):
        '''
        初始化问诊机器人
        '''
        system_prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompt_file),
            MessagesPlaceholder(variable_name="history"),
        ])

        self.clinicalBot = system_prompt | ChatOpenAI(
            model=self.llm_config['model'],
            temperature=self.llm_config['temperature'],
        )

        self.clinicalBot_with_history = RunnableWithMessageHistory(
            self.clinicalBot,
            #TODO:待做功能 - get_session_history
            self.get_session_history #可以直接使用langgraph的get_session_history方法或者自己写一个get_session_history方法
        )

    def chat_with_history(self, user_input, session_id=None):
        '''
        处理用户输入，生成包含聊天历史的回复
        参数:
            user_input (str): 用户输入的消息
            session_id (str): 会话ID，默认为None
        返回:
            str: 聊天机器人的回复
        '''
        if session_id is None:
            session_id = self.session_id
        
        response = self.clinicalBot_with_history.invoke(
            [HumanMessage(content=user_input)],
            {"configurable": {"session_id": session_id}}
        )
        return response.content
    
    @abstractmethod
    def process_patient_data(self, patient_data):
        '''
        处理对应患者数据
        '''
        pass




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