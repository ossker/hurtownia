import pandas as pd

from etl import ITransformer


class PostgresTransformer(ITransformer):
    def transform(self, data: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
        data["wojewodztwo"]["nazwa"] = data["wojewodztwo"]["nazwa"].str.strip().str.lower()
        data["miasto"]["nazwa"] = data["miasto"]["nazwa"].str.strip()
        data["uczelnia"]["nazwa"] = data["uczelnia"]["nazwa"].str.strip().str.upper()

        return data
