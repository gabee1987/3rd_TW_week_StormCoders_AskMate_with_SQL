'''
    Frequently used functions for the AskMate project.
    by StormCoders
'''

import psycopg2
from local_config import *


def query_execute(query, data_to_modify=None, return_data='all_data'):
    '''
        Set the connection with the database,
        and execute the orders in it. After the
        process, it closes the connection.
    '''

    connect_str = "dbname={0} user={1} password={2} host={3}".format(DATABASE, USER, PASSWORD, HOST)
    conn = psycopg2.connect(connect_str)
    conn.autocommit = True
    cursor = conn.cursor()
    print(data_to_modify)
    cursor.execute(query, data_to_modify)

    if data_to_modify is not None:     # The function decides if the query has some variable in it.
        if return_data == 'all_data':    # The function decides if the type of the query is SELECT or not.
            data_from_query = cursor.fetchall()
            conn.close()
            return data_from_query
        elif return_data == 'no_data':
            conn.close()
    if data_to_modify is None:
        if return_data == 'all_data':
            data_from_query = cursor.fetchall()
            conn.close()
            return data_from_query
        elif return_data == 'no_data':
            conn.close()
