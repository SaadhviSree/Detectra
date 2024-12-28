import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import re
from datetime import datetime

def prepare_log_data(df):
    """
    Prepare and split the log data columns.
    """
    # Create a copy of the dataframe
    data = df.copy()

    
    # Split the combined columns if needed
    if 'LineIdDateTimeLevelComponentContentEventIdEventTemplate' in data.columns:
        # Split the single column into multiple columns
        split_data = data['LineIdDateTimeLevelComponentContentEventIdEventTemplate'].str.split(n=6, expand=True)
        
        # Assign proper column names
        data = pd.DataFrame({
            'LineId': split_data[0],
            'Date': split_data[1],  # Adjust this if needed (e.g., 'datetime' instead of 'Date')
            'Time': split_data[2],
            'Level': split_data[3],
            'Component': split_data[4],
            'Content': split_data[5],
            'EventId': split_data[6],
            'EventTemplate': split_data[7]
        })

    return data

def preprocess_windows_logs(df):
    """
    Preprocess Windows system log data.
    """
    # First prepare and split the data
    data = prepare_log_data(df)
    

    # Combine 'Date' and 'Time' columns into a single 'DateTime' column
    if 'Date' in data.columns and 'Time' in data.columns:
        data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], errors='coerce')
    else:
        print("Error: 'Date' and/or 'Time' columns not found!")

    # Extract time-based features
    data['hour'] = data['DateTime'].dt.hour
    data['minute'] = data['DateTime'].dt.minute
    data['dayofweek'] = data['DateTime'].dt.dayofweek
    
    # Encode categorical columns
    le_level = LabelEncoder()
    le_component = LabelEncoder()
    le_eventid = LabelEncoder()
    
    data['Level_encoded'] = le_level.fit_transform(data['Level'])
    data['Component_encoded'] = le_component.fit_transform(data['Component'])
    data['EventId_encoded'] = le_eventid.fit_transform(data['EventId'])
    
    # Process EventTemplate field
    data['Template_cleaned'] = data['EventTemplate'].str.replace('<*>', 'PLACEHOLDER')
    data['Template_cleaned'] = data['Template_cleaned'].apply(lambda x: re.sub(r'[^a-zA-Z\s]', '', str(x)))
    
    # Extract template features using TF-IDF
    tfidf = TfidfVectorizer(max_features=50, stop_words='english')
    template_features = tfidf.fit_transform(data['Template_cleaned'])
    
    # Convert to dense array and reduce dimensionality
    pca = PCA(n_components=3)
    template_features_reduced = pca.fit_transform(template_features.toarray())
    
    # Add template features to dataframe
    for i in range(template_features_reduced.shape[1]):
        data[f'template_feature_{i}'] = template_features_reduced[:, i]
    
    # Calculate message length features
    data['content_length'] = data['Content'].str.len()
    data['template_length'] = data['EventTemplate'].str.len()
    data['parameter_count'] = data['EventTemplate'].str.count('<*>')
    
    return data, le_level, le_component, le_eventid

def detect_windows_log_anomalies(df, contamination=0.1):
    """
    Detect anomalies in Windows system log data.
    
    Parameters:
    df: pandas DataFrame with Windows log data
    contamination: expected proportion of outliers in the dataset
    
    Returns:
    DataFrame with anomaly scores and labels, silhouette score
    """
    # Preprocess the data
    processed_data, le_level, le_component, le_eventid = preprocess_windows_logs(df)
    
    # Select features for anomaly detection
    feature_columns = [
        'hour', 'minute', 'dayofweek',
        'Level_encoded', 'Component_encoded', 'EventId_encoded',
        'template_feature_0', 'template_feature_1', 'template_feature_2',
        'content_length', 'template_length', 'parameter_count'
    ]
    
    # Prepare features for modeling
    X = processed_data[feature_columns].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Isolation Forest
    iso_forest = IsolationForest(contamination=contamination, 
                                random_state=42,
                                n_estimators=200)
    iso_forest_labels = iso_forest.fit_predict(X_scaled)
    iso_forest_scores = iso_forest.score_samples(X_scaled)
    
    # DBSCAN
    dbscan = DBSCAN(eps=0.3, min_samples=3)
    dbscan_labels = dbscan.fit_predict(X_scaled)
    
    # Calculate silhouette score for DBSCAN (excluding noise points)
    valid_points = dbscan_labels != -1
    if len(np.unique(dbscan_labels[valid_points])) > 1:
        silhouette_avg = silhouette_score(X_scaled[valid_points], 
                                        dbscan_labels[valid_points])
    else:
        silhouette_avg = 0
    
    # Add results to original dataframe
    results = processed_data.copy()
    results['isolation_forest_label'] = iso_forest_labels
    results['isolation_forest_score'] = iso_forest_scores
    results['dbscan_label'] = dbscan_labels
    
    # Mark anomalies
    results['is_anomaly_isolation'] = results['isolation_forest_label'] == -1
    results['is_anomaly_dbscan'] = results['dbscan_label'] == -1
    
    # Create visualizations
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Temporal Distribution of Anomalies
    plt.subplot(221)
    plt.scatter(processed_data['DateTime'], iso_forest_scores,
                c=iso_forest_labels, cmap='viridis')
    plt.title('Temporal Distribution of Anomalies')
    plt.xlabel('DateTime')
    plt.ylabel('Anomaly Score')
    plt.xticks(rotation=45)
    
    # Plot 2: Component vs EventId Anomalies
    plt.subplot(222)
    plt.scatter(processed_data['Component_encoded'],
                processed_data['EventId_encoded'],
                c=iso_forest_labels, cmap='viridis')
    plt.title('Component vs EventId Anomalies')
    plt.xlabel('Component')
    plt.ylabel('EventId')
    
    # Plot 3: Message Length vs Parameter Count
    plt.subplot(223)
    plt.scatter(processed_data['content_length'],
                processed_data['parameter_count'],
                c=iso_forest_labels, cmap='viridis')
    plt.title('Message Length vs Parameter Count')
    plt.xlabel('Content Length')
    plt.ylabel('Parameter Count')
    
    # Plot 4: Anomaly Score Distribution
    plt.subplot(224)
    plt.hist(iso_forest_scores, bins=50)
    plt.title('Anomaly Score Distribution')
    plt.xlabel('Anomaly Score')
    plt.ylabel('Frequency')
    
    plt.tight_layout()
    
    return results, silhouette_avg, plt

# Example usage:

data = pd.read_csv('/content/Windows_2k.log_structured.csv')

# Run anomaly detection
results, silhouette, plot = detect_windows_log_anomalies(data)

print(f"Silhouette Score: {silhouette:.3f}")
print("\nNumber of anomalies detected:")
print(f"Isolation Forest: {results['is_anomaly_isolation'].sum()}")
print(f"DBSCAN: {results['is_anomaly_dbscan'].sum()}")

# Show visualization
plot.show()

# Get top anomalies
anomalies = results[results['is_anomaly_isolation']].sort_values('isolation_forest_score')
print("\nTop anomalous logs:")
print(anomalies[['DateTime', 'Level', 'Component', 'EventId', 'EventTemplate']].head())
