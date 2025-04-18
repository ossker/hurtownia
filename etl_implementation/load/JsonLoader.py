import pandas as pd
from injector import inject
from database import OracleDbManager
from etl import ILoader

class JsonLoader(ILoader):
    @inject
    def __init__(self, db_manager: OracleDbManager) -> None:
        self._db_manager = db_manager

    def load(self, data: dict[str, pd.DataFrame]) -> None:

        # Połączenie z bazą danych
        connection = self._db_manager.connection
        cursor = connection.cursor()

        try:
            query_grupy = "INSERT INTO Grupy (nazwa) VALUES (:nazwa)"
            query_podgrupy = "INSERT INTO Podgrupy (nazwa, IdGrupy) VALUES (:nazwa, :IdGrupy)"
            query_nazwy_kierunkow = "INSERT INTO NazwyKierunków (nazwa, IdPodgrupy) VALUES (:nazwa, :IdPodgrupy)"
            query_stopnie = "INSERT INTO Stopnie (nazwa) VALUES (:nazwa)"
            query_kierunki = """
                INSERT INTO Kierunki (nazwaKierunku, IdNazwKierunków, IdStopnia)
                VALUES (:nazwaKierunku, :IdNazwKierunków, :IdStopnia)
            """

            # === GRUPY ===
            grupy_df = data.get("grupa")
            if grupy_df is not None:
                for _, row in grupy_df.iterrows():
                    cursor.execute(query_grupy, {"nazwa": row["nazwa"]})
                connection.commit()

            # === STOPNIE ===
            stopnie_df = data.get("stopien")
            if stopnie_df is not None:
                for _, row in stopnie_df.iterrows():
                    cursor.execute(query_stopnie, {"nazwa": row["nazwa"]})
                connection.commit()

            # === PODGRUPY ===
            podgrupy_df = data.get("podgrupa")
            if podgrupy_df is not None:
                for _, row in podgrupy_df.iterrows():
                    cursor.execute("SELECT IdGrupy FROM Grupy WHERE nazwa = :nazwa", {"nazwa": row["grupa"]})
                    id_grupy = cursor.fetchone()[0]
                    cursor.execute(query_podgrupy, {"nazwa": row["nazwa"], "IdGrupy": id_grupy})
                connection.commit()

            # === NAZWY KIERUNKÓW ===
            nazwy_kierunkow_df = data.get("nazwa_kierunkow")
            if nazwy_kierunkow_df is not None:
                for _, row in nazwy_kierunkow_df.iterrows():
                    cursor.execute("SELECT IdPodgrupy FROM Podgrupy WHERE nazwa = :nazwa", {"nazwa": row["podgrupa"]})
                    id_podgrupy = cursor.fetchone()[0]
                    cursor.execute(query_nazwy_kierunkow, {"nazwa": row["nazwa"], "IdPodgrupy": id_podgrupy})
                connection.commit()

            # === KIERUNKI ===
            kierunki_df = data.get("kierunek")
            if kierunki_df is not None:
                for _, row in kierunki_df.iterrows():
                    cursor.execute("SELECT IdNazwKierunków FROM NazwyKierunków WHERE nazwa = :nazwa", {"nazwa": row["nazwaKierunkow"]})
                    id_nazw_kierunkow = cursor.fetchone()[0]

                    cursor.execute("SELECT IdStopnia FROM Stopnie WHERE nazwa = :nazwa", {"nazwa": row["stopien"]})
                    id_stopnia = cursor.fetchone()[0]

                    cursor.execute(query_kierunki, {
                        "nazwaKierunku": row["nazwaKierunku"],
                        "IdNazwKierunków": id_nazw_kierunkow,
                        "IdStopnia": id_stopnia
                    })
                connection.commit()

            print("Dane zostały poprawnie załadowane do bazy.")

        except Exception as e:
            connection.rollback()
            print(f"Błąd podczas ładowania danych: {e}")
        finally:
            cursor.close()
            connection.close()
