import sys
import os
import hashlib
import datetime
import sqlite3
from pathlib import Path
import struct
import logging
from threading import Thread
from queue import Queue
import json


try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False
    print("python-magic not installed. File type detection will be limited.")
try:
    import yara
    YARA_AVAILABLE = True
except ImportError:
    YARA_AVAILABLE = False
    print("yara-python not installed. Pattern matching will be disabled.")
try:
    import pyewf
    PYEWF_AVAILABLE = True
except ImportError:
    PYEWF_AVAILABLE = False
    print("pyewf not installed. E01 support disabled.")


class FileSignatures:
    """File signature definitions for file carving."""
    def __init__(self):
        self.signatures = [
            # JPEG Image
            {
                'type': 'JPG',
                'header': bytes([0xFF, 0xD8, 0xFF]),
                'footer': bytes([0xFF, 0xD9]),
                'max_size': 12000000
            },
            # PNG Image
            {
                'type': 'PNG',
                'header': bytes([0x89, 0x50, 0x4E, 0x47]),
                'footer': bytes([0x49, 0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82]),
                'max_size': 10000000
            },
            # PDF Document
            {
                'type': 'PDF',
                'header': bytes([0x25, 0x50, 0x44, 0x46]),
                'footer': bytes([0x0A, 0x25, 0x25, 0x45, 0x4F, 0x46]),
                'max_size': 20000000
            },
            # Microsoft Word Document
            {
                'type': 'DOC',
                'header': bytes([0xD0, 0xCF, 0x11, 0xE0]),
                'footer': None,
                'max_size': 10000000
            },
            # ZIP Archive
            {
                'type': 'ZIP',
                'header': bytes([0x50, 0x4B, 0x03, 0x04]),
                'footer': bytes([0x50, 0x4B, 0x05, 0x06]),  # or use 0x50 0x4B 0x07 0x08 for directories
                'max_size': 50000000
            },
            # RAR Archive
            {
                'type': 'RAR',
                'header': bytes([0x52, 0x61, 0x72, 0x21, 0x1A, 0x07]),
                'footer': bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
                'max_size': 50000000
            },
            # Microsoft Excel (XLS)
            {
                'type': 'XLS',
                'header': bytes([0xD0, 0xCF, 0x11, 0xE0, 0xA1, 0xB1, 0x1A, 0xE1]),
                'footer': None,
                'max_size': 10000000
            },
            # Microsoft Excel (XLSX)
            {
                'type': 'XLSX',
                'header': bytes([0x50, 0x4B, 0x03, 0x04]),
                'footer': bytes([0x50, 0x4B, 0x05, 0x06]),
                'max_size': 50000000
            },
            # Microsoft PowerPoint (PPT)
            {
                'type': 'PPT',
                'header': bytes([0xD0, 0xCF, 0x11, 0xE0, 0xA1, 0xB1, 0x1A, 0xE1]),
                'footer': None,
                'max_size': 10000000
            },
            # Microsoft PowerPoint (PPTX)
            {
                'type': 'PPTX',
                'header': bytes([0x50, 0x4B, 0x03, 0x04]),
                'footer': bytes([0x50, 0x4B, 0x05, 0x06]),
                'max_size': 50000000
            },
            # WordPerfect
            {
                'type': 'WP',
                'header': bytes([0xD0, 0x73, 0x68, 0x6E]),
                'footer': None,
                'max_size': 10000000
            },
            # Text file (TXT)
            {
                'type': 'TXT',
                'header': bytes([0xEF, 0xBB, 0xBF]),  # UTF-8 BOM for text files
                'footer': None,
                'max_size': 5000000
            }
        ]

    def get_signatures(self):
        return self.signatures


