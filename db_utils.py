from mysql import connector
import datetime

import app_settings


def get_mysql_db_connection():

    conn = connector.connect(host=app_settings.HOST, database=app_settings.DATABASE,
                             user=app_settings.USER, password=app_settings.PASSWORD)
    return conn


def create_table_if_not_exists():
    """
    Assuming that DB('bot_history') is already present, create table('search_history')
    :return:
    """
    with get_mysql_db_connection() as conn:
        cursor = conn.cursor()
        sql_statement = '''
        CREATE TABLE IF NOT EXISTS search_history(search_text VARCHAR(255) NOT NULL, searched_at DATE)
        '''
        cursor.execute(sql_statement)
        cursor.close()

def insert_into_search_history(search_text):
    insert_statement = '''
    INSERT INTO search_history(search_text, searched_at) VALUES('{search_text}', '{searched_at}'
    '''.format(search_text=search_text, searched_at=datetime.datetime.now())

    with get_mysql_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(insert_statement)
        conn.commit()
        cursor.close()


def filter_from_search_history(search_text):
    """
    Return top 2 search_text after sorting in reversed order by searched_at
    :return:
    """

    select_statement = '''
    SELECT search_text from search_history where search_text LIKE '%{search_text}%' ORDER BY 
    searched_at LIMIT 2 '''.format(search_text=search_text)

    matched_search_items = []
    with get_mysql_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(select_statement)

        for match in cursor.fetchall():
            matched_search_items.append(match)
        cursor.close()
        return '\n'.join(matched_search_items)
