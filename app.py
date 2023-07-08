import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__, static_url_path='/static')
app.template_folder = 'templates'
model=pickle.load(open('cancer.pkl','rb'))

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        features = []
        for value in request.form.values():
            if value != 'submit':  # Skip the 'submit' value
                features.append(int(value))
        final_features = [np.array(features)]
        final_features = pd.DataFrame(final_features, columns=['Cosmic_ID', 'Drug_ID', 'TCGA_Classification', 'PSA', 'Tissue', 'Tissue_Sub-type', 'IS_Mutated'])
        prediction = model.predict(final_features)
        output = prediction[0]
    return render_template('index.html', prediction_text='Cancer cell IC50 value is {}'.format(output))

    
if __name__=='__main__':
	app.run()