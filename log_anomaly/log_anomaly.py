import pandas as pd
import numpy as np
import json
import re
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.svm import OneClassSVM
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from typing import List, Dict, Tuple


class PackageLogAnalyzer:
    def __init__(self):
        self.log_data = pd.DataFrame()
        self.processing_data = pd.DataFrame()

    def parse_json_logs(self, json_file: str, ground_truth_file: str = None) -> pd.DataFrame:
        """Parse JSON log file and extract package processing information."""
        with open(json_file, 'r') as f:
            logs = json.load(f)

        parsed_data = []
        pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\s*\] Processed (\d+) out of (\d+) packages"

        for log in logs:
            match = re.match(pattern, log['message'])
            if match:
                timestamp, level, processed, total = match.groups()
                parsed_data.append({
                    'timestamp': timestamp,
                    'level': level,
                    'processed_packages': int(processed),
                    'total_packages': int(total),
                    'completion_percentage': (int(processed) / int(total)) * 100
                })

        self.log_data = pd.DataFrame(parsed_data)
        self.log_data['timestamp'] = pd.to_datetime(self.log_data['timestamp'])
        return self.log_data

    def analyze_processing_patterns(self) -> Dict:
        """Analyze package processing patterns and metrics."""
        analysis = {}

        # Processing speed with better handling of time differences
        self.log_data['time_diff'] = self.log_data['timestamp'].diff().dt.total_seconds()
        self.log_data['packages_diff'] = self.log_data['processed_packages'].diff()

        # Handle division by zero and very small time differences
        mask = self.log_data['time_diff'] > 0.001  # Avoid extremely small time differences
        self.log_data['processing_speed'] = np.where(
            mask,
            self.log_data['packages_diff'] / self.log_data['time_diff'],
            0
        )

        # Calculate metrics using cleaned data
        valid_speeds = self.log_data['processing_speed'][mask]
        analysis['average_speed'] = valid_speeds.mean() if len(valid_speeds) > 0 else 0
        analysis['max_speed'] = valid_speeds.max() if len(valid_speeds) > 0 else 0
        analysis['min_speed'] = valid_speeds.min() if len(valid_speeds) > 0 else 0
        analysis['total_duration'] = (self.log_data['timestamp'].max() - 
                                      self.log_data['timestamp'].min()).total_seconds()
        analysis['completion_percentage'] = self.log_data['completion_percentage'].iloc[-1]

        return analysis

    def detect_anomalies(self, contamination_rate: float = 0.05, use_dbscan: bool = False) -> Tuple[pd.DataFrame, List[int]]:
        """Detect anomalies in processing speed using One-Class SVM or DBSCAN."""
        speed_data = self.log_data[['timestamp', 'processing_speed']].copy()
        speed_data = speed_data[speed_data['processing_speed'].notna() & (speed_data['processing_speed'] != 0)]

        if len(speed_data) < 2:
            return speed_data, []

        # Normalize processing speed data for anomaly detection
        scaler = MinMaxScaler()
        X = scaler.fit_transform(speed_data[['processing_speed']].values.reshape(-1, 1))

        if use_dbscan:
            # DBSCAN for anomaly detection
            dbscan = DBSCAN(eps=0.5, min_samples=10)
            labels = dbscan.fit_predict(X)
            anomalies = labels == -1  # -1 indicates anomalies in DBSCAN
        else:
            # Use One-Class SVM for anomaly detection
            ocsvm = OneClassSVM(kernel='rbf', gamma='auto', nu=contamination_rate)
            ocsvm.fit(X)

            # Predict anomalies
            anomalies = ocsvm.predict(X)
            anomalies = anomalies == -1  # -1 indicates anomalies in One-Class SVM

        # Mark anomalies in the dataframe
        speed_data['is_anomaly'] = anomalies

        # Compute silhouette score
        # 0 for normal points and 1 for anomalies
        labels = np.where(anomalies, 1, 0)

        # Compute silhouette score if there are more than 1 unique label
        if len(np.unique(labels)) > 1:
            silhouette_avg = silhouette_score(X, labels)
            print(f"Silhouette Score: {silhouette_avg:.2f}")
        else:
            silhouette_avg = None
            print("Silhouette Score is not defined due to only one class being detected.")

        return speed_data, np.where(anomalies)[0]

    def visualize_results(self):
        """Create visualizations for package processing analysis."""
        plt.style.use('default')
        fig = plt.figure(figsize=(15, 10))

        # 1. Processing Progress Over Time
        plt.subplot(2, 2, 1)
        plt.plot(self.log_data['timestamp'], self.log_data['completion_percentage'], 'b-', linewidth=2)
        plt.title('Package Processing Progress', pad=20)
        plt.xlabel('Time')
        plt.ylabel('Completion Percentage')
        plt.grid(True, linestyle='--', alpha=0.7)

        # 2. Processing Speed Over Time with Anomalies
        speed_data, _ = self.detect_anomalies()
        plt.subplot(2, 2, 2)
        if not speed_data.empty:
            plt.plot(speed_data['timestamp'], speed_data['processing_speed'], 'g-', linewidth=2, label='Processing Speed')

            # Highlight anomalies
            anomalies = speed_data[speed_data['is_anomaly']]
            if not anomalies.empty:
                plt.scatter(anomalies['timestamp'], anomalies['processing_speed'], color='red', label='Anomalies', s=100)

        plt.title('Processing Speed with Anomalies', pad=20)
        plt.xlabel('Time')
        plt.ylabel('Packages/Second')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()

        # 3. Processing Speed Distribution
        plt.subplot(2, 2, 3)
        valid_speeds = self.log_data['processing_speed'][self.log_data['processing_speed'].notna() &
                                                         (self.log_data['processing_speed'] != 0)]
        if not valid_speeds.empty:
            plt.hist(valid_speeds, bins=30, color='skyblue', edgecolor='black')
            plt.axvline(valid_speeds.mean(), color='red', linestyle='--', label=f'Mean: {valid_speeds.mean():.2f}')
        plt.title('Processing Speed Distribution', pad=20)
        plt.xlabel('Packages/Second')
        plt.ylabel('Frequency')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()

        # 4. Cumulative Packages Processed
        plt.subplot(2, 2, 4)
        plt.plot(self.log_data['timestamp'], self.log_data['processed_packages'], 'b-', linewidth=2)
        plt.title('Cumulative Packages Processed', pad=20)
        plt.xlabel('Time')
        plt.ylabel('Packages Processed')
        plt.grid(True, linestyle='--', alpha=0.7)

        plt.tight_layout(pad=3.0)
        return fig

    def generate_report(self, analysis_results: Dict) -> str:
        """Generate a detailed analysis report."""
        report = []
        report.append("=== Package Processing Analysis Report ===\n")

        # Processing Overview
        report.append("Processing Overview:")
        report.append(f"Total Duration: {analysis_results['total_duration']:.2f} seconds")
        report.append(f"Final Completion: {analysis_results['completion_percentage']:.2f}%")

        # Processing Speed Metrics
        report.append("\nProcessing Speed Metrics:")
        report.append(f"Average Speed: {analysis_results['average_speed']:.2f} packages/second")
        report.append(f"Maximum Speed: {analysis_results['max_speed']:.2f} packages/second")
        report.append(f"Minimum Speed: {analysis_results['min_speed']:.2f} packages/second")

        # Anomaly Detection
        speed_data, _ = self.detect_anomalies()
        anomaly_count = len(speed_data[speed_data['is_anomaly']]) if 'is_anomaly' in speed_data.columns else 0
        report.append(f"\nAnomalies Detected: {anomaly_count}")

        if anomaly_count > 0:
            report.append("\nAnomaly Details:")
            anomalies = speed_data[speed_data['is_anomaly']]
            for _, row in anomalies.iterrows():
                report.append(f"Time: {row['timestamp']}, Speed: {row['processing_speed']:.2f} packages/second")

        return "\n".join(report)

# Example usage
log_analyzer = PackageLogAnalyzer()
log_analyzer.parse_json_logs('/content/log_anomaly_detector-10000-events.json')  # Replace with your log file path
analysis_results = log_analyzer.analyze_processing_patterns()
report = log_analyzer.generate_report(analysis_results)

# Print the report
print(report)

# Optionally, visualize the results
log_analyzer.visualize_results()
