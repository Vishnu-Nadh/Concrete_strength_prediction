# Concrete Compressive Strength Prediction

The quality of concrete is determined by its compressive strength, which is measured
using a conventional crushing test on a concrete cylinder. The strength of the concrete
is also a vital aspect in achieving the requisite longevity. It will take 28 days to test
strength, which is a long period. So, what will we do now? We can save a lot of time and
effort by using Data Science to estimate how much quantity of which raw material we
need for acceptable compressive strength. This is what accomplished by this project.
Predict the compressive strength by providing the composition of materials either as a
single sample value or as a batch file of many sample input Data.

## Demo

![App Demo](static/images/values.gif)
![App Demo](static/images/csv.gif)

## Tech Stack

- **Client:** HTML, CSS, JavaScript

- **Server:** Python with libraries xgboost, scikit-learn, pandas, numpy

- **API Framework:** Python Flask==2.0.2

## Deployed Link

This project is deployed in the cloud service of Heroku using docker and Circle CI to establish countinous intergration and continous development.

- App link : [Concrete_strength_predictor]()

## Run App Locally

To run the App locally python version 3.6 or higher should be installed in your computer

Clone the project

Go to the project directory you want to clone the project files

```bash
  cd your-project-directory
```

```bash
  git clone https://github.com/Vishnu-Nadh/Concrete_strength_prediction.git
```

Install dependencies

Choose your python environment to install dependencies and install the libaries using below commant in terminal

```bash
  pip install -r requirements.txt
```

Start the server

```bash
    python app.py
```

Press Enter and visit the app from local host url shown in the terminal. Use csv data from the folder "Prediction_Input" to test the app

## Reflection

- The data used was not much challengng and having of nummerical values only. Non normal distribution of some features are solved by logarithamic tranformation and followed by standered scaling
- Tried of different algorithms. Out of those Linear regression with polynomial degree of 2 , random forest regression and xgboost regression showed the best results. Since xgboost showed less overfitting it choosed for model training.
- Entire training pipeline (Retraining when new data set is being added to the directory to update the model) is implimented. For database storage sqlite database is used
- Two prediction pipelines are implemented. One to predict from user input values and other from predition batch file for mass sample prediction
- UI is created using HTML, CSS and javascript. Form validations (eg: non csv input,blank input, Incorrect format of prediction data etc) are established. Entire interphase is done using ajax and the web application is completely responsive in nature.

## 🚀 About Me

- 📈I'm a Data scientist...
- 🖥Full stack python developer..
- 💻Tech enthusiast..
- 📖Avid learner..

## 🔗 Links

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vishnunadh/)
