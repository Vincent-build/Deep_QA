from sqlalchemy import create_engine,text,inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncEngine
from app.db_orm.model.orm_model import DrugsMySQL,InventoryMySQL,SalesRecordsMySQL
from base_config.config.config import config as conf
from typing import Optional,Union
from app.db_orm.model.base import Base


class MySQLOperator:
    def __init__(
            self,
            host=conf.mysql.host,
            port=conf.mysql.port,
            user=conf.mysql.user,
            password=conf.mysql.password,
            database=conf.mysql.database,
            charset=conf.mysql.charset,
            table1 = conf.mysql.table1,
            table2 = conf.mysql.table2,
            table3 = conf.mysql.table3,
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.engine:Optional[AsyncEngine]
        self.session_factory = None
        self.table1 = table1
        self.table2 = table2
        self.table3 = table3
        self._init()


    def _get_url(self):
        result = self._check_database()
        if result:
            return f"mysql+asyncmy://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?{self.charset}"
        else:
            return f"mysql+asyncmy://{self.user}:{self.password}@{self.host}:{self.port}"


    def _check_database(self):
        url = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}"
        engine = create_engine(url)
        session = sessionmaker(engine)
        sql = f"CREATE DATABASE IF NOT EXISTS {self.database}"
        with session() as session:
            session.execute(text(sql))
            session.commit()
            sql = f"USE {self.database}"
            session.execute(text(sql))
            sql = f"SELECT DATABASE()"
            response = session.execute(text(sql))
            result = response.fetchone()[0]
        if result == self.database:
            print(f"加载{self.database}数据库")
            session.close()
            engine.dispose()
            return True
        else:
            print(f"创建数据库失败")
            session.close()
            engine.dispose()
            return None


    def _init(self):
        url = self._get_url()
        self.engine = create_async_engine(url)
        self.session_factory = async_sessionmaker(self.engine,autoflush=True,expire_on_commit=False)


    def check_table(self):
        print("检查数据库表...")
        url = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?{self.charset}"
        engine = create_engine(url)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        table_needs = [self.table1,self.table2,self.table3]
        if len(tables) != len(table_needs) or self.table1 not in tables or self.table2 not in tables or self.table3 not in tables:
            print("数据库表缺失")
            Base.metadata.create_all(engine)
            print("表创建完成")
        engine.dispose()


    async def update_data(self,data_list:Union[list[DrugsMySQL],list[InventoryMySQL],list[SalesRecordsMySQL]]):
        async with self.session_factory() as session:
            session.add_all(data_list)
            await session.commit()
            print("数据写入成功")


    async def close(self):
        await self.session_factory.close()
        await self.engine.dispose()


mysql_operated = MySQLOperator()

if __name__ == "__main__":
    pass
    #mysql_operated.check_table()







