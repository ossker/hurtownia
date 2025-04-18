import pandas as pd
from etl import IExtractor


class CSVExtractor(IExtractor):
    def extract(self) -> dict[str, pd.DataFrame]:
        df = pd.read_csv("data/raw/CSV/dane.csv", encoding="utf-8")
        uczelnie = df[["nazwaUczelni"]].drop_duplicates().reset_index(drop=True)
        kierunki = df[["nazwaKierunku"]].drop_duplicates().reset_index(drop=True)
        stopnie = df[["nazwaStopnia"]].drop_duplicates().reset_index(drop=True)
        rekordy = df[["ilosc", "nazwaUczelni", "nazwaKierunku", "nazwaStopnia"]].copy()
        rekordy = rekordy.reset_index(drop=True)
        rekordy.insert(0, "id", rekordy.index + 1)
        return {
            "uczelnia": uczelnie,
            "kierunek": kierunki,
            "stopien": stopnie,
            "rekordy": rekordy
        }


