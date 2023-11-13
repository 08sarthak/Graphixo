from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import threading
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'  # Create a folder for uploading files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# A function to generate the chart image
def generate_pie_chart(data, filename):
    plt.figure(figsize=(8, 8))
    plt.pie(data['Data'], labels=data['Category'], autopct='%1.1f%%')
    plt.title('Pie Chart')
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()

    # Delete the uploaded file after use
    os.remove(filename)

    return chart_url

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']

    if file.filename == '':
        return 'No selected file'
    
    if file:
        # Save the uploaded file to the designated folder
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Read the Excel file into a DataFrame
        df = pd.read_excel(filename)
        
        # Create a separate thread to generate the chart image
        chart_url = generate_pie_chart(df, filename)
        
        return render_template('result.html', chart_url=chart_url)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)

