import pandas as pd
from injector import inject

from database import OracleDbManager
from etl import ILoader


class PostgresLoader(ILoader):
    @inject
    def __init__(self, db_manager: OracleDbManager) -> None:
        self._db_manager = db_manager

    def load(self, data: dict[str, pd.DataFrame] = None) -> None:
        if not data:
            raise Exception
        self._insert_data_frame("INSERT INTO wojewodztwo (id, nazwa) VALUES (:id, :nazwa)", data["wojewodztwo"])
        self._insert_data_frame("INSERT INTO miasto (id, nazwa, wojewodztwo_id) VALUES (:id, :nazwa, :wojewodztwo_id)", data["miasto"])
        self._insert_data_frame("INSERT INTO uczelnia (id, nazwa, miasto_id) VALUES (:id, :nazwa, :miasto_id)", data["uczelnia"])

    def _insert_data_frame(self, query: str, data: pd.DataFrame) -> None:
        self._db_manager.insert_many(query, data.to_dict("records"))
