from etl import extract_excel, transform_excel, load_to_db

if __name__ == '__main__':
    """
        Pipeline ETL:
            E. Extract – pobierz dane z PostgreSQL/Excel/CSV/JSON
            T. Transform – Pandas, oczyszczenie, konwersje
            L. Load – wrzuć dane do Oracle
            (A. Analyze – Oracle Analytics i Python notebooks)
    """
    data = extract_excel()
    uczelnie_w_wojewodztwach = transform_excel(data)
    load_to_db(uczelnie_w_wojewodztwach)