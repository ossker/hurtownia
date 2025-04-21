import pandas as pd
from injector import inject

from database import OracleDbManager
from etl import ILoader


class CSVLoader(ILoader):
    @inject
    def __init__(self, db_manager: OracleDbManager) -> None:
        self._db_manager = db_manager

    def load(self, data: dict[str, pd.DataFrame] = None) -> None:
        if not data:
            raise Exception
        self._insert_data_frame("""
            INSERT INTO absolwenci (id, ilosc, nazwa_uczelni, nazwa_kierunku, nazwa_stopnia, rok)
            VALUES (:id, :ilosc, :nazwa_uczelni, :nazwa_kierunku, :nazwa_stopnia, :rok)
        """, data["graduates"])

    def _insert_data_frame(self, query: str, data: pd.DataFrame):
        self._db_manager.insert_many(query, data.to_dict("records"))
