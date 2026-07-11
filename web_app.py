from flask import Flask, render_init, send_file
import os
from analysis import DataAnalyzer

app = Flask(__name__)

# Initialize your logic with dataset.csv
analyzer = DataAnalyzer("dataset.csv")
analyzer.load_data()
stats = analyzer.compute_statistics()

@app.route('/')
def home():
    return render_template('index.html', stats=stats)

@app.route('/get_chart/<chart_type>')
def get_chart(chart_type):
    # Match tabs dynamically to files saved inside your charts directory
    chart_mapping = {
        'bar': 'category_sales_chart.png',
        'pie': 'city_orders_chart.png',
        'line': 'region_orders_chart.png',
        'histogram': 'category_sales_chart.png' # Fallback or custom histogram image name
    }
    
    filename = chart_mapping.get(chart_type, 'category_sales_chart.png')
    # If files are directly in root or inside charts folder, update path
    filepath = os.path.join(os.getcwd(), filename)
    if not os.path.exists(filepath):
        filepath = os.path.join(os.getcwd(), 'charts', filename)
        
    return send_file(filepath, mime_type='image/png')

if __name__ == '__main__':
    app.run(debug=True)