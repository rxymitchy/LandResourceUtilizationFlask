import joblib
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the trained model
model = joblib.load('random_forest_model.pkl')
scaler = joblib.load('scaler.pkl')

# Possible zoning types
possible_zoning_types = ['Residential', 'Commercial','Mixed-Use']

def encode_zoning(zoning_type):
    return [1 if zoning == zoning_type else 0 for zoning in possible_zoning_types]

@app.route('/')
def home():
    return render_template('index.html', possible_zoning_types=possible_zoning_types)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get the input values from the form
        area_id = float(request.form['area_id'])
        density = float(request.form['density'])
        housing_units = float(request.form['housing_units'])
        available_land = float(request.form['available_land'])
        max_density = float(request.form['max_density'])
        greenspace = float(request.form['greenspace'])
        zoning_type = request.form['zoning_type']

        # Subtract greenspace from available land
        available_land_after_greenspace = available_land - greenspace

        # Encode the zoning type
        zoning_encoding = encode_zoning(zoning_type)

        # Concatenate the features including the one-hot encoded zoning type
        features = [area_id, density, housing_units, available_land_after_greenspace, max_density, greenspace] + zoning_encoding

        # Ensure we only use 7 features
        features = features[:7]

        # Scale the features
        scaled_features = scaler.transform([features])
        
        # Predict using the model
        prediction = model.predict(scaled_features)
        result = "Land is available for development." if prediction[0] == 1 else "Land is not available for development."

        return render_template('index.html', result=result, possible_zoning_types=possible_zoning_types)

if __name__ == '__main__':
    app.run(debug=True)
