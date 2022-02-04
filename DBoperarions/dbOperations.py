import sqlite3
import os
import shutil
import csv
import logging
from application_logger.loggerConfigure import configure_logger


logger = logging.getLogger(__name__)
logger = configure_logger(logger, "dbOperations.log")


class DB_operations:
    """This class is used to handle all sql database operations"""

    def __init__(self):
        self.path = "Training_Database/"
        self.good_data_dir = "training_Data_Validated/GoodData/"
        self.bad_data_dir = "training_Data_Validated/BadData/"

    def databaseConnection(self, database_name):
        """this method create a database connection object with given database name

        Args:
            database_name (string): name of the database
        """
        try:
            conn = sqlite3.connect(self.path + database_name + ".db")
            logger.info(f"opened database {database_name} succussfully")
        except ConnectionError:
            logger.exception("error while connecting to database")
            raise ConnectionError
        return conn

    def createTableDb(self, database_name, column_names):
        """this function create a data base table with given name and given columns

        Args:
            database_name (string): Name of the database creating
            column_names (dictionary with column names as keys): column names of the table to create
        """
        try:
            logger.info("entered to create tabledb method")
            conn = self.databaseConnection(database_name)
            c = conn.cursor()
            c.execute(
                "SELECT count(name)  FROM sqlite_master WHERE type = 'table'AND name = 'Good_Raw_Data'"
            )
            if c.fetchone()[0] == 1:
                conn.close()
                logger.info("Table created succussfully and database closed")
            else:
                for key in column_names.keys():
                    type = column_names[key]
                    # in try block we check if the table exists, if yes then add columns to the table
                    # else in catch block we will create the table
                    try:
                        # cur = cur.execute("SELECT name FROM {dbName} WHERE type='table' AND name='Good_Raw_Data'".format(dbName=DatabaseName))

                        conn.execute(
                            'ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(
                                column_name=key, dataType=type
                            )
                        )

                    except:
                        # conn.execute(f"CREATE TABLE  Good_Raw_Data ({key} {type})")
                        query = "CREATE TABLE  Good_Raw_Data ({column_name} {dataType})".format(
                            column_name=key, dataType=type
                        )
                        conn.execute(query)
                conn.close()
                logger.info("Tables crated succussfully and database closed")
        except Exception as e:
            logger.exception(f"{e}")
            conn.close()
            raise e

    def deleteTableContentFromDB(self, database):
        """this function deletes all data from existing table in database
        ( this function is called only if the input data folder is not being replaced
        by new data, so that same data will not be uploaded twice into databse)

        Args:
            database (string): database name
        """
        conn = self.databaseConnection(database)
        c = conn.cursor()
        c.execute(
            "SELECT count(name)  FROM sqlite_master WHERE type = 'table'AND name = 'Good_Raw_Data'"
        )
        try:
            if (
                c.execute("SELECT COUNT(*) FROM Good_Raw_Data") != 0
            ):  # table is not empty
                c.execute("DELETE FROM Good_Raw_Data")
                conn.commit()
                conn.close()
                logger.info("deleted all data from table before adding new data")

        except Exception as e:
            logger.exception(f"Error while deleting all data from table : {e}")
            raise e

    def insertIntoTableGoodData(self, database):

        conn = self.databaseConnection(database)
        goodFilePath = self.good_data_dir
        badFilePath = self.bad_data_dir

        files = os.listdir(goodFilePath)
        for file in files:
            try:
                with open(os.path.join(goodFilePath, file), "r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line in enumerate(reader):
                        for list in line[1]:
                            try:
                                conn.execute(
                                    "INSERT INTO Good_Raw_Data values ({values})".format(
                                        values=(list)
                                    )
                                )
                                conn.commit()

                            except Exception as e:
                                logger.exception(f"{e}")
                                raise e

                logger.info(f"{file} values inserted into table")

            except Exception as e:
                conn.rollback()
                logger.exception(f"error while inserting data into table: {e}")
                shutil.move(os.path.join(goodFilePath, file), badFilePath)
                logger.info(f"file {file} moved to bad data directory")
                conn.close()
        conn.close()

    def selectTableFromDBintoCSV(self, database):
        """this function export table from database to csv file

        Args:
            database string: name of the database
        """
        self.fileFromDb = "Training_FileFromDB/"
        self.fileName = "InputFile.csv"
        try:
            conn = self.databaseConnection(database)
            sqlSelect = "SELECT *  FROM Good_Raw_Data"
            cursor = conn.cursor()

            cursor.execute(sqlSelect)

            results = cursor.fetchall()
            # Get the headers of the csv file
            headers = [i[0] for i in cursor.description]

            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            csvFile = csv.writer(
                open(self.fileFromDb + self.fileName, "w", newline=""),
                delimiter=",",
                lineterminator="\r\n",
                quoting=csv.QUOTE_ALL,
                escapechar="\\",
            )
            csvFile.writerow(headers)
            csvFile.writerows(results)

            logger.info("Data base table exported to csv succussfully")
        except Exception as e:
            logger.exception(f"{e}")
            raise e
