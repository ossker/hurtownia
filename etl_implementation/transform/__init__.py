from etl import ITransformer
from etl_implementation.transform.CSVTransformer import CSVTransformer
from etl_implementation.transform.ExcelTransformer import ExcelTransformer
from etl_implementation.transform.JsonTransformer import JsonTransformer
from etl_implementation.transform.PostgresTransformer import PostgresTransformer

from injector import Module, multiprovider


class TransformerModule(Module):
    @multiprovider
    def provide_transformers(self) -> list[ITransformer]:
        return [
            # CSVTransformer(),
            # ExcelTransformer(),
            JsonTransformer(),
            # PostgresTransformer(),
        ]
