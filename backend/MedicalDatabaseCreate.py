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

# executing cursor with execute method and pass SQL query
#db_cursor.execute("CREATE DATABASE MedicalDatabase")

"""
# get list of all databases
db_cursor.execute("SHOW DATABASES")

# print all databases
for db in db_cursor:
    print(db)
"""
db_cursor.execute("USE MedicalDatabase")


def populate_table(db_connection, db_cursor, insert_query, file_path):
    with open(file_path, mode='r') as csv_data:
        reader = csv.reader(csv_data, delimiter=';')
        csv_data_list = list(reader)
        for row in csv_data_list[1:]:
            row = tuple(map(lambda x: None if x == "" else x, row[0].split(',')))
            db_cursor.execute(insert_query, row)

    db_connection.commit()


db_cursor.execute("""CREATE TABLE Patients (
                    StudentID INT PRIMARY KEY AUTO_INCREMENT,
                    Age INT,
                    Gender VARCHAR(10),
                    Height DECIMAL(10,5),
                    Weight DECIMAL(10,5),
                    BloodType VARCHAR(5),
                    BMI DECIMAL(10,5),
                    Temperature DECIMAL(10,5),
                    HeartRate DECIMAL,
                    BloodPressure DECIMAL,
                    Cholesterol DECIMAL,
                    Diabetes VARCHAR(10),
                    Smoking VARCHAR(10)
                );""")

insert_patients = (
    "INSERT INTO Patients(StudentID, Age, Gender, Height, Weight, BloodType, BMI, Temperature, "
    "HeartRate, BloodPressure, Cholesterol, Diabetes, Smoking) "
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
)

populate_table(db_connection, db_cursor, insert_patients, "medical_students_dataset.csv")
