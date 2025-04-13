import pandas as pd

from etl import IExtractor


class PostgresExtractor(IExtractor):
    def extract(self) -> pd.DataFrame:
        #TODO postgres implementation
        ...