import pandas as pd
from injector import inject

from database import PostgresDbManager
from etl import IExtractor


class PostgresExtractor(IExtractor):
    @inject
    def __init__(self, db_manager: PostgresDbManager) -> None:
        self._db_manager = db_manager

    def extract(self) -> dict[str, pd.DataFrame]:
        regions = self._db_manager.get_data("SELECT id, nazwa FROM wojewodztwo")
        cities = self._db_manager.get_data("SELECT id, nazwa, wojewodztwo_id FROM miasto")
        universities = self._db_manager.get_data("SELECT id, nazwa, miasto_id FROM uczelnia")

        return {
            "wojewodztwo": pd.DataFrame(regions, columns=["id", "nazwa"]),
            "miasto": pd.DataFrame(cities, columns=["id", "nazwa", "wojewodztwo_id"]),
            "uczelnia": pd.DataFrame(universities, columns=["id", "nazwa", "miasto_id"])
        }
