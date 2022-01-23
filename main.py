from distutils.log import error
from wsgiref import simple_server
from logging import exception
from flask import Flask, render_template, request, jsonify, url_for, make_response
from flask_cors import cross_origin, CORS
import flask_monitoringdashboard as dashboard
import os

os.putenv("LANG", "en_US.UTF-8")
os.putenv("LC_ALL", "en_US.UTF-8")

app = Flask(__name__)
dashboard.bind(app)
CORS(app)

app.config["SECRET_KEY"] = "80c2f0634018c50157ef1ff885b0fa3190423755"
root_dir = os.getcwd()
app.config["INPUT_DATA_PATH"] = os.path.join(root_dir, "Prediction_Input")
app.config["SENT_RESULT_PATH"] = os.path.join(root_dir, "Predicted_Output")


@app.route("/", methods=["GET"])
@cross_origin()
def home():
    return render_template("index.html")


@app.route("/train", methods=["GET", "POST"])
@cross_origin()
def trainModel():
    try:
        if request.method == "POST":
            if request.json["start"]:

                """model training goes here"""
                output = "Model training completed!"
                return jsonify(output)
                # return render_template('index.html')
        else:
            return render_template("index.html")
    except exception as e:
        raise e


@app.route("/predict_from_values", methods=["GET", "POST"])
@cross_origin()
def predictFromValue():
    try:
        if request.method == "POST":
            data_dict = request.json
            output = "45 Mpa"
            return jsonify(output)
            # return render_template('index.html')
        else:
            return render_template("index.html")
    except exception as e:
        raise e


@app.route("/predict_from_csv", methods=["GET", "POST"])
@cross_origin()
def predictFromCSV():
    try:
        if request.method == "POST":
            file = request.files["file"]
            print(file)
            print(file.filename)
            file.save(
                os.path.join(app.config["INPUT_DATA_PATH"], "prediction_data.csv")
            )
            """schema validation goes here"""

            # status = 'success'
            dic = {
                # "status" : "error",
                "status": "success",
                "val_error": "validation error message",
            }
            if dic["status"] == "error":
                return jsonify(dic)
            else:
                """prediction calculation goes here"""
                return jsonify(dic)
        else:
            return render_template("predictCSV.html")
    except exception as e:
        raise e


port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    host = "0.0.0.0"
    httpd = simple_server.make_server(host, port, app)
    print(f"Serving on {host}:5000")
    httpd.serve_forever()
