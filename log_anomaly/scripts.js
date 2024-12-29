document.getElementById('upload-button').addEventListener('click', () => {
  const fileInput = document.getElementById('log-upload');
  const file = fileInput.files[0];

  if (!file) {
    alert('Please select a CSV file to upload.');
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  fetch('/upload', {
    method: 'POST',
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error('Failed to process the file.');
      }
      return response.json();
    })
    .then((data) => {
      const resultsDiv = document.getElementById('results');
      resultsDiv.innerHTML = `
        <h3>Silhouette Score: ${data.silhouette_score}</h3>
        <h3>Top Anomalies</h3>
        <table>
          <thead>
            <tr>
              <th>DateTime</th>
              <th>Level</th>
              <th>Component</th>
              <th>Event ID</th>
              <th>Event Template</th>
            </tr>
          </thead>
          <tbody>
            ${data.top_anomalies
              .map(
                (anomaly) => `
              <tr>
                <td>${anomaly.DateTime}</td>
                <td>${anomaly.Level}</td>
                <td>${anomaly.Component}</td>
                <td>${anomaly.EventId}</td>
                <td>${anomaly.EventTemplate}</td>
              </tr>`
              )
              .join('')}
          </tbody>
        </table>
        <h3>Visualization</h3>
        <img src="data:image/png;base64,${data.plot}" alt="Anomaly Plot">
      `;
    })
    .catch((error) => {
      console.error('Error:', error);
      alert('An error occurred while processing the file.');
    });
});
