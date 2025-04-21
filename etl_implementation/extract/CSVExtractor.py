import pandas as pd
from etl import IExtractor


class CSVExtractor(IExtractor):
    def extract(self) -> dict[str, pd.DataFrame]:
        path = "data/raw/CSV/graduates_dataset_23-24.csv"
        df = pd.read_csv(path, encoding="utf-8")
        df["rok"] = "23/24"
        return {
            "graduates": df
        }


