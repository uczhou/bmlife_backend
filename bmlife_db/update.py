from db_utils.config import *
import pandas as pd
import psycopg2
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()


def update_zipcode(connection):
    # Create table
    df = pd.read_csv('zip_state.csv')
    state_zip = {}
    for index, row in df.iterrows():
        if index > 3170:
            if row['zipcode'] < 10000:
                key = '0{}'.format(row['zipcode'])
                state_zip[key] = row['state']
            else:
                state_zip[str(row['zipcode'])] = row['state']
    cursor = None
    count = 0
    try:

        # commands = [
        #             """
        #             UPDATE zipcode
        #                 SET    state = '{}'
        #                 WHERE  geoid10 ilike '{}';
        #             """.format(value, str(key)) for key, value in state_zip.items()
        #             ]
        # sqls = ["""
        #         update zipcode set crimecount =
        #         (select count(*) from crimemap_{}
        #             where ST_Contains((select geom from zipcode where geoid10 ilike '{}'), crimemap_{}.location))
        #             where geoid10 ilike '{}' and crimecount is null;
        #     """.format(value.lower(), key, value.lower(),  key) for key, value in state_zip.items()]
        sql_dict = {}
        for key, value in state_zip.items():
            sql_dict[key] = """         
                select count(*) from crimemap_{} 
                    where ST_Contains((select geom from zipcode where geoid10 ilike '{}'), crimemap_{}.location);
            """.format(value.lower(), key, value.lower(),  key)
        cursor = connection.cursor()
        crimecount = []
        zipcodes = []
        for key, sql in sql_dict.items():
            try:
                print('Executing: {}'.format(sql))
                cursor.execute(sql)
                for item in cursor:
                    print(item[0])
                    crimecount.append(item[0])
                    zipcodes.append(key)

                print('Finished: {}'.format(sql))
                count += 1
                print(count)
                zipcode_df = pd.DataFrame.from_dict({
                    'zipcode': zipcodes, 'crimecount': crimecount
                })
                zipcode_df.to_csv('crimecount_3170.csv', index=False)
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                connection.rollback()
                continue

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if cursor:
            cursor.close()


def update_zipcode_crimecount(connection):
    # Create table
    df = pd.read_csv('')
    state_zip = {}
    for index, row in df.iterrows():
        if row['zipcode'] < 10000:
            zipcode = '0{}'.format(row['zipcode'])
        else:
            zipcode = str(row['zipcode'])
        state_zip[zipcode] = row['crimecount']

    cursor = None
    try:
        sqls = ["""
                update zipcode set crimecount = {} where geoid10 ilike '{}' and crimecount is null;
            """.format(value,  key) for key, value in state_zip.items()]

        cursor = connection.cursor()
        for sql in sqls:
            try:
                print('Executing: {}'.format(sql))
                cursor.execute(sql)
                connection.commit()
                print('Finished: {}'.format(sql))
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                connection.rollback()
                continue

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if cursor:
            cursor.close()


if __name__ == "__main__":
    import time

    failed_files = []
    start_old = time.time()
    connection = None
    try:
        connection = psycopg2.connect(user=username,
                                      password=password,
                                      host=host,
                                      port="5432",
                                      database=test_db)
        update_zipcode_crimecount(connection)
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            connection.close()
            print("PostgreSQL connection is closed")
