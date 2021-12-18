import pandas as pd
import numpy as np
from flask import Flask

app = Flask(__name__)

# TODO: Load model pkl file here

@app.route("/")
def home():
    # TODO: Render HTML template with render_template method
    pass

@app.route('predict', methods=['POST', 'GET'])
def predict():
    pass

if __name__ == "__main__":
    app.run(debug=True)