class DiskReader:
    def __init__(self, filename, disk_to_read=500000000):
        self.filename = filename
        self.disk_to_read = disk_to_read
        self.handle = None
        self.file_type = self._detect_file_type()
        
    def _detect_file_type(self):
        ext = os.path.splitext(self.filename)[1].lower()
        if ext == '.e01' and PYEWF_AVAILABLE:
            return 'E01'
        return 'RAW'
    
    def open(self):
        try:
            if self.file_type == 'E01' and PYEWF_AVAILABLE:
                filenames = pyewf.glob(self.filename)
                self.handle = pyewf.handle()
                self.handle.open(filenames)
            else:
                self.handle = open(self.filename, 'rb')
            return True
        except Exception as e:
            print(f"Error opening file: {str(e)}")
            return False
    
    def read(self, size):
        try:
            return self.handle.read(size)
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            return None
    
    def close(self):
        if self.handle:
            self.handle.close()

class ForensicAnalyzer:
    def __init__(self, evidence_path, case_id, output_path):
        self.evidence_path = evidence_path
        self.case_id = case_id
        self.output_path = output_path
        os.makedirs(self.output_path, exist_ok=True)
        self.file_signatures = FileSignatures().get_signatures()
        self.db_path = f"case_{self.case_id}.db"
        self.disk_reader = DiskReader(self.evidence_path)  # Use DiskReader for file access
        self.initialize_database()  # Initialize the SQLite database

    def initialize_database(self):
        """Initialize SQLite database for storing forensic artifacts."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.executescript('''
            CREATE TABLE IF NOT EXISTS carved_files (
                id INTEGER PRIMARY KEY,
                file_type TEXT,
                offset INTEGER,
                size INTEGER,
                md5 TEXT,
                recovery_time TEXT
            );
        ''')
        conn.commit()
        conn.close()

    def analyze_disk(self):
        """Analyze the entire disk or file."""
        if not self.disk_reader.open():
            print("Failed to open the evidence file.")
            return

        try:
            mbr = self.disk_reader.read(512)  # Read the Master Boot Record (MBR)
            if not mbr:
                print("Failed to read MBR.")
                return

            partitions = self.parse_partitions(mbr)
            for part_num, partition in partitions.items():
                print(f"Analyzing partition {part_num}: {partition}")
                self.analyze_partition(partition)
        except Exception as e:
            print(f"Error analyzing disk: {e}")
        finally:
            self.disk_reader.close()

    def parse_partitions(self, mbr):
        """Parse MBR to extract partition entries."""
        partitions = {}
        for i in range(4):  # Four partition entries in the MBR
            offset = 446 + i * 16
            partitions[i + 1] = mbr[offset:offset + 16]
        return partitions

    def analyze_partition(self, partition):
        """Analyze a specific partition."""
        start_sector = self.get_sector(partition)
        part_size = self.get_part_size(partition)
        part_type = self.get_part_type(partition)

        if part_type == "Empty" or part_size == 0:
            print(f"Partition is empty or size is zero.")
            return

        print(f"Partition: Type={part_type}, Start Sector={start_sector}, Size={part_size}")
        self.carve_files_from_partition(start_sector, part_size)

    def get_sector(self, partition):
        """Get the starting sector of the partition."""
        sector_data = partition[8:12]
        return int.from_bytes(sector_data, byteorder='little')

    def get_part_size(self, partition):
        """Get the size of the partition in sectors."""
        size_data = partition[12:16]
        return int.from_bytes(size_data, byteorder='little')

    def get_part_type(self, partition):
        """Get the partition type."""
        part_type_code = partition[4]
        partition_types = {
            0x00: "Empty",
            0x07: "NTFS",
            0x0B: "FAT32",
            0x0C: "FAT32 LBA",
            0x83: "Linux"
        }
        return partition_types.get(part_type_code, f"Unknown ({hex(part_type_code)})")

    def carve_files_from_partition(self, start_sector, size):
        """Carve files from a partition."""
        chunk_size = 1024 * 1024  # 1 MB
        offset = start_sector * 512
        remaining = size * 512

        while remaining > 0:
            read_size = min(chunk_size, remaining)
            chunk = self.disk_reader.read(read_size)
            if not chunk:
                print("No more data to read.")
                break

            self.carve_files_from_chunk(chunk, offset)
            offset += read_size
            remaining -= read_size

    def carve_files_from_chunk(self, chunk, offset):
        """Find and carve files in a chunk."""
        for sig in self.file_signatures:
            pos = 0
            while True:
                pos = chunk.find(sig['header'], pos)
                if pos == -1:
                    break

                try:
                    file_data = self.extract_file(chunk[pos:], sig)
                    if file_data:
                        md5 = hashlib.md5(file_data).hexdigest()
                        file_path = os.path.join(self.output_path, f"{md5}.{sig['type'].lower()}")

                        with open(file_path, 'wb') as carved_file:
                            carved_file.write(file_data)

                        # Insert into database
                        conn = sqlite3.connect(self.db_path)
                        c = conn.cursor()
                        c.execute('''
                            INSERT INTO carved_files (file_type, offset, size, md5, recovery_time)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (sig['type'], offset + pos, len(file_data), md5, datetime.datetime.now().isoformat()))
                        conn.commit()
                        conn.close()

                        print(f"Carved {sig['type']} file: {file_path}")
                except Exception as e:
                    print(f"Error carving file at offset {offset + pos}: {e}")
                pos += 1

    def extract_file(self, data, signature):
        """Extract a file from the given data using its signature."""
        if signature['footer']:
            end = data.find(signature['footer'])
            if end == -1 or (end - len(signature['header'])) > signature['max_size']:
                return None
            return data[:end + len(signature['footer'])]
        else:
            # Carve file using header and max_size only
            return data[:signature['max_size']]


    def generate_report(self):
        """Generate a detailed JSON report."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Fetch all carved files
        carved_files = c.execute('SELECT * FROM carved_files').fetchall()

        # Aggregate data by file type
        file_type_summary = c.execute('''
            SELECT file_type, 
                COUNT(*) AS file_count, 
                SUM(size) AS total_size, 
                MAX(size) AS largest_file_size
            FROM carved_files
            GROUP BY file_type
        ''').fetchall()

        # Get earliest and latest recovery times
        recovery_times = c.execute('''
            SELECT MIN(recovery_time), MAX(recovery_time) FROM carved_files
        ''').fetchone()

        conn.close()

        # Format report
        report = {
            'case_id': self.case_id,
            'evidence_file': self.evidence_path,
            'analysis_time': datetime.datetime.now().isoformat(),
            'total_files': len(carved_files),
            'file_type_summary': [
                {
                    'file_type': row[0],
                    'file_count': row[1],
                    'total_size': row[2],
                    'largest_file_size': row[3]
                }
                for row in file_type_summary
            ],
            'earliest_recovery_time': recovery_times[0],
            'latest_recovery_time': recovery_times[1],
            'carved_files': carved_files
        }

        # Save report to JSON file
        report_file = os.path.join(self.output_path, f"case_{self.case_id}_report.json")
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=4)

        print(f"Report generated: {report_file}")
        print("\nSummary:")
        for row in file_type_summary:
            print(f"- {row[0]}: {row[1]} files, Total Size: {row[2]} bytes, Largest File: {row[3]} bytes")



def main():
    case_id = input("Enter case ID: ").strip()
    evidence_path = input("Enter evidence file path: ").strip()
    output_path = input("Enter output directory path: ").strip()

    analyzer = ForensicAnalyzer(evidence_path, case_id, output_path)

    print("1 - Analyze Disk")
    print("2 - Generate Report")
    print("3 - Exit")

    while True:
        choice = input("Select an option: ").strip()
        if choice == "1":
            print("Analyzing disk...")
            analyzer.analyze_disk()
            print("Analysis completed.")
        elif choice == "2":
            print("Generating report...")
            analyzer.generate_report()
        elif choice == "3":
            print("Exiting.")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
