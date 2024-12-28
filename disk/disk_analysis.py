import sys
import os

try:
    import pyewf
    PYEWF_AVAILABLE = True
except ImportError:
    PYEWF_AVAILABLE = False
    print("pyewf not installed. E01 support disabled.")

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

class PartitionAnalyzer:
    def __init__(self):
        self.part_codes = {
            0x00: "Empty",
            0x01: "12-bit FAT",
            0x04: "16-bit FAT",
            0x05: "Extended MS-DOS",
            0x06: "FAT-16",
            0x07: "NTFS",
            0x0B: "FAT-32 (CHS)",
            0x0C: "FAT-32 (LBA)",
            0x0E: "FAT-16 (LBA)"
        }
    
    def get_sector(self, part):
        try:
            big_endian = part[8:12]
            big_endian.reverse()
            hexed = ''.join(format(x, '02x') for x in big_endian)
            return int(hexed, 16)
        except Exception:
            return 0
    
    def get_part_size(self, part):
        try:
            big_endian = part[12:16]
            big_endian.reverse()
            hexed = ''.join(format(x, '02x') for x in big_endian)
            return int(hexed, 16)
        except Exception:
            return 0
    
    def get_part_code(self, part):
        try:
            code = part[4]
            return self.part_codes.get(code, f"Unknown ({hex(code)})")
        except Exception:
            return "Invalid"
    
    def print_info(self, part):
        print(f"Start Sector: {self.get_sector(part)}")
        print(f"Partition Size: {self.get_part_size(part)}")
        print(f"Partition Type: {self.get_part_code(part)}\n")

    def get_ntfs_information(self, part, disk_data):
        try:
            start_sector = self.get_sector(part)
            volume = start_sector * 512
            
            if volume + 512 >= len(disk_data):
                print("Insufficient disk data read")
                return None
            
            bytes_per_sector = int.from_bytes(disk_data[volume+11:volume+13], 'little')
            sectors_per_cluster = disk_data[volume+13]
            mft_start_cluster = int.from_bytes(disk_data[volume+48:volume+56], 'little')
            
            print(f"NTFS Information:")
            print(f"Bytes per sector: {bytes_per_sector}")
            print(f"Sectors per cluster: {sectors_per_cluster}")
            print(f"MFT start cluster: {mft_start_cluster}")
            
            return start_sector
            
        except Exception as e:
            print(f"Error reading NTFS information: {str(e)}")
            return None

    def get_fat_information(self, part, disk_data):
        try:
            part_type = self.get_part_code(part)
            if part_type == "Empty":
                print("Partition is empty")
                return None
                
            if "NTFS" in part_type:
                return self.get_ntfs_information(part, disk_data)
                
            volume = self.get_sector(part) * 512 - 512
            if volume <= 0:
                print("Invalid partition offset")
                return None
                
            if volume + 24 >= len(disk_data):
                print("Insufficient disk data read")
                return None
            
            reserved_area = disk_data[volume + 14:volume + 16]
            reserved_area.reverse()
            reserved_area = int(''.join(format(x, '02x') for x in reserved_area), 16)
            
            fat_area = disk_data[volume + 22:volume + 24]
            fat_area.reverse()
            fat_area = int(''.join(format(x, '02x') for x in fat_area), 16)
            
            fat_copies = disk_data[volume + 16]
            per_cluster = disk_data[volume + 13]
            
            print(f"FAT Information:")
            print(f"Reserved Area: {reserved_area}")
            print(f"FAT Area: {fat_area}")
            print(f"FAT Copies: {fat_copies}")
            print(f"Sectors Per Cluster: {per_cluster}")
            
            data_area = self.get_sector(part) + reserved_area + fat_area * fat_copies
            print(f"Data Area: {data_area}")
            
            return data_area
            
        except Exception as e:
            print(f"Error reading filesystem information: {str(e)}")
            return None

    def directory_scan(self, data_area, disk_data):
        try:
            if not data_area:
                return
                
            directory_size = 32
            start = (data_area * 512) - 512
            
            if start >= len(disk_data):
                print("Insufficient disk data for directory scan")
                return
                
            directory = [disk_data[start]]
            overflow = 0
            
            while directory[0] != 0 and overflow < 50:
                if start + directory_size >= len(disk_data):
                    print("Reached end of disk data")
                    break
                    
                overflow += 1
                directory = disk_data[start:start + directory_size]
                directory_name = directory[0:11]
                
                try:
                    name = ''.join(chr(x) for x in directory_name if 32 <= x <= 126)
                    if name.strip():
                        print(f"Name: {name}")
                except:
                    continue
                
                if directory[0] == 229:  # Deleted file
                    try:
                        print("   Deleted File Information")
                        deleted_info = directory[26:28]
                        deleted_info.reverse()
                        deleted_info = int(''.join(format(x, '02x') for x in deleted_info), 16)
                        print(f"   Starting Cluster: {deleted_info}")
                        deleted_info = (deleted_info - 2) * 8 + 599
                        print(f"   Starting Sector: {deleted_info}")
                        
                        deleted_size = directory[28:32]
                        deleted_size.reverse()
                        deleted_size = int(''.join(format(x, '02x') for x in deleted_size), 16)
                        print(f"   Size of file: {deleted_size} bytes")
                        
                        if deleted_info * 512 - 496 < len(disk_data):
                            first_chars = disk_data[deleted_info * 512 - 512:deleted_info * 512 - 496]
                            print(f"   First 16 Characters: {''.join(chr(x) for x in first_chars if 32 <= x <= 126)}\n")
                    except:
                        print("   Error reading deleted file information")
                
                start += directory_size
                
        except Exception as e:
            print(f"Error scanning directory: {str(e)}")

def main():
    if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        file = r"C:\Users\kavin_1xozkcy\Projects\detectra\data\charlie-2009-11-12.E01"
    
    disk_reader = DiskReader(file)
    analyzer = PartitionAnalyzer()
    
    if not disk_reader.open():
        sys.exit(1)
    
    mbr = list(disk_reader.read(512))
    if not mbr:
        print("Error reading MBR")
        disk_reader.close()
        sys.exit(1)
    
    partitions = {
        1: mbr[446:462],
        2: mbr[462:478],
        3: mbr[478:494],
        4: mbr[494:510]
    }
    
    more_disk = list(disk_reader.read(disk_reader.disk_to_read))
    disk_reader.close()
    
    options = {
        1: "List Partitions",
        2: "Show Partitions Information",
        3: "Exit"
    }
    
    for x in options:
        print(f"{x} - {options[x]}")
    
    while True:
        try:
            choice = input("Choose the option 1-3: ")
            
            if choice == "1":
                for p in partitions:
                    print(f"\nPartition {p}")
                    analyzer.print_info(partitions[p])
            
            elif choice == "2":
                print("Choose the partition 1-4:")
                for p in partitions:
                    print(f"Partition {p}")
                
                part_select = int(input("Choose the partition 1-4: "))
                if part_select in partitions:
                    data_area = analyzer.get_fat_information(partitions[part_select], more_disk)
                    analyzer.directory_scan(data_area, more_disk)
                else:
                    print("Invalid partition selection")
            
            elif choice == "3":
                break
            
            else:
                print("Please select a valid option")
                
        except Exception as e:
            print(f"Error: {str(e)}")
            continue

if __name__ == "__main__":
    main()
