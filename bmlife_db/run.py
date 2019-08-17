import pandas as pd
import psycopg2
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()


def bulk_insert(file_name, connection, table_name, failed_files):
    cursor = None
    try:
        cursor = connection.cursor()
        sql = """
        copy {} (address_1, 
                case_number, 
                city,
                created_at,
                day_of_week,
                hour_of_day,
                incident_datetime,
                incident_id,
                incident_type_primary,
                latitude,
                longitude,
                location,
                parent_incident_type,
                state,
                updated_at,
                zip)
        from STDIN delimiter ',' quote '"' CSV HEADER
        """.format(table_name)
        with open(file_name, 'r') as f:
            cursor.copy_expert(sql, f)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error processing file: {}, DB: {}".format(file_name, table_name))
        print("Error: ", error)
        failed_files.append(file_name)
        connection.rollback()
        if cursor:
            cursor.close()


def update_zipcode(connection):
    # Create table
    df = pd.read_csv('zip_state.csv')
    state_zip = {}
    for index, row in df.iterrows():
        state_zip[row['zipcode']] = row['state']

    cursor = None
    try:
        cursor = connection.cursor()
        commands = ['''
                    CREATE TEMP TABLE tmp_x (id int, state VARCHAR(5), zipcode VARCHAR(5)); 
                    ''',
                    '''
                    COPY tmp_x FROM '/absolute/path/to/file' (FORMAT csv);
                    ''',

                    '''
                    UPDATE zipcode
                        SET    state = tmp_x.state
                        FROM   tmp_x
                        WHERE  zipcode.geoid10 = tmp_x.zipcode;
                    ''',
                    '''
                    DROP TABLE tmp_x;
                    '''
                    ]
        for command in commands:
            cursor.execute(command)
        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        connection.rollback()
        if cursor:
            cursor.close()


if __name__ == "__main__":
    import os
    import time

    failed_files = []
    start_old = time.time()
    connection = None
    try:
        base_dir = ''
        files = os.listdir(base_dir)
        df = pd.read_csv('file_state.csv')
        file_size = pd.read_csv('filesize.csv')
        file_size_dict = {}
        for index, row in file_size.iterrows():
            file_size_dict[row['uuid']] = row['lines']
        for index, row in df.iterrows():
            file_name = row['filename'] + '.csv'
            try:
                full_name = base_dir + file_name
                start = time.time()
                bulk_insert(base_dir + file_name, connection, 'CRIMEMAP_' + row['state'], failed_files)
                end = time.time()
                print('Finish processing file: {} ********* Total Lines: {}  Time used: {}s'.format(file_name, file_size_dict[row['filename']], end-start))
                logger.info('Finish processing file: {} ********* Total Lines: {}  Time used: {}s'.format(file_name, file_size_dict[row['filename']], end-start))
            except Exception as e:
                print(e)
                continue
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        end = time.time()
        print('Finish the project! Time used: {}s'.format(end - start_old))
        logger.info('Finish the project! Time used: {}s'.format(end - start_old))
        print('Failed Files: ', '\n'.join(failed_files))
        logger.info('Failed Files: {}'.format('\n'.join(failed_files)))
        if (connection):
            connection.close()
            print("PostgreSQL connection is closed")
