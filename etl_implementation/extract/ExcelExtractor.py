import pandas as pd

from etl import IExtractor


class ExcelExtractor(IExtractor):
    def extract(self) -> dict[str, pd.DataFrame]:
        path = "data/raw/XLSX/students_dataset_23-24.xlsx"
        df = pd.read_excel(path, sheet_name="Arkusz1")
        df["rok"] = "23/24"
        return {
            "students": df
        }
