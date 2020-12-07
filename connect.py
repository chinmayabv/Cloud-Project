import mysql.connector
from mysql.connector.constants import ClientFlag

def connection():
	config = {
		'user': 'root',
		'password': 'testdbpwd',
		'host': '104.198.52.49',
		'client_flags': [ClientFlag.SSL],
		'database': 'testdb',
		'ssl_ca': 'server-ca.pem',
		'ssl_cert': 'client-cert.pem',
		'ssl_key': 'client-key.pem'
	}

	# now we establish our connection
	cnxn = mysql.connector.connect(**config)
	print(cnxn)

	cursor = cnxn.cursor()  # initialize connection cursor # create a new 'testdb' database
	return cursor,cnxn
	
	
def createStudent():
	c, conn = connection()
	#c.execute('Create Database Attendancemgmt')
	c.execute('CREATE TABLE Student (studentid int NOT NULL AUTO_INCREMENT,name varchar(255),email varchar(255), password varchar(255),    filename varchar(255), PRIMARY KEY (studentid));')
	conn.commit()
	conn.close()
	
def createProfessor():
	c, conn = connection()
	c.execute('CREATE TABLE Professor(Profid int NOT NULL AUTO_INCREMENT,username varchar(255),email varchar(255),password varchar(255), Department varchar(255), PRIMARY KEY(Profid));')
	conn.commit()
	conn.close()
	
def createClass():
	c, conn = connection()
	c.execute('CREATE TABLE Professor(Classid int NOT NULL AUTO_INCREMENT,classname varchar(255),Pid int,Timings varchar(255),Totalmeets int, PRIMARY KEY(Classid),Foreign );')
	conn.commit()
	conn.close()
	
def createAttendance():
	c, conn = connection()
	c.execute('CREATE TABLE Attedance(Stid int,date varchar(255), Foreign Key(Stid) References Student(studentid) On delete Cascade On update cascade);')

def deleteRecord():
	c, conn = connection()
	c.execute('Delete From Student Where studentid=3')
	conn.commit()
	conn.close()

def truncateRecord():
	c, conn = connection()
	c.execute('Truncate Table Attedance')
	conn.commit()
	conn.close()
if __name__ == "__main__":
	truncateRecord()
