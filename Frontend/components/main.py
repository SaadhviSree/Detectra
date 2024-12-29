
import argparse
from mount_disc import DiskImageManager
from paths import get_path
from analyze import analyze_files
import os
import datetime

def main():
    parser = argparse.ArgumentParser(description="Mount a disk image and process its partitions or process a directory of files.")
    parser.add_argument('path', type=str, help="Path to the disk image file or directory")
    parser.add_argument('--case-id', type=str, default=None, help="Case ID for the analysis")
    
    args = parser.parse_args()
    
    # Generate a case ID if none provided
    case_id = args.case_id or f"case_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Create base output directory
    base_output_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'outputs'
    )
    
    # Create analysis output directory
    analysis_output_dir = os.path.join(base_output_dir, 'analysis')
    os.makedirs(analysis_output_dir, exist_ok=True)
    
    output_file = os.path.join(analysis_output_dir, f"{case_id}_report.json")
    
    if os.path.isdir(args.path):
        print(f"Processing directory: {args.path}")
        paths = [args.path]
        print("Starting file analysis...")
        analyze_files(paths, output_file, case_id)
    else:
        print(f"Processing disk image: {args.path}")
        disk = DiskImageManager(str(args.path), base_output_dir=base_output_dir)
        paths = disk.mount_points
        
        try:
            if paths:
                print("Starting file analysis...")
                analyze_files(paths, output_file, case_id)
            else:
                print("No valid paths found for analysis!")
                return
        finally:
            disk.cleanup()
            
    if os.path.exists(output_file):
        print(f"\nAnalysis complete. Results saved to: {output_file}")
    else:
        print("\nError: Analysis failed to generate output file!")

if __name__ == '__main__':
    main()