from mysql import connector
from base_config.config.config import config as conf


class MySQLClient:
    def __init__(
            self,
            host:str=conf.mysql.host,
            port:str=conf.mysql.port,
            user:str=conf.mysql.user,
            password:str=conf.mysql.password,
            charset:str=conf.mysql.charset,
            collection:str=conf.mysql.collection,
            sql_mode:str=conf.mysql.sql_mode,
            database:str=conf.mysql.database,
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.charset = charset
        self.collection = collection
        self.sql_mode = sql_mode
        self.database = database
        self.client = None



    def init(self):
        self.client = connector.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password,
        )


    def close(self):
        self.client.close()


mysql_client_management = MySQLClient()


if __name__ == "__main__":
    pass





