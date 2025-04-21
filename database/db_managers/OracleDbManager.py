import cx_Oracle
import sqlparse
from cx_Oracle import Connection

from utils import get_oracle_connection
import re


class OracleDbManager:
    def __init__(self) -> None:
        self._connection = get_oracle_connection()
        self._remove_tables()
        self._create_table_from_csv()
        self._create_table_from_excel()
        self._create_table_from_json()
        self._create_table_from_postgres()
        self._create_fact_table()

        print("All tables created.")

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
            raise e
        finally:
            cursor.close()

    def get_data(self, query: str) -> list:
        cursor = self._connection.cursor()

        try:
            cursor.execute(query)
            columns = [col[0].lower() for col in cursor.description]
            data = cursor.fetchall()
            return [dict(zip(columns, row)) for row in data]

        except cx_Oracle.DatabaseError as e:
            print(f"Błąd podczas pobierania danych: {e}")
            return []

        finally:
            cursor.close()

    def _create_table_from_excel(self) -> None:
        create_table_studenci = """
            CREATE TABLE studenci (
                id NUMBER PRIMARY KEY,
                ilosc NUMBER,
                nazwa_uczelni VARCHAR2(255),
                nazwa_kierunku VARCHAR2(255),
                nazwa_stopnia VARCHAR2(30),
                rok VARCHAR2(5)
            )
        """
        self._execute_many([create_table_studenci])

    def _create_table_from_csv(self) -> None:
        create_table_absolwenci = """
        CREATE TABLE absolwenci(
            id NUMBER PRIMARY KEY,
            ilosc NUMBER,
            nazwa_uczelni VARCHAR2(255),
            nazwa_kierunku VARCHAR2(255),
            nazwa_stopnia VARCHAR2(255),
            rok VARCHAR2(5)
        )
        """
        self._execute_many([create_table_absolwenci])

    def _create_table_from_postgres(self) -> None:
        self._execute_many_from_file("schema/from_postgres.sql")

    def _create_table_from_json(self) -> None:
        self._execute_many_from_file("database/scripts/json.sql")
        # self._execute_many_from_file_by_slash("database/scripts/json_triggers.sql")

    def _create_fact_table(self) -> None:
        self._execute_many_from_file("database/scripts/fact_table.sql")

    def _remove_tables(self) -> None:
        self._execute_many_from_file("database/scripts/remove_tables.sql")

    def _execute_many_from_file(self, file_to_execute: str) -> None:
        with open(file_to_execute, "r", encoding="utf-8") as f:
            self._execute_many(sqlparse.split(f.read(), strip_semicolon=True))

    def _execute_many_from_file_by_slash(self, file_to_execute: str) -> None:
        with open(file_to_execute, "r", encoding="utf-8") as f:
            sql_script = f.read()
            statements = self._split_oracle_sql_by_slash(sql_script)
            self._execute_many(statements)

    @staticmethod
    def _split_oracle_sql_by_slash(sql_script: str) -> list[str]:
        parts = re.split(r'(?m)^(\s*/\s*)$', sql_script.strip())
        statements = []
        buffer = ""

        for part in parts:
            if re.match(r'^\s*/\s*$', part):
                buffer += "\n" + part
                statements.append(buffer.strip())
                buffer = ""
            else:
                buffer += ("\n" if buffer else "") + part.strip()
        if buffer.strip():
            statements.append(buffer.strip())

        return statements

    def _execute_many(self, list_to_execute: list[str]) -> None:
        cursor = self._connection.cursor()
        executing=None
        try:
            for item_to_execute in list_to_execute:
                executing = item_to_execute
                cursor.execute(item_to_execute)
            self._connection.commit()
            print("Executed.")
        except cx_Oracle.DatabaseError as e:
            print(f"Błąd: {executing}")
            self._handle_exceptions(e)

        finally:
            cursor.close()

    @staticmethod
    def _handle_exceptions(e: cx_Oracle.DatabaseError) -> None:
        error, = e.args
        if "ORA-04080" in error.message or "ORA-00942" in error.message:
            print(f"Pomijam: {e}")
        else:
            print(f"Błąd: {e}")
            raise e
