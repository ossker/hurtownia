import pandas as pd
from enum import Enum

from etl import ITransformer

class StopienEnum(Enum):
    a = "ogółem"
    b = "studia pierwszego stopnia"
    c = "studia magisterskie jednolite"
    d = "studia drugiego stopnia"
    e = "brak danych"

class ExcelTransformer(ITransformer):
    def transform(self, data: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
        df = data["students"]

        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].astype(str).str.strip()

        df["ilosc"] = df["ilosc"].replace("-", 0)
        df["ilosc"] = pd.to_numeric(df["ilosc"], errors="coerce").fillna(0).astype(int)

        df["nazwaUczelni"] = df["nazwaUczelni"].str.upper()

        df["nazwaStopnia"] = df["nazwaStopnia"].str.lower().map({
            "a": StopienEnum.a.value,
            "b": StopienEnum.b.value,
            "c": StopienEnum.c.value,
            "d": StopienEnum.d.value,
            "e": StopienEnum.e.value
        })

        df.reset_index(drop=True, inplace=True)
        df.insert(0, "IdStudentow", df.index + 1)

        return {"students": df}