from pathlib import Path

import sqlalchemy as db
from sqlalchemy import exc, text
import pandas as pd


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DataManager(object):
    __metaclass__ = Singleton
    conn = None

    def __new__(cls, *args, **kwargs):
        print("Initialise Database utility class")

        db_name = 'mobiledata'
        engine = db.create_engine('postgresql+psycopg2://postgres:20081979@localhost/' + db_name)
        cls.conn = engine.connect()
        return super().__new__(cls)

    def get_od(self, file_name, verbos=0):
        try:
            query = Path(file_name).read_text().replace("\n", " ")
            if verbos == 1:
                print(query)

            results = self.conn.execute(text(query))
            df_results = pd.DataFrame(results)

            if verbos == 1:
                print("results shape" + str(df_results.shape))
        except exc.SQLAlchemyError as e:

            print("Encountered general SQLAlchemyError!", e)
        return df_results
