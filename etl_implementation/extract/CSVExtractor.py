import pandas as pd

from etl import IExtractor


class CSVExtractor(IExtractor):
    def extract(self) -> pd.DataFrame:
        #TODO csv implementation
        ...