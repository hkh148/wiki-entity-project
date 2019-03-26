from macros import *
import mysql.connector
import argparse

mydb = mysql.connector.connect(
    host="localhost",
    user=USER_NAME,
    passwd=PASSWORD
)
cursor = mydb.cursor()


def dbcreator():
    cursor.execute("CREATE SCHEMA " + DB_NAME + " DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci")
    cursor.execute("SHOW DATABASES")
    for x in cursor:
        print(x)


def dbclearer():
    cursor.execute("USE " + DB_NAME)
    cursor.execute("DROP TABLE anchortable;")
    cursor.execute("DROP TABLE relevantanchorstable;")

    # TODO: delete and drop other tables


def dbdropper():
    cursor.execute("DROP DATABASE " + DB_NAME)
    cursor.execute("SHOW DATABASES")
    for x in cursor:
        print(x)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Utility tool to create, clear or drop database")
    parser.add_argument("operation", help="operation", choices=["create", "clear", "drop", "load"])
    args = parser.parse_args()
    operation = args.operation
    if operation == "create":
        dbcreator()
    if operation == "clear":
        dbclearer()
    if operation == "drop":
        dbdropper()
    mydb.commit()
    mydb.disconnect()
