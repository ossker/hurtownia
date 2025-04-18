import cx_Oracle
import sqlparse
from cx_Oracle import Connection

from utils import get_oracle_connection

# x = {
#     "inzynierskie": [
#         {
#             "informatyka":{
#                 "nazwa kierunkow": "",
#                 "podgrupa": "",
#                 "grupa": "",
#             }
#
#         },
#         {
#             "matematyka":{
#                 "nazwa kierunkow": "",
#                 "podgrupa": "",
#                 "grupa": "",
#             }
#         }
#     ],
#     "magisterskie": [
#         {
#             "informatyka": {
#                 "nazwa kierunkow": "",
#                 "podgrupa": "",
#                 "grupa": "",
#             }
#         },
#         {
#             "pedagogika": {
#                 "nazwa kierunkow": "...",
#                 "podgrupa": "...",
#                 "grupa": "humanistyczne",
#             }
#
#         },
#         {
#             "pedagogika": {
#                 "nazwa kierunkow": "...",
#                 "podgrupa": "...",
#                 "grupa": "gowniane",
#
#         },
#     ]
# }
#
# UCZELNIA | KIERUNEK | STUDENCI
#
# UCZELNIA | KIERUNEK | ABSOLWENCI

class OracleDbManager:
    def __init__(self) -> None:
        self._connection = get_oracle_connection()
    def __post_init__(self) -> None:
        print("Tables created.")
        # self._create_table_from_excel()
        # self._create_table_from_csv()
        # self._create_table_from_postgres()

    @property
    def connection(self) -> Connection:
        return self._connection

    def insert_many(self, sql: str, data: list[dict]) -> None:
        cursor = self._connection.cursor()
        try:
            cursor.executemany(sql, data)
            self._connection.commit()
            print("Dane zostały dodane.")
        except cx_Oracle.DatabaseError as e:
            print(f"Błąd podczas dodawania danych: {e}")
        finally:
            cursor.close()

    def get_data(self, query: str) -> list:
        cursor = self._connection.cursor()

        try:
            cursor.execute(query)
            data = cursor.fetchall()
            columns = data.keys()
            return [dict(zip(columns, row)) for row in data]

        except cx_Oracle.DatabaseError as e:
            print(f"Błąd podczas pobierania danych: {e}")
            return []

        finally:
            cursor.close()

    def _create_table_from_excel(self) -> None:
        create_table_studenci = """
            CREATE TABLE studenci (
                IdStudentow NUMBER PRIMARY KEY,
                ilosc NUMBER,
                nazwaUczelni VARCHAR2(255),
                nazwaKierunku VARCHAR2(255),
                nazwaStopnia VARCHAR2(30)
            )
        """
        self._execute_many([create_table_studenci])

    def _create_table_from_csv(self) -> None:
        create_table_absolwenci  = """
        CREATE TABLE absolvenci_csv (
            id NUMBER PRIMARY KEY,
            ilosc NUMBER,
            nazwa_uczelni VARCHAR2(255),
            nazwa_kierunku VARCHAR2(255),
            nazwa_stopnia VARCHAR2(255)
        )
        """
        self._execute_many([create_table_absolwenci])


    def _create_table_from_postgres(self) -> None:
        self._execute_many_from_file("schema/from_postgres.sql")

    def _execute_many_from_file(self, file_to_execute) -> None:
        with open(file_to_execute, "r", encoding="utf-8") as f:
            self._execute_many(sqlparse.split(f.read(), strip_semicolon=True))

    def _execute_many(self, list_to_execute: list[str]) -> None:
        cursor = self._connection.cursor()
        try:
            for item_to_execute in list_to_execute:
                cursor.execute(item_to_execute)
            print("Executed.")
        except cx_Oracle.DatabaseError as e:
            print(f"Błąd: {e}")
        finally:
            cursor.close()
