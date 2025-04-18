import pandas as pd

from etl import ITransformer


class CSVTransformer(ITransformer):
    def transform(self, data: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
        df = data["rekordy"].copy()

        # Czyszczenie i formatowanie
        df["nazwaUczelni"] = df["nazwaUczelni"].str.strip().str.upper()
        df["nazwaKierunku"] = df["nazwaKierunku"].str.strip().str.title()
        df["nazwaStopnia"] = df["nazwaStopnia"].str.strip().str.lower()

        # Konwersja ilości na liczbę całkowitą (jeśli trzeba)
        df["ilosc"] = pd.to_numeric(df["ilosc"], errors="coerce").fillna(0).astype(int)

        # Nadpisujemy zmodyfikowaną wersję
        data["rekordy"] = df

        return data
