import mysql.connector
import csv

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="MertAkkanPass123",
    auth_plugin='mysql_native_password'
)
# creating database_cursor to perform SQL operation to run queries
db_cursor = db_connection.cursor(buffered=True)

db_cursor.execute("USE MedicalDatabase")


def populate_table(db_connection, db_cursor, insert_query, file_path):
    with open(file_path, mode='r') as csv_data:
        reader = csv.reader(csv_data, delimiter=';')
        csv_data_list = list(reader)
        for row in csv_data_list[1:]:
            row = tuple(map(lambda x: None if x == "" else x, row[0].split(',')))
            db_cursor.execute(insert_query, row)

    db_connection.commit()


db_cursor.execute("""CREATE TABLE users (
                    ID INT PRIMARY KEY AUTO_INCREMENT,
                    username VARCHAR(30),
                    password VARCHAR(30),
                    epsilon FLOAT
                );""")

insert_patients = (
    "INSERT INTO users(username, password, epsilon)"
    "VALUES (%s, %s, %s)"
)

populate_table(db_connection, db_cursor, insert_patients, "users.csv")