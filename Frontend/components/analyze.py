import os
import json
import datetime
from collections import defaultdict

class ForensicAnalyzer:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.file_stats = defaultdict(list)
        os.makedirs(output_dir, exist_ok=True)

    def analyze_recovered_files(self, recovery_dir):
        """Analyze files recovered by PhotoRec."""
        print(f"\nAnalyzing files in: {recovery_dir}")
        
        file_count = 0
        # Walk through all recovered files
        for root, _, files in os.walk(recovery_dir):
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    # Get file extension (type)
                    file_type = os.path.splitext(file)[1][1:].upper() or 'UNKNOWN'
                    file_size = os.path.getsize(file_path)
                    
                    self.file_stats[file_type].append({
                        'path': file_path,
                        'size': file_size,
                        'recovery_time': datetime.datetime.fromtimestamp(
                            os.path.getctime(file_path)
                        ).isoformat()
                    })
                    file_count += 1
                    
                    if file_count % 5000 == 0:  # Progress update every 100 files
                        print(f"Processed {file_count} files...")
                        
                except Exception as e:
                    print(f"Error analyzing {file}: {e}")
        
        if file_count == 0:
            print("No files found in the directory!")
        else:
            print(f"Completed analysis of {file_count} files.")

    def generate_report(self, case_id, output_file):
        """Generate analysis report."""
        total_files = sum(len(files) for files in self.file_stats.values())
        
        if total_files == 0:
            print("\nNo files were found for analysis!")
            return
            
        report = {
            'case_id': case_id,
            'analysis_time': datetime.datetime.now().isoformat(),
            'total_files': total_files,
            'file_type_summary': []
        }

        # Generate file type summary
        for file_type, files in sorted(self.file_stats.items()):
            total_size = sum(f['size'] for f in files)
            largest_size = max(f['size'] for f in files) if files else 0
            
            report['file_type_summary'].append({
                'file_type': file_type,
                'file_count': len(files),
                'total_size': total_size,
                'largest_file_size': largest_size,
                'file_list': files  # Include full file details
            })

        # Save report
        try:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=4)
            print(f"\nReport successfully saved to: {output_file}")
        except Exception as e:
            print(f"Error saving report: {e}")

def analyze_files(file_paths, output_file, case_id="default"):
    """Main analysis function."""
    analyzer = ForensicAnalyzer(os.path.dirname(output_file))
    
    # Process all paths in a single analysis
    for path in file_paths:
        if os.path.exists(path):
            analyzer.analyze_recovered_files(path)
        else:
            print(f"Warning: Path does not exist: {path}")
    
    analyzer.generate_report(case_id, output_file)
    return analyzer.file_stats