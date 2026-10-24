from langchain.tools import tool
from base_config.config.config import config as conf
from base_config.logger.logger import logger
from app.client_management.mysql_client import mysql_client_management
from api.monitor.monitor import monitor

mysql_client_management.init()
client = mysql_client_management.client


@tool
def list_sql_tables():
    """
    查询数据库内的所有表
    :return: 返回数据库内所有的表名，CSV格式数据；工具报错时，返回报错信息
    """
    monitor.report_tool(tool_name="查询数据库所有表:list_sql_tables", args={})
    try:
        cursor = client.cursor()
        sql = f"USE {conf.mysql.database}"
        cursor.execute(sql)
        sql = f"SHOW TABLES"
        cursor.execute(sql)
        response = cursor.fetchall()
        if not response:
            return "没有可用的表"
        result = [ans[0] for ans in response]
        logger.info(f"db_tables_result:{result}")
        return result
    except Exception as e:
        logger.error(str(e))
        return str(e)


@tool
def get_table_data(table_name:str):
    """
    获取表内容信息
    :param table_name: 需要获取相关表信息的表名
    :return: 返回表内的数据信息，CSV格式数据；工具报错时，返回报错信息
    """
    monitor.report_tool(tool_name="获取数据库数据:get_table_data",args={"table_name":table_name})
    try:
        #注入风险
        cursor = client.cursor()
        sql = "USE deepsearch_db"
        cursor.execute(sql)
        sql = f"SELECT * FROM {table_name} Limit 100"
        cursor.execute(sql)
        response = cursor.description
        if not response:
            return f"数据库{table_name}表里无数据"
        title = [ans[0] for ans in response]
        response_all = cursor.fetchall()
        content = [",".join(map(str,row)) for row in response_all]
        header = ",".join(title)
        contents = "\n".join(content)
        logger.info(f"db_tables_data:{header}\n{contents}")
        return f"{header}\n{contents}"
    except Exception as e:
        logger.error(str(e))
        return str(e)



@tool
def execute_sql_query(query:str):
    """
    执行自定义SQL查询
    注意：查询之前先通过list_sql_tables工具获取表名，再通过get_table_data获取表的数据格式和表结构
    :param query: 要执行的自定义SQL语句
    :return: CSV格式数据,工具报错时，返回报错信息
    """
    monitor.report_tool(tool_name="查询自定义SQL:execute_sql_query",args={"generate - sql":query})
    cursor = client.cursor()
    sql = "USE deepsearch_db"
    cursor.execute(sql)
    """
    try:
        logger.info("校验SQL")
        cursor.execute(f"EXPLAIN {query}")
    except Exception as e:
        logger.error(str(e))
        return f"查询语句有误:{str(e)}"
    """
    try:
        logger.info("SQL查询")
        cursor.execute(query)
        response = cursor.description
        if not response:
            return "没有查询到相关内容"
        logger.info(f"response:{response}")
        title = [ans[0] for ans in response]
        header = ",".join(title)
        response_all = cursor.fetchall()
        content = [",".join(map(str,row)) for row in response_all]

        contents = "\n".join(content)
        logger.info(f"生成SQL的检索答案:{header}\n{contents}")
        return f"{header}\n{contents}"
    except Exception as e:
        logger.error(str(e))
        return str(e)


if __name__ == "__main__":
    a = get_table_data('drugs')
    print(a)

