import json

# Replace with your actual JSON file path
json_path = "case_case_20241228_082959_report.json"



with open(json_path, 'r') as f:
    data = json.load(f)

# Print key statistics
print(f"Case ID: {data['case_id']}")
print(f"Total Files Analyzed: {data['total_files']}")
print("\nTop 5 file types by count:")
sorted_types = sorted(data['file_type_summary'], key=lambda x: x['file_count'], reverse=True)[:5]
for file_type in sorted_types:
    print(f"- {file_type['file_type']}: {file_type['file_count']} files")
    print(f"  Total Size: {file_type['total_size']:,} bytes")