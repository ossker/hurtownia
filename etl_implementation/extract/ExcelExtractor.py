import pandas as pd

from etl import IExtractor


class ExcelExtractor(IExtractor):
    def extract(self) -> pd.DataFrame:
        #TODO excel implementation
        ...