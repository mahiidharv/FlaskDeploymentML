# Import libraries
#import numpy as np
import os
import pandas as pd
from flask import Flask, request, jsonify, Response,render_template
from werkzeug import secure_filename
from sklearn.metrics import classification_report
#import json

app = Flask(__name__)
from joblib import load 
# Load the model
model = load('./pickle/best_decision_tree.pkl')
#outputcsv = pd.DataFrame()
@app.route('/')
def index():
   return render_template('upload.html')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
@app.route('/upload',methods=['POST'])
def upload():
    
    target = os.path.join(APP_ROOT,'data/')
    print(target)
    if not os.path.isdir(target):
      os.mkdir(target)
    
    file= request.files['file']

    if file:
      filename = secure_filename(file.filename)
      destination = '/'.join([target,filename])
      data = pd.read_csv(file)
      print(data.columns)
      print(destination)
      data.to_csv(destination)
      #data = data.drop('rowno',axis =1)
      
     
    
            
    return render_template('layout.html')#,output = outputcsv.to_html())

		
@app.route('/submit',methods=['GET','POST'])
def submit():
    target = os.path.join(APP_ROOT,'result/')
    print(target)
    if not os.path.isdir(target):
      os.mkdir(target)
    if request.form.getlist("display"):
        data = pd.read_csv("./data/test_cases.csv",index_col=[0])
        print("Readng data \n",data.columns)
        try:
            data = data.drop('y',axis=1)
            data = data.reset_index(drop=True)
            
        except:
            pass
        print(data.columns)
        prediction = model.predict(data)
        output = prediction
        output = output.tolist()
        data['prediction'] = output
        cols = data.columns
        col = [cols[0]]+[cols[len(cols)-1]]+[colu for colu in cols[1:len(cols)-1]]
        print(col)
        data = data.reindex(columns=col)
        outputcsv = data

        destination = '/'.join([target,"output.csv"])
        outputcsv.to_csv(destination,index=False)
        
        return render_template('submit.html',output = outputcsv.to_html())
    else:
        
        outputcsv = pd.read_csv("./result/output.csv")
        try:
            outputcsv = outputcsv.drop(['Unnamed: 0','Unnamed: 0.1'],axis=1)
        except:
            pass
        print(outputcsv.columns)
        csv = outputcsv.to_csv()
        print(type(csv))
        return Response(
                csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=result.csv"})

'''

@app.route('/api',methods=['POST'])
def predict():
    # Get the data from the POST request.
    test_data = request.json
    print(test_data)
    print(type(test_data))

    temp = pd.DataFrame.from_dict(test_data,orient='index')
    print(type(temp))
    
    prediction = model.predict(temp.T)
    
    output = prediction
    output = output.tolist()[0]

    #return jsonify(output)
    return render_template("main/layout.html",output= output)
'''
if __name__ == '__main__':
    
    app.run(debug=True)
    