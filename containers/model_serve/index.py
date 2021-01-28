from flask import Flask, request
from flask import jsonify
import json

app = Flask(__name__)

from joblib import load
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import os
 
clf = None 
# Download model and cluster_names from s3
def loadModel():
    global clf
    model = os.environ["MODELFILENAME"]
    bucket = os.environ["BUCKET"]
    # Model download
    # Load model file
    clf = load(model+'.pkl')
    print("model loaded")

@app.route('/')
def hello():
    return "hello :)"

@app.route('/predict', methods=["POST"])
def predict():
    global clf
    data = json.loads(json.dumps(request.get_json()))
    data = { "prediction": clf.predict([data["data"]])[0] }
    return jsonify(data),200,{'Content-Type': 'application/json'}

@app.route('/_health')
def _health():
    return "_health"

if __name__ == '__main__':
    loadModel()
    app.run(host='0.0.0.0', port=5431, debug=True)
