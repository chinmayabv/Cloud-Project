import mysql.connector

def connection():
    conn = mysql.connector.connect(user = "chinmay",password = "Password@sql1",host="localhost",database = "AttendanceMgmt")
    c = conn.cursor()
    return c, conn
