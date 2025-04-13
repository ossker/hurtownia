import pandas as pd

from etl import IExtractor


class JsonExtractor(IExtractor):
    def extract(self) -> pd.DataFrame:
        pass