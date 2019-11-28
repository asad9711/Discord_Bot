from mysql import connector

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
    conn = get_mysql_db_connection()

    cursor = conn.cursor()
    sql_statement = "CREATE TABLE IF NOT EXISTS search_history(search_id INT NOT NULL" \
                    " AUTO_INCREMENT,PRIMARY KEY(search_id),search_text VARCHAR(255) NOT NULL" \
                    ", searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    cursor.execute(sql_statement)
    cursor.close()
    conn.close()
    print("Successfully created Table")


def insert_into_search_history(search_text):
    insert_statement = "INSERT INTO search_history(search_text) " \
                       "VALUES(%s)"

    conn = get_mysql_db_connection()

    cursor = conn.cursor()
    cursor.execute(insert_statement, (search_text,))
    conn.commit()
    cursor.close()
    conn.close()


def filter_from_search_history(search_text):
    """
    Return top 2 search_text after sorting in DESCENDING order by searched_at datetime
    :return:
    """
    select_statement = "SELECT search_text from search_history where search_text " \
                       "LIKE '%{}%' ORDER BY searched_at DESC LIMIT 2 ".format(search_text)

    matched_search_items = []
    conn = get_mysql_db_connection()
    cursor = conn.cursor()
    cursor.execute(select_statement)

    for match in cursor.fetchall():
        matched_search_items.append(match)
    cursor.close()
    conn.close()
    return matched_search_items
