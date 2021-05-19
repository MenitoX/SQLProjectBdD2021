import cx_Oracle, os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv('USER')
PASS = os.getenv('PASS')
URL  = os.getenv('URL')

connection = cx_Oracle.connect(USER,PASS,URL)
print("Database version:", connection.version)
#cursor = connection.cursor()



#cursor.execute (
#        """
#            CREATE TABLE Persona(
#                person_id NUMBER GENERATED BY DEFAULT AS IDENTITY,
#                first_name VARCHAR2(50) NOT NULL,
#                last_name VARCHAR2(50) NOT NULL,
#                PRIMARY KEY(person_id)
#            )
#        """
#        )

#cursor.execute(
#    """
#        SELEcT first_name, last_name, person_ID
#        FROM Persona
#    """
#)
#for fname, lname, person_id in cursor:
#    print("Values:", fname, lname, person_id)


connection.close()