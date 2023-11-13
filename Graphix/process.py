from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import matplotlib

app = Flask(__name__)

# Set the Matplotlib backend to 'agg'
matplotlib.use('agg')

@app.route('/')
def index():
    return render_template('pg1.html')

@app.route('/Pput')
def Pput():
    return render_template('Pupload.html')

@app.route('/Bput')
def Bput():
    return render_template('Bupload.html')

@app.route('/Lput')
def Lput():
    return render_template('Lupload.html')

@app.route('/Pupload', methods=['POST'])
def Pupload():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    if file:
        data = pd.read_excel(file)

        plt.clf()
        plt.figure()
        plt.pie(data['Value'], labels=data['Category'], autopct='%1.1f%%')
        plt.title('Pie Chart')
        pie_chart_image = get_image()

        return render_template('Presult.html',pie_chart=pie_chart_image)
    
@app.route('/Bupload', methods=['POST'])
def Bupload():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    if file:
        data = pd.read_excel(file)

        plt.clf()
        plt.bar(data['Category'], data['Value'])
        plt.xlabel('Category')
        plt.ylabel('Value')
        plt.title('Bar Chart')
        bar_chart_image = get_image()

        return render_template('Bresult.html', bar_chart=bar_chart_image) 
    
# Function to generate the line chart and return it as a base64 image
@app.route('/Lupload', methods=['POST'])
def Lupload():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    if file:
        data = pd.read_excel(file)

    plt.clf()
    plt.figure(figsize=(8, 6))
    plt.plot(data['Category'], data['Value'], marker='o', linestyle='-')
    plt.xlabel('Category')
    plt.ylabel('Value')
    plt.title('Line Chart')
    line_chart_image = get_image()
    
    return render_template('Lresult.html', line_chart=line_chart_image)


def get_image():
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

if __name__ == '__main__':
    app.run(debug=True)

    
