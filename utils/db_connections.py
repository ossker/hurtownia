import psycopg2
import yaml
import cx_Oracle
from cx_Oracle import Connection


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


def get_oracle_connection(config_path='config/settings.yaml') -> Connection:
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    oracle_cfg = config['oracle']
    instant_client = config['instant_client']
    instant_client_path = instant_client['path']
    try:
        cx_Oracle.init_oracle_client(lib_dir=instant_client_path)
    except Exception:
        print("Oracle Client library has already been initialized")
    dsn = cx_Oracle.makedsn(
        oracle_cfg['host'],
        oracle_cfg['port'],
        service_name=oracle_cfg['service_name']
    )

    connection = cx_Oracle.connect(
        user=oracle_cfg['user'],
        password=oracle_cfg['password'],
        dsn=dsn,
        # mode=cx_Oracle.SYSDBA
    )

    return connection