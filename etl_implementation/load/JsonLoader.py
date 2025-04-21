import pandas as pd
from injector import inject
from database import OracleDbManager
from etl import ILoader


class JsonLoader(ILoader):
    @inject
    def __init__(self, db_manager: OracleDbManager) -> None:
        self._db_manager = db_manager

    def load(self, data: dict[str, pd.DataFrame] = None) -> None:
        if not data:
            raise Exception
        connection = self._db_manager.connection
        cursor = connection.cursor()

        try:
            for key in data:
                if data[key] is not None:
                    df = data[key]
                    if "id" not in df.columns:
                        df.insert(0, "id", df.index + 1)
                        data[key] = df

            query_grupy = "INSERT INTO grupa (id, nazwa) VALUES (:id, :nazwa)"
            query_podgrupy = "INSERT INTO podgrupa (id, nazwa, grupa_id) VALUES (:id, :nazwa, :grupa_id)"
            query_nazwy_kierunkow = "INSERT INTO nazwa_kierunkow (id, nazwa, podgrupa_id) VALUES (:id, :nazwa, :podgrupa_id)"
            query_stopnie = "INSERT INTO stopien (id, nazwa) VALUES (:id, :nazwa)"
            query_kierunki = """
                INSERT INTO kierunek (id, nazwa, nazwa_kierunkow_id, stopien_id)
                VALUES (:id, :nazwa, :nazwa_kierunkow_id, :stopien_id)
            """

            # === GRUPY ===
            grupy_df = data.get("grupa")
            if grupy_df is not None:
                for _, row in grupy_df.iterrows():
                    cursor.execute(query_grupy, {"id": row["id"], "nazwa": row["nazwa"]})
                connection.commit()

            # === STOPNIE ===
            stopnie_df = data.get("stopien")
            if stopnie_df is not None:
                for _, row in stopnie_df.iterrows():
                    cursor.execute(query_stopnie, {"id": row["id"], "nazwa": row["nazwa"]})
                connection.commit()

            # === PODGRUPY ===
            podgrupy_df = data.get("podgrupa")
            if podgrupy_df is not None:
                for _, row in podgrupy_df.iterrows():
                    cursor.execute("SELECT id FROM grupa WHERE nazwa = :nazwa", {"nazwa": row["grupa"]})
                    id_grupy = cursor.fetchone()[0]
                    cursor.execute(query_podgrupy, {
                        "id": row["id"],
                        "nazwa": row["nazwa"],
                        "grupa_id": id_grupy
                    })
                connection.commit()

            # === NAZWY KIERUNKÓW ===
            nazwy_kierunkow_df = data.get("nazwa_kierunkow")
            if nazwy_kierunkow_df is not None:
                for _, row in nazwy_kierunkow_df.iterrows():
                    cursor.execute("SELECT id FROM podgrupa WHERE nazwa = :nazwa", {"nazwa": row["podgrupa"]})
                    id_podgrupy = cursor.fetchone()[0]
                    cursor.execute(query_nazwy_kierunkow, {
                        "id": row["id"],
                        "nazwa": row["nazwa"],
                        "podgrupa_id": id_podgrupy
                    })
                connection.commit()

            # === KIERUNKI ===
            kierunki_df = data.get("kierunek")
            if kierunki_df is not None:
                for _, row in kierunki_df.iterrows():
                    cursor.execute("SELECT id FROM nazwa_kierunkow WHERE nazwa = :nazwa", {"nazwa": row["nazwaKierunkow"]})
                    id_nazw_kierunkow = cursor.fetchone()[0]

                    cursor.execute("SELECT id FROM stopien WHERE nazwa = :nazwa", {"nazwa": row["stopien"]})
                    id_stopnia = cursor.fetchone()[0]

                    cursor.execute(query_kierunki, {
                        "id": row["id"],
                        "nazwa": row["nazwa"],
                        "nazwa_kierunkow_id": id_nazw_kierunkow,
                        "stopien_id": id_stopnia
                    })
                connection.commit()

            print("Dane zostały poprawnie załadowane do bazy.")

        except Exception as e:
            connection.rollback()
            print(f"Błąd podczas ładowania danych: {e}")
        finally:
            cursor.close()
