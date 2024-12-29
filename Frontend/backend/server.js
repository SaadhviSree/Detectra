const express = require("express");
const path = require("path");
const fs = require("fs");
const cors = require("cors");

const app = express();
const PORT = 3000;

app.use(cors());

// Serve the CSV data
app.get("/api/data", (req, res) => {
  const filePath = path.join(__dirname, "na.csv"); // Updated path
  fs.readFile(filePath, "utf8", (err, data) => {
    if (err) {
      console.error("Error reading CSV file:", err); // Log error
      return res.status(500).json({ error: "Failed to read CSV file" });
    }

    const rows = data.split("\n").filter(row => row.trim() !== "");
    const headers = rows[0].split(",");
    const jsonData = rows.slice(1).map((row) => {
      const values = row.split(",");
      return headers.reduce((acc, header, index) => {
        acc[header] = values[index];
        return acc;
      }, {});
    });

    console.log("Data fetched successfully"); // Log success
    res.json(jsonData);
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
