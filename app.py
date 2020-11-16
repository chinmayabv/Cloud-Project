from flask import Flask, jsonify, request
from recognize_video import predictVideo
app = Flask(__name__)

@app.route("/getstname",methods=['GET'])
def predict():
	name = predictVideo('face_detection_model','openface_nn4.small2.v1.t7','output/recognizer.pickle','output/le.pickle')
	return jsonify(name)
	
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000, debug=True)
