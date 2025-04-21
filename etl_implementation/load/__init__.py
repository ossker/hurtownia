from database import OracleDbManager
from etl import ILoader
from etl_implementation.load.CSVLoader import CSVLoader
from etl_implementation.load.ExcelLoader import ExcelLoader

from etl_implementation.load.FactsLoader import FactsLoader
from etl_implementation.load.JsonLoader import JsonLoader
from etl_implementation.load.PostgresLoader import PostgresLoader


from injector import Module, multiprovider, Binder


class LoaderModule(Module):
    def configure(self, binder: Binder):
        binder.bind(FactsLoader, FactsLoader)

    @multiprovider
    def provide_loaders(self, db_manager: OracleDbManager) -> list[ILoader]:
        return [
            CSVLoader(db_manager),
            ExcelLoader(db_manager),
            JsonLoader(db_manager),
            PostgresLoader(db_manager),
        ]
