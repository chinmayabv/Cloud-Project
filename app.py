from flask import Flask, jsonify, request, render_template, redirect, url_for
from recognize_video import predictVideo
import os.path
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './dataset/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route("/getstname",methods=['GET'])
def predict():
	name = predictVideo('face_detection_model','openface_nn4.small2.v1.t7','output/recognizer.pickle','output/le.pickle')
	return jsonify(name)
	

@app.route("/Register",methods=['POST','GET'])
def register():
	if request.method == "POST":
		username = request.form["usernamesignup"]
		print(username)
		useremail = request.form["emailsignup"]
		print(useremail)
		userpwd = request.form["passwordsignup"]
		print(userpwd)
		userpwdconfirm = request.form["passwordsignup_confirm"]
		print(userpwdconfirm)
		uploaded_files = request.files.getlist("files[]")
		print(uploaded_files)
		filenames = []
		for file in uploaded_files:
			print("In for")
			if file and allowed_file(file.filename):
				# Make the filename safe, remove unsupported chars
				filename = secure_filename(file.filename)
				# Move the file form the temporal folder to the upload
				# folder we setup
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				#Save the filename into a list, we'll use it later
				filenames.append(filename)
		return render_template('Index.html')
	return render_template('Register.html')
	
@app.route("/Register/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
	
@app.route("/Login",methods=['GET'])
def login():
	return render_template('Login.html')
	
@app.route("/",methods=['GET'])
def home():
	return render_template('Index.html')
	
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000, debug=True)
   

