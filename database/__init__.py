from database.db_managers import *

from injector import Binder, Module


class DatabaseModule(Module):
    def configure(self, binder: Binder):
        binder.bind(OracleDbManager, OracleDbManager)
        binder.bind(PostgresDbManager, PostgresDbManager)
