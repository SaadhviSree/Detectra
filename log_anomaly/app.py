from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from werkzeug.utils import secure_filename
import os
import webbrowser  # For opening the browser automatically
from log import detect_windows_log_anomalies  # Your anomaly detection function

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')  # Just shows file upload page

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the file and run anomaly detection
        data = pd.read_csv(filepath)
        results, silhouette, plot = detect_windows_log_anomalies(data)
        
        # Preparing results to show
        anomaly_summary = {
            'silhouette_score': silhouette,
            'isolation_forest_anomalies': results['is_anomaly_isolation'].sum(),
            'dbscan_anomalies': results['is_anomaly_dbscan'].sum(),
        }
        top_anomalies_html = results[['DateTime', 'Level', 'Component', 'EventId', 'EventTemplate']].head().to_html(classes='table')
        
        # Convert plot to base64 string for embedding in HTML
        img_str = plot_to_base64(plot)  # Function to convert plot to base64 string
        
        # Render result page with anomaly results and the base64 image
        return render_template('result.html', anomaly_summary=anomaly_summary, top_anomalies_html=top_anomalies_html, img_str=img_str)
    return redirect(url_for('index'))  # Redirect back to upload page if no file uploaded

def plot_to_base64(plot):
    import io
    import base64
    img = io.BytesIO()
    plot.savefig(img, format='png')  # Save the plot in PNG format
    img.seek(0)
    img_str = base64.b64encode(img.getvalue()).decode('utf-8')
    return img_str

if __name__ == '__main__':
    # Automatically open the default browser to the app URL
    port = 5000  # Default Flask port
    url = f'http://127.0.0.1:{port}/'
    print(f"Starting Flask app at {url}")
    
    # Open the browser
    webbrowser.open(url)
    
    # Run the Flask app
    app.run(debug=True, port=port)
