import psycopg2
import sqlparse

from utils import get_postgres_connection


class PostgresDbManager:
    def __init__(self) -> None:
        self._connection = get_postgres_connection()
        self._execute_many_from_file("data/raw/postgres/schema.sql")
        self._execute_many_from_file("data/raw/postgres/data.sql")

    @property
    def connection(self):
        return self._connection

    def get_data(self, query) -> list:
        cursor = self._connection.cursor()
        try:
            cursor.execute(query)
            data = cursor.fetchall()
            return data
        except psycopg2.DatabaseError as e:
            print("Cannot get data from Postgres!")
            raise e
        finally:
            cursor.close()

    def _execute_many_from_file(self, file_to_execute) -> None:
        with open(file_to_execute, "r", encoding="utf-8") as f:
            self._execute_many(sqlparse.split(f.read(), strip_semicolon=True))

    def _execute_many(self, list_to_execute: list[str]) -> None:
        cursor = self._connection.cursor()
        try:
            for item_to_execute in list_to_execute:
                cursor.execute(item_to_execute)
            self._connection.commit()
            print("Executed.")
        except psycopg2.DatabaseError as e:
            print("Cannot execute queries to Postgres!")
            raise e
        finally:
            cursor.close()
