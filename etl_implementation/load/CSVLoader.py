import pandas as pd
from injector import inject

from database import OracleDbManager
from etl import ILoader


class CSVLoader(ILoader):
    @inject
    def __init__(self, db_manager: OracleDbManager) -> None:
        self._db_manager = db_manager

    def load(self, data: dict[str, pd.DataFrame]) -> None:
        df = data["rekordy"].rename(columns={
            "nazwaUczelni": "nazwa_uczelni",
            "nazwaKierunku": "nazwa_kierunku",
            "nazwaStopnia": "nazwa_stopnia"
        })

        self._db_manager.insert_many(
            """
            INSERT INTO absolwenci (id, ilosc, nazwa_uczelni, nazwa_kierunku, nazwa_stopnia)
            VALUES (:id, :ilosc, :nazwa_uczelni, :nazwa_kierunku, :nazwa_stopnia)
            """,
            df.to_dict("records")
        )
