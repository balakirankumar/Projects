import sqlite3
file_name="External.sqlite3"
connection=sqlite3.connect(file_name)
cursor=connection.cursor()
print("The tables in databse are :")
for i in cursor.execute("select name from sqlite_master where type='table';"):
    print(i)
print("Table info of 'statement'")
for i in cursor.execute("pragma table_info(statement);"):
    print(i)
print("Contents of 'statement' table are:")
for i in cursor.execute("select * from statement;"):
    print(i)

