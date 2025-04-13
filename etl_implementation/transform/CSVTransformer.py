import pandas as pd

from etl import ITransformer


class CSVTransformer(ITransformer):
    def transform(self, data: pd.DataFrame) -> dict:
        pass