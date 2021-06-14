import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries



def drop_tables(cur, conn):
"""
    Drop tables in data base.
    
    Keyword arguments:
    cur  --> cursor
    conn --> connection to data base
"""
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
"""
    Create tables in data base.
    
    Keyword arguments:
    cur  --> cursor
    conn --> connection to data base
"""
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    try :
        config = configparser.ConfigParser()
        config.read('dwh.cfg')
        conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
        cur = conn.cursor()
        drop_tables(cur, conn)
        create_tables(cur, conn)
        conn.close()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()