from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, make_response, session
from recognize import predictimg , extr_emb,train_mod
from connect import connection
from flask import Flask, jsonify, request, render_template, redirect, url_for
from recognize import predictimg
import os.path
from werkzeug.utils import secure_filename
import datetime
import subprocess
import zipfile


UPLOAD_FOLDER = './zipdataset/'
UNZIP_FOLDER = './dataset/'
Check_Folder = './classphoto/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','zip'}

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UNZIP_FOLDER'] = UNZIP_FOLDER
app.config['CHECK_FOLDER'] = Check_Folder
app.secret_key = 'any random string'


@app.route("/index")
def index():
	if 'username' in session:
		username = session['username']
		getidsql = "Select studentid From Student where name = %s"
		value = (username,) 
		try:
			c, conn = connection()
			c.execute(getidsql,value)
			result = c.fetchall()
			#print(result)
			for x in result:
				presentcountsql = "Select Count(*) from Attedance Where Stid = %s;"
				totalclasscount = "Select count(distinct(date)) from Attedance;"
				val = (x[0],)
				c.execute(presentcountsql,val)
				getAttendance = c.fetchall()
				percent = 0
				for att in getAttendance:
					percent += att[0]
				c.execute(totalclasscount)
				gettotalclass = c.fetchall()
				for classcount in gettotalclass:
					if classcount[0] != 0:
						percent /= classcount[0]
				percentage = percent*100
				return render_template('Percentage.html', percentvalue=percentage,stname=username)
			 
		except Exception as e:
			return(str(e))
	else:
		return render_template('Index.html')


@app.route("/getstname",methods=['GET','POST'])
def predict():
	if request.method == "POST":
		ts = datetime.datetime.now().timestamp()
		#print(ts)
		uploaded_files = request.files.getlist("files[]")
		#print(uploaded_files)
		filenames = []
		for file in uploaded_files:
			print("In for")
			if file and allowed_file(file.filename):
				# Make the filename safe, remove unsupported chars
				filename = secure_filename(file.filename)
				# Move the file form the temporal folder to the upload
				# folder we setup
				file.save(os.path.join(app.config['CHECK_FOLDER'], filename))
				#Save the filename into a list, we'll use it later
				filepath = Check_Folder+filename
				today = datetime.date.today()
				today1 = today.strftime("%m_%d_%Y")
				result_img = today1+"_"+filename
				os.system("gsutil cp "+filepath+" gs://class_imgs")
				name = predictimg(filepath,filename)
				flag = insertAttendance(name)
				
				#imgsrcurl = "https://storage.googleapis.com/class_imgs/"+result_img
				if flag==True:
					return render_template('1.html')
	return render_template('Attendance.html')


		
@app.route("/CheckName/<stname>",methods=['GET','POST'])
def checkname(stname):
	if request.method == "POST":
		print("In post")
		print(stname[0])
		flag = insertAttendance(stname)
		return"<h1> Success</h1>"
		return redirect(url_for('checkname',stname=name))
	return render_template('Attendance.html')
	
@app.route("/CheckName/<stname>",methods=['GET','POST'])
def checkName(stname):
	if request.method == "POST":
		return"<h1> Success</h1>"
	return render_template('Checkname.html',name=stname)
		
@app.route("/Register",methods=['POST','GET'])
def register():
	if request.method == "POST":
		username = request.form["usernamesignup"]
		#print(username)
		useremail = request.form["emailsignup"]
		#print(useremail)
		userpwd = request.form["passwordsignup"]
		#print(userpwd)
		userpwdconfirm = request.form["passwordsignup_confirm"]
		#print(userpwdconfirm)
		uploaded_files = request.files.getlist("files[]")
		#print(uploaded_files)
		filenames = []
		dbstorename = ""
		for file in uploaded_files:
			str1 = file.filename
			leng = len(str1)
			dbstorename = str1[:leng-4]
			print(dbstorename)
			if file and allowed_file(file.filename):
				# Make the filename safe, remove unsupported chars
				filename = secure_filename(file.filename)
				
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				#Save the filename into a list, we'll use it later
				usrfolder = UPLOAD_FOLDER+filename
				extrfolder = UNZIP_FOLDER+username
				path = os.path.join(UNZIP_FOLDER, username)
				print(usrfolder)
				with zipfile.ZipFile(usrfolder, 'r') as zip_ref:
					zip_ref.extractall(UNZIP_FOLDER)
				size = len(filename)
				os.rename(r'./dataset/'+str(filename[:size - 4]),r'./dataset/'+str(username))
				filenames.append(filename)
			
		print("Calling sql method")
		flag = registerStudent(username,useremail,userpwd,dbstorename)		
		print(flag)
		if flag == False:
			return "<h1> Record exists try a different username </h1>"
		else:
			session['username'] = username
			extr_emb()
			print("Extracted embeddings")
			train_mod()
			print("Model trained")
			return redirect(url_for('index'))
	return render_template('Register.html')

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))


@app.route("/Register/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename) 


@app.route("/Login",methods=['GET','POST'])
def login():
	if request.method == "POST":
		username = request.form["username"]
		print(username)
		session['username'] = username
		userpwd = request.form["password"]
		print(userpwd)
		#keeplogin = request.form["loginkeeping"]
		#print(keeplogin)
		authenticate = uservalidation(username,userpwd)
		if authenticate==True:
			return redirect(url_for('index'))
	return render_template('Login.html')
	
@app.route("/",methods=['GET'])
def home():
	return render_template('Index.html')


@app.route("/admin/sql/createstudent",methods=['GET'])
def createstudenttbl():
	createTable()
	return '<h1>created table<h1>'
	

@app.route("/admin/Checkconnect/",methods=['GET','POST'])
def checkconnect():
	try:
		c, conn = connection()
		c.execute('''SELECT * from Attedance''')
		rv = c.fetchall()
		print(rv)
		return("okay")
	except Exception as e:
		return(str(e))
		
def registerStudent(username,useremail,userpwd,dbstorename):
	try:
		c, conn = connection()
		sqlselect = "SELECT * from Student where name = %s"
		value = (username,)
		c.execute(sqlselect,value)
		result = c.fetchall()
		print(username)
		for x in result:
			return False
		sql = "Insert into Student(name,email,password,filename) Values(%s,%s,%s,%s);"
		val = (username,useremail,userpwd,dbstorename)
		c.execute(sql,val)
		conn.commit()
		return True
	except Exception as e:
		return(str(e))
	
def uservalidation(username,userpwd):
	try:
		c, conn = connection()
		sqlselect = "SELECT password from Student where name = %s"
		value = (username,)
		c.execute(sqlselect,value)
		result = c.fetchall()
		print(username)
		for x in result:
			print(x)
			if x[0] == userpwd:
				print("in if")
				return True
		return False
	except Exception as e:
		return(str(e))
		


def insertAttendance(stname):
	print(stname)
	try:
		print("In try")
		c, conn = connection()
		today = datetime.date.today()
		yesterday = today - timedelta(days = 1)
		print(stname)
		i=0
		while i < len(stname):
			name = stname[i]
			sql = "Select studentid From Student where name = %s"
			value = (name,) 
			c.execute(sql,value)
			result = c.fetchall()
			#print(result)
			for x in result:
				insertsql = "Insert into Attedance(Stid,date) Values(%s,%s);"
				val = (x[0],yesterday)
				c.execute(insertsql,val)
				conn.commit()
			i=i+1
		return True
	except Exception as e:
		#print(str(e))
		return(str(e))
	
	
	
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000, debug=True)
   

