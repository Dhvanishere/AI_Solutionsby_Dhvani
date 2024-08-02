from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

def analyze_data(file):
    df = pd.read_csv(file)
    
    head_html = df.head().to_html(classes='table table-striped')
    description_html = df.describe().to_html(classes='table table-striped')
    missing_values_html = df.isnull().sum().to_frame(name='Missing Values').to_html(classes='table table-striped')
    data_types_html = df.dtypes.to_frame(name='Data Type').to_html(classes='table table-striped')
    unique_values_html = df.nunique().to_frame(name='Unique Values').to_html(classes='table table-striped')

    return head_html, description_html, missing_values_html, data_types_html, unique_values_html

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('file')
    if file is None:
        return "No file uploaded", 400

    head, description, missing_values, data_types, unique_values = analyze_data(file)

    return render_template('results.html', head=head, description=description, 
                           missing_values=missing_values, data_types=data_types, 
                           unique_values=unique_values)

if __name__ == '__main__':
    app.run(debug=True)
