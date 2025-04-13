from injector import Injector

from etl import extract_excel, transform_excel, load_to_db
from etl_implementation import ETLModule, ETLPipeline

if __name__ == '__main__':
    """
        Pipeline ETL:
            E. Extract – pobierz dane z PostgreSQL/Excel/CSV/JSON
            T. Transform – Pandas, oczyszczenie, konwersje
            L. Load – wrzuć dane do Oracle
            (A. Analyze – Oracle Analytics i Python notebooks)
    """
    injector = Injector([ETLModule()])
    pipeline = injector.get(ETLPipeline)
    pipeline.run()

    # data = extract_excel()
    # uczelnie_w_wojewodztwach = transform_excel(data)
    # load_to_db(uczelnie_w_wojewodztwach)