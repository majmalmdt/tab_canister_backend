import sqlite3

conn = sqlite3.connect("hospital.sqlite")

cursor = conn.cursor()
sql_query = """ CREATE TABLE patient (
    id integer PRIMARY KEY,
    Name text NOT NULL,
    Address text NOT NULL,
    Pin text NOT NULL,
    DOB text NOT NULL,
    BloodGroup text NOT NULL,
    ContactNumber text NOT NULL,
    EmergencyContactNumber text NOT NULL,
    Email text NOT NULL,
    password text NOT NULL,
    image text NULL
)"""
sql_query2 = """ CREATE TABLE patientdetails (
    id integer PRIMARY KEY,
    HealthIssues text NOT NULL,
    DoctorName text NOT NULL,
    Medicine text NOT NULL,
    DoctorsContactNumber text NOT NULL 
)"""

sql_query3 = """ CREATE TABLE medicinedetails (
    id integer PRIMARY KEY,
    MedName text NOT NULL,
    Doses integer NOT NULL,
    count integer NOT NULL,
    Temparature integer NOT NULL 
)"""



# cursor.execute(sql_query)
# cursor.execute(sql_query2)
cursor.execute(sql_query3)