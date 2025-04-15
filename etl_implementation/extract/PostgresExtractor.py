import pandas as pd
from injector import inject

from database import PostgresDbManager
from etl import IExtractor


class PostgresExtractor(IExtractor):
    @inject
    def __init__(self, db_manager: PostgresDbManager) -> None:
        self._db_manager = db_manager

    def extract(self) -> pd.DataFrame:
        #TODO postgres implementation
        ...