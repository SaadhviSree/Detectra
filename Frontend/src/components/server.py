from flask import Flask, jsonify, send_file
from pathlib import Path
import json
import matplotlib.pyplot as plt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define the output directory where the forensic data is saved
OUTPUT_DIR = Path("forensics_output/20241229_030319")  # Use forward slashes

# Dummy data for generating charts
MEMORY_INFO = {"used": 8 * 1024**3, "available": 16 * 1024**3}  # Bytes
NETWORK_CONNECTIONS = [
    {"status": "established", "count": 25},
    {"status": "listening", "count": 10},
    {"status": "closed", "count": 5},
]


@app.route("/system_info.json")
def get_system_info():
    return get_json_response("system_info.json")


@app.route("/running_processes.json")
def get_running_processes():
    return get_json_response("running_processes.json")


@app.route("/network_connections.json")
def get_network_connections():
    return get_json_response("network_connections.json")


@app.route("/memory_info.json")
def get_memory_info():
    return get_json_response("memory_info.json")


@app.route("/suspicious_processes.json")
def get_suspicious_processes():
    return get_json_response("suspicious_processes.json")


@app.route("/suspicious_connections.json")
def get_suspicious_connections():
    return get_json_response("suspicious_connections.json")


@app.route("/suspicious_files.json")
def get_suspicious_files():
    return get_json_response("suspicious_files.json")


def get_json_response(filename):
    try:
        file_path = OUTPUT_DIR / filename
        print(f"Attempting to read: {file_path}")  # Debug print
        if file_path.exists():
            with open(file_path, "r") as f:
                data = json.load(f)
            return jsonify(data), 200
        else:
            print(f"File not found: {file_path}")  # Debug print
            return jsonify({"error": f"{filename} not found"}), 404
    except Exception as e:
        print(f"Error reading file: {str(e)}")  # Debug print
        return jsonify({"error": str(e)}), 500


# Helper Function to Create Pie Chart
def create_pie_chart(memory_info):
    labels = ['Used', 'Available']
    sizes = [memory_info['used'], memory_info['available']]
    colors = ['#FF8042', '#00C49F']

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    output_path = 'memory_pie_chart.png'
    plt.savefig(output_path)
    plt.close()
    return output_path


# Helper Function to Create Bar Chart
def create_bar_chart(network_connections):
    labels = [conn['status'] for conn in network_connections]
    counts = [conn['count'] for conn in network_connections]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, counts, color='#8884d8')
    plt.xlabel('Connection Status')
    plt.ylabel('Count')
    plt.title('Network Connections')
    output_path = 'network_bar_chart.png'
    plt.savefig(output_path)
    plt.close()
    return output_path


@app.route("/memory-chart")
def memory_chart():
    chart_path = create_pie_chart(MEMORY_INFO)
    return send_file(chart_path, mimetype="image/png")


@app.route("/network-chart")
def network_chart():
    chart_path = create_bar_chart(NETWORK_CONNECTIONS)
    return send_file(chart_path, mimetype="image/png")


if __name__ == "__main__":
    # Print the actual directory path when starting the server
    print(f"Looking for files in: {OUTPUT_DIR.absolute()}")
    app.run(debug=True)
