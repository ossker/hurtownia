import pandas as pd

from etl import ITransformer
from etl_implementation.StopienEnum import StopienEnum


class ExcelTransformer(ITransformer):
    def transform(self, data: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
        df = data["students"]

        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].astype(str).str.strip()
        df = df[
            (df["ilosc"] != ".") &
            (df["kierunek"].str.lower() != "ogółem") &
            (df["uczelnia"].str.lower() != "ogółem") &
            (~df["stopien"].str.lower().isin(["a", "e"]))
            ].copy()
        df["ilosc"] = df["ilosc"].replace("-", 0)
        df["ilosc"] = pd.to_numeric(df["ilosc"], errors="coerce").fillna(0).astype(int)

        df["uczelnia"] = df["uczelnia"].str.upper()

        df["stopien"] = df["stopien"].str.lower().map({
            "a": StopienEnum.a.value,
            "b": StopienEnum.b.value,
            "c": StopienEnum.c.value,
            "d": StopienEnum.d.value,
            "e": StopienEnum.e.value
        })

        df = df.rename(columns={
            "uczelnia": "nazwa_uczelni",
            "kierunek": "nazwa_kierunku",
            "stopien": "nazwa_stopnia"
        })
        df = df.drop_duplicates()
        df.reset_index(drop=True, inplace=True)
        df.insert(0, "id", df.index + 1)

        return {"students": df}
