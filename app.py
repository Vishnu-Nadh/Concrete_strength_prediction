from wsgiref import simple_server
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import cross_origin, CORS
import flask_monitoringdashboard as dashboard
import os
import pandas as pd
from trainingValidationInsertion import Train_Validation
from predictionDataValidation import Predicton_Data_Validation
from trainingModel import Train_Model
from Data_Preprocessing.preprocessPredVals import PreprocessVals
from PredictOutput import Predict_Output


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
                path = "Training_Batch_Files/"
                train_validation = Train_Validation(path)
                train_validation.training_data_validation()

                """model training goes here"""
                trainmodel = Train_Model()
                trainmodel.trainModel()

                output = "Model training Completed"
                return jsonify(output)
                # return render_template('index.html')
        else:
            return render_template("index.html")

    except Exception as e:
        raise e


@app.route("/predict_from_values", methods=["GET", "POST"])
@cross_origin()
def predictFromValue():
    try:
        if request.method == "POST":
            data_dict = request.json
            data = pd.json_normalize(data_dict).astype(float)
            preprocess = PreprocessVals(data)
            data = preprocess.preprocessPredvalues()
            predict = Predict_Output()
            output = str(predict.predictFromValues(data))
            return jsonify(output)
        else:
            return render_template("index.html")

    except Exception as e:
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
            csvValidation = Predicton_Data_Validation(
                "Prediction_Input/prediction_data.csv"
            )
            dic = csvValidation.predictionCSVvalidation()

            print(dic)

            if dic["status"] == "error":
                return jsonify(dic)
            else:
                """prediction calculation goes here"""
                predict = Predict_Output()
                response = predict.predictFromCSV()
                print(response)
                return jsonify(dic)
        else:
            return render_template("predictCSV.html")
    except Exception as e:
        raise e


@app.route("/download_result", methods=["GET", "POST"])
def download_result():
    path = os.path.join(app.config["SENT_RESULT_PATH"], "predictions.csv")
    return send_file(path, "predictions.csv", as_attachment=True)


# port = int(os.getenv("PORT", 5000))
# if __name__ == "__main__":
#     host = "0.0.0.0"
#     httpd = simple_server.make_server(host, port, app)
#     print(f"Serving on {host}:5000")
#     httpd.serve_forever()

if __name__ == "__main__":
    app.run(debug=True)
