import psycopg2
import yaml

def get_postgres_connection(config_path='config/settings.yaml'):
    with open(config_path, 'r') as f:
        cfg = yaml.safe_load(f)

    db = cfg['postgres']
    conn = psycopg2.connect(
        host=db['host'],
        port=db['port'],
        dbname=db['dbname'],
        user=db['user'],
        password=db['password']
    )
    return conn