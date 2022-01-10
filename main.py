from wsgiref import simple_server
from logging import exception
from flask import Flask, render_template, request, flash, jsonify, url_for
from flask_cors import cross_origin, CORS
import flask_monitoringdashboard as dashboard
import os

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/predict_from_values", methods = ['GET', 'POST'])
@cross_origin()
def predictFromValue():
    try:
        if request.method == 'POST':
            pass
        else:
            return render_template('index.html')
    except exception as e:
         raise e
        
@app.route("/predict_from_csv", methods = ['GET', 'POST'])
@cross_origin()
def predictFromCSV():
    try:
        if request.method == 'POST':
            pass
        else:
            return render_template('predictCSV.html')
    except exception as e:
         raise e


port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    host = '0.0.0.0'
    httpd = simple_server.make_server(host, port, app)
    print("Serving on %s %d" % (host, port))
    httpd.serve_forever()
