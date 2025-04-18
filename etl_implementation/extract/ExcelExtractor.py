import pandas as pd

from etl import IExtractor


class ExcelExtractor(IExtractor):
    def extract(self) -> dict[str, pd.DataFrame]:
        path = "data/raw/students_dataset.xlsx"
        df = pd.read_excel(path, sheet_name="Arkusz1")

        return {
            "students": df
        }