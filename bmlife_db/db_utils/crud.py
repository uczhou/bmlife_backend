import psycopg2
from .config import *
import pandas as pd


def insert_city():
    # Create table
    df = pd.read_csv('file_state.csv')
    states = set(df['state'])

    droptables = [
        """
        Drop table if exists crimemap_{}
        """.format(state) for state in states
    ]
    commands = ["""
        CREATE TABLE crimemap_{} (
            gid Serial PRIMARY KEY,
            address_1 TEXT,
            case_number TEXT,
            city VARCHAR(50),
            created_at TEXT,
            day_of_week VARCHAR(50),
            hour_of_day VARCHAR(50),
            incident_datetime TEXT,
            incident_id VARCHAR(75),
            incident_type_primary TEXT,
            latitude VARCHAR(50),
            longitude VARCHAR(50),
            location geometry(POINT, 4326),
            parent_incident_type TEXT,
            state VARCHAR(10),
            updated_at TEXT,
            zip VARCHAR(10)
        )
        """.format(state) for state in states]
                # """
                # CREATE INDEX landmarks_the_geom_gist
                #   ON KYCrimeMap
                #   USING gist
                #   (location );
                # """
    conn = None
    try:
        # read the connection parameters
        conn = psycopg2.connect(user=username,
                                      password=password,
                                      host=host,
                                      port="5432",
                                      database=test_db)
        cur = conn.cursor()
        # create table one by one
        for command in droptables:
            cur.execute(command)

        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

