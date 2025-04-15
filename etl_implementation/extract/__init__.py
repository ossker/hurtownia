from database import PostgresDbManager
from etl import IExtractor
from etl_implementation.extract.CSVExtractor import CSVExtractor
from etl_implementation.extract.ExcelExtractor import ExcelExtractor
from etl_implementation.extract.JsonExtractor import JsonExtractor
from etl_implementation.extract.PostgresExtractor import PostgresExtractor

from injector import Module, multiprovider


class ExtractorModule(Module):
    @multiprovider
    def provide_extractors(self, db_manager: PostgresDbManager) -> list[IExtractor]:
        return [
            CSVExtractor(),
            ExcelExtractor(),
            JsonExtractor(),
            PostgresExtractor(db_manager),
        ]