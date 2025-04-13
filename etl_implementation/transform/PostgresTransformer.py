import pandas as pd

from etl import ITransformer


class PostgresTransformer(ITransformer):
    def transform(self, data: pd.DataFrame) -> dict:
        pass
