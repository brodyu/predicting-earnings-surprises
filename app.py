import pandas as pd
import numpy as np
from flask import Flask, render_template

app = Flask(__name__)

# TODO: Load model pkl file here

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    pass

if __name__ == "__main__":
    app.run(debug=True)
