import pandas as pd

from injector import inject
from database import OracleDbManager
from etl import ILoader


class FactsLoader(ILoader):
    @inject
    def __init__(self, db_manager: OracleDbManager) -> None:
        self._db_manager = db_manager

    def load(self, data: dict[str, pd.DataFrame] = None) -> None:
        studenci = pd.DataFrame(self._db_manager.get_data("SELECT * FROM studenci"))
        absolwenci = pd.DataFrame(self._db_manager.get_data("SELECT * FROM absolwenci"))

        if studenci.empty or absolwenci.empty:
            print("Brak danych w jednej z tabel (studenci lub absolwenci).")
            raise

        merged = pd.merge(
            studenci,
            absolwenci,
            on=["nazwa_uczelni", "nazwa_kierunku", "nazwa_stopnia", "rok"],
            suffixes=("_studenci", "_absolwenci"),
            how="inner"
        )

        merged["nazwa_stopnia"] = (
            merged["nazwa_stopnia"]
            .str.replace(r"^studia\s+", "", case=False, regex=True)
            .str.replace(r"\s+", "_", regex=True)
            .str.lower()
        )

        print(f"Złączono {len(merged)} rekordów.")

        uczelnie = self._db_manager.get_data("SELECT id, LOWER(TRIM(nazwa)) AS nazwa FROM uczelnia")
        uczelnie_map = {u["nazwa"]: u["id"] for u in uczelnie}

        kierunki = self._db_manager.get_data("""
                SELECT k.id, k.nazwa AS kierunek, LOWER(TRIM(s.nazwa)) AS stopien
                FROM kierunek k
                JOIN stopien s ON k.stopien_id = s.id
            """)
        kierunki_map = {(k["kierunek"], k["stopien"]): k["id"] for k in kierunki}

        statystyki_records = []
        missing_uni = set()
        for _, row in merged.iterrows():
            uczelnia_id = uczelnie_map.get(row["nazwa_uczelni"].strip().lower())
            kierunek_id = kierunki_map.get(
                (row["nazwa_kierunku"].strip().lower(), row["nazwa_stopnia"].strip().lower()))

            if not uczelnia_id:
                print(f"Brak uczelni: {row['nazwa_uczelni']}")
                missing_uni.add(row['nazwa_uczelni'])
                continue

            if not kierunek_id:
                print(f"Brak kierunku: {row['nazwa_kierunku']} | {row['nazwa_stopnia']}")
                continue

            record = {
                "rok": row["rok"],
                "kierunek_id": kierunek_id,
                "studenci_id": row["id_studenci"],
                "absolwenci_id": row["id_absolwenci"],
                "uczelnia_id": uczelnia_id,
            }
            statystyki_records.append(record)

        print(f"Brakuje {len(missing_uni)} uczelni")

        if statystyki_records:
            df_statystyki = pd.DataFrame(statystyki_records)
            df_statystyki.drop_duplicates(
                subset=["rok", "kierunek_id", "studenci_id", "absolwenci_id", "uczelnia_id"],
                inplace=True
            )
            df_statystyki.insert(0, "id", range(1, len(df_statystyki) + 1))

            self._insert_data_frame("""
                        INSERT INTO statystyki (id, rok, kierunek_id, studenci_id, absolwenci_id, uczelnia_id)
                        VALUES (:id, :rok, :kierunek_id, :studenci_id, :absolwenci_id, :uczelnia_id)
                    """, df_statystyki)

            print(f"Wstawiono {len(df_statystyki)} rekordów do statystki.")

        else:
            print("Nie znaleziono danych do wstawienia.")

    def _insert_data_frame(self, query: str, data: pd.DataFrame):
        self._db_manager.insert_many(query, data.to_dict("records"))
