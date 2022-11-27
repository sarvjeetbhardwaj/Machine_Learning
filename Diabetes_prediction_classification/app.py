from distutils.log import debug
import pickle
from flask import Flask,request,app,jsonify,url_for,render_template,redirect
import pandas as pd
import numpy as np

app = Flask(__name__)
classify_model = pickle.load(open('Diabetes_prediction.pkl','rb'))  ### Loading the  trained regression model
scalar = pickle.load(open('scaling.pkl','rb')) ### Loading the scaled picked file

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api', methods=['POST'])
def predict_api():
    data=request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1,-1))
    new_transformed_data = scalar.transform(np.array(list(data.values())).reshape(1,-1))
    output = classify_model.predict(new_transformed_data)
    print(output[0])
    return jsonify(output[0])

@app.route('/predict',methods=['POST'])
def predict():
    data=[float(x) for x in request.form.values()]
    final_input = scalar.transform(np.array(data).reshape(1,-1))
    print(final_input)
    output = classify_model.predict(final_input)[0]
    return render_template('home.html',prediction_text=f'The House price prediction is {output}')
    
    
if __name__=='__main__':
    app.run(debug=True)

