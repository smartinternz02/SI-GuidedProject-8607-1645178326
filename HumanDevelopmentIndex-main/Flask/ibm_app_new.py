
import numpy as np
import pandas as pd
from flask import Flask, render_template, request
import pickle
import requests

import json

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "MKtwemgwfSBrHqrHo6G4LSAKJYeYmrBXAvwknwXhMC9C"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
app = Flask(__name__)
#model = pickle.load(open('HDI.pkl','rb'))
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/Prediction',methods=['POST','GET'])
def prediction():
    return render_template('indexnew.html')
@app.route('/Home',methods=['POST','GET'])
def my_home():
     return render_template('home.html')
@app.route('/predict',methods=['POST','GET'])
def predict():
     input_features = [int(x) for x in request.form.values()]
     print(input_features)
     print(type(input_features))
     features_value = [np.array(input_features)]
     
     features_name = ['Country','Life expectancy','Mean years of schooling','Gross national income (GNI) per capita','Internet Users']
     # NOTE: manually define and pass the array(s) of values to be scored in the next line
     payload_scoring = {"input_data": [{"field": [["Country","Life expectancy","Mean years of schooling","Gross national income (GNI) per capita","Internet users"]], "values": [input_features] }]}

     response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/d92780dd-ae7d-4a4c-afa7-403ee369f344/predictions?version=2022-03-03', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
     # print("Scoring response")
     predictions = response_scoring.json()


     print(response_scoring.json())
     output = predictions['predictions'][0]['values'][0][0][0]
    # print(output)

     
   #  df = pd.DataFrame(features_value, columns=features_name)
     
     #predictions using the loaded model file
     #output = model.predict(df)
    # print(round(output[0][0],2))
     print(type(output))
     y_pred = output
     print(y_pred)
     if(y_pred >= 0.3 and y_pred <= 0.4) :
        return render_template("resultnew.html",prediction_text = 'Low HDI- ' + str(y_pred))
     elif(y_pred >= 0.4 and y_pred <= 0.7):
        return render_template("resultnew.html",prediction_text = 'Medium HDI- ' + str(y_pred))
     elif(y_pred >= 0.7 and y_pred <= 0.8):
        return render_template("resultnew.html",prediction_text = 'High HDI- ' + str(y_pred))
     elif(y_pred >= 0.8 and y_pred <= 0.94):
        return render_template("resultnew.html",prediction_text = 'Very High HDI- ' + str(y_pred))
     else :
        return render_template("resultnew.html",prediction_text = 'The given values do not match the range of values of the model. Try giving the values in the mentioned range'+str(y_pred))
     return render_template('result.html', prediction_text=output)
 
if __name__ == '__main__':
    app.run(debug=False,port=5000)
    