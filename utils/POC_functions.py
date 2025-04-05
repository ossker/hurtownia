import cx_Oracle

from utils.db_connections import get_oracle_connection


def get_uczelnia_data():
    conn = get_oracle_connection()
    cursor = conn.cursor()
    query = """
        SELECT u.nazwa AS uczelnia, w.nazwa AS wojewodztwo
        FROM uczelnia u
        JOIN wojewodztwo w ON u.wojewodztwo_id = w.id
    """
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except cx_Oracle.DatabaseError as e:
        print(f"Błąd podczas pobierania danych: {e}")
        return []
    finally:
        cursor.close()