import pandas as pd
from injector import inject

from database import OracleDbManager
from etl import ILoader


class JsonLoader(ILoader):
    @inject
    def __init__(self, db_manager: OracleDbManager) -> None:
        self._db_manager = db_manager

    def load(self, data: dict[str, pd.DataFrame]) -> None:
        # self._db_manager.insert_many()
        # self._db_manager.insert_many()
        pass