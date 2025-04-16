import pandas as pd

from etl import ITransformer


class JsonTransformer(ITransformer):
    def transform(self, data: dict[str, pd.DataFrame]) -> dict:
        pass