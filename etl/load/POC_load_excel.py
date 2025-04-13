import uuid

from utils import get_oracle_connection
import cx_Oracle
import yaml


def create_table_if_not_exists(connection):
    cursor = connection.cursor()

    create_wojewodztwo_table = """
        CREATE TABLE wojewodztwo (
            id NUMBER PRIMARY KEY,
            nazwa VARCHAR2(100) NOT NULL
        )
        """

    create_uczelnia_table = """
        CREATE TABLE uczelnia (
            id NUMBER PRIMARY KEY,
            nazwa VARCHAR2(255) NOT NULL,
            wojewodztwo_id NUMBER,
            CONSTRAINT fk_wojewodztwo FOREIGN KEY (wojewodztwo_id) REFERENCES wojewodztwo(id)
        )
        """

    create_sequence_woj = """
        CREATE SEQUENCE wojewodztwo_seq
        START WITH 1
        INCREMENT BY 1
    """

    create_sequence_uczelnia = """
            CREATE SEQUENCE uczelnia_seq
            START WITH 1
            INCREMENT BY 1
        """

    trigger_woj = """
        CREATE OR REPLACE TRIGGER trg_wojewodztwo_id
        BEFORE INSERT ON wojewodztwo
        FOR EACH ROW
        BEGIN
            IF :NEW.id IS NULL THEN
                SELECT wojewodztwo_seq.NEXTVAL
                INTO :NEW.id
                FROM dual;
            END IF;
        END;
        /
    """

    trigger_uni = """
        CREATE OR REPLACE TRIGGER trg_uczelni_id
        BEFORE INSERT ON uczelnia
        FOR EACH ROW
        BEGIN
            IF :NEW.id IS NULL THEN
                SELECT uczelnia_seq.NEXTVAL
                INTO :NEW.id
                FROM dual;
            END IF;
        END;
        /
    """

    try:
        cursor.execute(create_sequence_woj)
        cursor.execute(create_sequence_uczelnia)
        cursor.execute(create_wojewodztwo_table)
        cursor.execute(create_uczelnia_table)
        cursor.execute(trigger_woj)
        cursor.execute(trigger_uni)
        print("Tabela wojewodztwo i uczelnia zostały stworzone lub już istnieją.")
    except cx_Oracle.DatabaseError as e:
        print(f"Błąd podczas tworzenia tabel: {e}")
    finally:
        cursor.close()


def insert_wojewodztwo_data(connection, wojewodztwa_data):
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO wojewodztwo (nazwa) 
    VALUES (:nazwa)
    """

    try:
        cursor.executemany(insert_query, [{"nazwa": wojewodztwo} for wojewodztwo in wojewodztwa_data])
        connection.commit()
        print("Dane wojewodztwa zostały dodane.")
    except cx_Oracle.DatabaseError as e:
        print(f"Błąd podczas dodawania danych do wojewodztwo: {e}")
    finally:
        cursor.close()


def insert_uczelnia_data(connection, uczelnia_data):
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO uczelnia (nazwa, wojewodztwo_id) 
    VALUES (:nazwa, :wojewodztwo_id)
    """

    try:
        cursor.executemany(insert_query, uczelnia_data)
        connection.commit()
        print("Dane uczelni zostały dodane.")
    except cx_Oracle.DatabaseError as e:
        print(f"Błąd podczas dodawania danych do uczelni: {e}")
    finally:
        cursor.close()


def get_wojewodztwa(connection):
    cursor = connection.cursor()

    select_query = "SELECT id, nazwa FROM wojewodztwo"

    try:
        cursor.execute(select_query)
        wojewodztwa = cursor.fetchall()
        return wojewodztwa

    except cx_Oracle.DatabaseError as e:
        print(f"Błąd podczas pobierania danych z tabeli wojewodztwo: {e}")
        return []

    finally:
        cursor.close()



def load_to_db(data: dict) -> None:
    """
        #TODO zakomentuj create_table_if_not_exists() jak juz stworzysz!!!
    """
    conn = get_oracle_connection()
    create_table_if_not_exists(conn)
    wojewodztwa_data = list(data.keys())
    insert_wojewodztwo_data(conn, wojewodztwa_data)
    wojewodztwa_z_id = get_wojewodztwa(conn)
    uczelnia_data = []
    wojewodztwa_dict = {woj[1].strip(): woj[0] for woj in wojewodztwa_z_id}
    for wojewodztwo, uczelnie in data.items():
        wojewodztwo_id = wojewodztwa_dict.get(wojewodztwo.strip())
        if wojewodztwo_id:
            for uczelnia in uczelnie:
                uczelnia_data.append({
                    "nazwa": uczelnia.strip(),
                    "wojewodztwo_id": wojewodztwo_id
                })
        else:
            print("Brak wojewodztwa.")

    insert_uczelnia_data(conn, uczelnia_data)
    conn.close()