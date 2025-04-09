# import the sqlite3 library
import sqlite3

# create a connection to sqlite3
connection = sqlite3.connect("student.db")  # corrected the connection method

# create a cursor object to insert records and create the table
cursor = connection.cursor()

# create table
new_table = """ 
CREATE TABLE STUDENT (
    NAME VARCHAR(20),
    CLASS VARCHAR(20),
    SECTION VARCHAR(20),
    MARKS INT
)
"""

cursor.execute(new_table)

# Insert some records into the table
cursor.execute('''INSERT INTO STUDENT VALUES("Ram", "Data Science", "A1", 90)''')
cursor.execute('''INSERT INTO STUDENT VALUES("Shyam", "Machine Learning", "B2", 99)''')
cursor.execute('''INSERT INTO STUDENT VALUES("Hari", "Artificial Intelligence", "C3", 95)''')
cursor.execute('''INSERT INTO STUDENT VALUES('Jacob', 'DEVOPS', 'A2', 50)''')
cursor.execute('''INSERT INTO STUDENT VALUES('Dipesh', 'DEVOPS', 'A2', 35)''')

# display all the records
print("The inserted records are:\n") 
display = cursor.execute('''SELECT * FROM STUDENT''')
for row in display:
    print(row)

# commit changes and close the connection
connection.commit()
connection.close()
