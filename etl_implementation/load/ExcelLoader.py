import pandas as pd

from injector import inject
from database import OracleDbManager
from etl import ILoader


class ExcelLoader(ILoader):
    @inject
    def __init__(self, db_manager: OracleDbManager) -> None:
        self._db_manager = db_manager

    def load(self, data: dict[str, pd.DataFrame]) -> None:
        self.insert_data_frame("""
            INSERT INTO studenci (IdStudentow, ilosc, nazwaUczelni, nazwaKierunku, nazwaStopnia)
            VALUES (:IdStudentow, :ilosc, :nazwaUczelni, :nazwaKierunku, :nazwaStopnia)
        """, data["students"])

    def insert_data_frame(self, query: str, data: pd.DataFrame):
        self._db_manager.insert_many(query, data.to_dict("records"))