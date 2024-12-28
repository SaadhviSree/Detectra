import os
import platform
import psutil
import datetime
import socket
import subprocess
import json
import logging
from pathlib import Path

# Additional Imports for hash checking
import hashlib
import requests

# Known malicious process names, command line patterns, and suspicious file paths
MALICIOUS_PROCESSES = ['malware.exe', 'evilprocess', 'cmd.exe', 'powershell.exe']
SUSPICIOUS_FILE_PATHS = ['/temp/', '/user/', '/appdata/']
MALICIOUS_IPS = ['192.168.1.100', '10.0.0.2']  # Replace with actual known malicious IPs
KNOWN_MALWARE_HASHES = ['5d41402abc4b2a76b9719d911017c592', 'e99a18c428cb38d5f260853678922e03']

class LiveForensics:
    def __init__(self, output_dir="forensics_output"):
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path(output_dir) / self.timestamp
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            filename=self.output_dir / "forensics.log",
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def collect_system_info(self):
        """Collect basic system information"""
        try:
            system_info = {
                "hostname": socket.gethostname(),
                "os": platform.system(),
                "os_release": platform.release(),
                "architecture": platform.machine(),
                "processor": platform.processor(),
                "boot_time": datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self._write_json("system_info.json", system_info)
            self.logger.info("System information collected successfully")
            return system_info
        except Exception as e:
            self.logger.error(f"Error collecting system info: {str(e)}")
            return None

    def collect_running_processes(self):
        """Collect information about running processes and detect malicious ones"""
        try:
            processes = []
            suspicious_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline', 'create_time']):
                try:
                    pinfo = proc.info
                    pinfo['create_time'] = datetime.datetime.fromtimestamp(pinfo['create_time']).strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Check for known malicious processes or suspicious command lines
                    if any(
                        pinfo['name'].lower() == malware or 
                        (pinfo['cmdline'] and any(malware in ' '.join(pinfo['cmdline']).lower() for malware in MALICIOUS_PROCESSES))
                        for malware in MALICIOUS_PROCESSES
                    ):
                        suspicious_processes.append(pinfo)
                    
                    processes.append(pinfo)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            self._write_json("running_processes.json", processes)
            self.logger.info(f"Collected information for {len(processes)} running processes")
            if suspicious_processes:
                self._write_json("suspicious_processes.json", suspicious_processes)
                self.logger.warning(f"Suspicious processes detected: {len(suspicious_processes)}")
            return processes
        except Exception as e:
            self.logger.error(f"Error collecting process info: {str(e)}")
            return None


    def collect_network_connections(self):
        """Collect active network connections and check for malicious IPs"""
        try:
            connections = []
            suspicious_connections = []
            for conn in psutil.net_connections(kind='inet'):
                connection_info = {
                    "local_address": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "",
                    "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "",
                    "status": conn.status,
                    "pid": conn.pid
                }
                
                # Check if the remote address is a known malicious IP
                if conn.raddr and conn.raddr.ip in MALICIOUS_IPS:
                    suspicious_connections.append(connection_info)
                
                connections.append(connection_info)
            
            self._write_json("network_connections.json", connections)
            self.logger.info(f"Collected {len(connections)} network connections")
            if suspicious_connections:
                self._write_json("suspicious_connections.json", suspicious_connections)
                self.logger.warning(f"Suspicious network connections detected: {len(suspicious_connections)}")
            return connections
        except Exception as e:
            self.logger.error(f"Error collecting network connections: {str(e)}")
            return None

    def collect_memory_info(self):
        """Collect system memory information"""
        try:
            memory_info = {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "percent": psutil.virtual_memory().percent,
                "used": psutil.virtual_memory().used,
                "swap": {
                    "total": psutil.swap_memory().total,
                    "used": psutil.swap_memory().used,
                    "free": psutil.swap_memory().free,
                    "percent": psutil.swap_memory().percent
                }
            }
            
            self._write_json("memory_info.json", memory_info)
            self.logger.info("Memory information collected successfully")
            return memory_info
        except Exception as e:
            self.logger.error(f"Error collecting memory info: {str(e)}")
            return None

    def scan_files_for_malware(self, path="/"):
        """Scan files in a given directory for known malware signatures and suspicious files"""
        suspicious_files = []
        for root, dirs, files in os.walk(path):
            for file in files:
                # Check file path and name for suspicious patterns
                file_path = os.path.join(root, file)
                if any(susp_path in file_path.lower() for susp_path in SUSPICIOUS_FILE_PATHS):
                    suspicious_files.append(file_path)
                    self.logger.warning(f"Suspicious file detected: {file_path}")

                # Check file hash against known malware hashes
                try:
                    file_hash = self.calculate_file_hash(file_path)
                    if file_hash in KNOWN_MALWARE_HASHES:
                        suspicious_files.append(file_path)
                        self.logger.warning(f"Malicious file detected: {file_path}")
                except Exception as e:
                    self.logger.error(f"Error checking file hash for {file_path}: {str(e)}")
        
        if suspicious_files:
            self._write_json("suspicious_files.json", suspicious_files)
            self.logger.warning(f"Suspicious files found: {len(suspicious_files)}")
        return suspicious_files

    def calculate_file_hash(self, file_path):
        """Calculate SHA-1 hash of a file"""
        sha1 = hashlib.sha1()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha1.update(chunk)
        return sha1.hexdigest()

    def _write_json(self, filename, data):
        """Helper method to write data to JSON file"""
        try:
            with open(self.output_dir / filename, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            self.logger.error(f"Error writing to {filename}: {str(e)}")

def main():
    # Create forensics instance
    forensics = LiveForensics()
    
    # Collect all information
    forensics.collect_system_info()
    forensics.collect_running_processes()
    forensics.collect_network_connections()
    forensics.collect_memory_info()
    
    # Scan for suspicious files (can be limited to certain directories)
    forensics.scan_files_for_malware(r"C:\Users\kavin_1xozkcy\OneDrive\BTech-CSECS\Semesters")
    
    print(f"Forensic data collection completed. Check the output directory: {forensics.output_dir}")

if __name__ == "__main__":
    main()
