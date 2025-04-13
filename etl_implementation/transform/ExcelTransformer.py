import pandas as pd

from etl import ITransformer


class ExcelTransformer(ITransformer):
    def transform(self, data: pd.DataFrame) -> dict:
        pass