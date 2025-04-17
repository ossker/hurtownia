import pandas as pd

from etl import IExtractor


class CSVExtractor(IExtractor):
    def extract(self) -> dict[str, pd.DataFrame]:
        #TODO csv implementation
        ...