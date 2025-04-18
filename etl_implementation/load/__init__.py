from database import OracleDbManager
from etl import ILoader
from etl_implementation.load.CSVLoader import CSVLoader
from etl_implementation.load.ExcelLoader import ExcelLoader
from etl_implementation.load.JsonLoader import JsonLoader
from etl_implementation.load.PostgresLoader import PostgresLoader


from injector import Module, multiprovider


class LoaderModule(Module):

    @multiprovider
    def provide_loaders(self, db_manager: OracleDbManager) -> list[ILoader]:
        return [
            CSVLoader(db_manager),
            ExcelLoader(db_manager),
            JsonLoader(db_manager),
            PostgresLoader(db_manager),
        ]