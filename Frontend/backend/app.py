from flask import Flask, request, jsonify
import joblib
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the pre-trained model
model = joblib.load('NA_detectra.joblib')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.endswith('.txt'):
        return jsonify({"error": "Invalid file type. Only .txt files are allowed"}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    file.save(filepath)

    # Process the file (assuming the file contains rows of network data)
    with open(filepath, 'r') as f:
        data = f.readlines()

    # Prepare data for the model (modify as per your model's requirements)
    # For example, convert the input to a numerical feature vector
    feature_vector = process_data(data)

    # Use the model to predict anomalies
    prediction = model.predict([feature_vector])[0]
    result = "Anomaly Detected" if prediction == 1 else "No Anomaly Detected"

    return jsonify({"analysis": result})

def process_data(data):
    """
    Process the input text data to create a feature vector for the model.
    Modify this function based on your model's requirements.
    """
    # Example: return the length of each line as a feature
    return [len(line.strip()) for line in data]

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
