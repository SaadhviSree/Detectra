
import os
import subprocess
import time
import shutil

class DiskImageManager:
    def __init__(self, image_path, base_output_dir=None):
        self.image_path = image_path
        self.mount_point = "/mnt/EnCasefile"
        self.loop_device = "/dev/loop0"
        
        # Set up custom output directory
        if base_output_dir is None:
            base_output_dir = os.path.join(
                os.getcwd(), 
                'outputs'
            )
        
        self.mount_base = os.path.join(base_output_dir, 'disk_mount')
        self.recovery_dir = os.path.join(base_output_dir, 'recovered')
        self.mount_points = []
        self.ewf_mount = None
        
        # Create all necessary directories
        os.makedirs(self.mount_base, exist_ok=True)
        os.makedirs(self.recovery_dir, exist_ok=True)
        os.makedirs(self.mount_point, exist_ok=True)
        
        print(f"Output directories initialized:")
        print(f"- Mount base: {self.mount_base}")
        print(f"- Recovery directory: {self.recovery_dir}")
        print(f"- Mount point: {self.mount_point}")
        
        self.process_image()

    def check_and_unmount(self):
        """Check if mount point is occupied and unmount if necessary."""
        try:
            # Check if mount point is occupied
            result = subprocess.run(
                ["mountpoint", "-q", self.mount_point],
                check=False
            )
            if result.returncode == 0:
                print(f"Unmounting {self.mount_point}...")
                subprocess.run(["sudo", "umount", self.mount_point], check=True)
                
            # Detach loop device if it exists
            if os.path.exists(self.loop_device):
                print(f"Detaching loop device {self.loop_device}...")
                subprocess.run(["sudo", "losetup", "-d", self.loop_device], check=True)
                
        except Exception as e:
            print(f"Error during unmounting: {e}")
            raise

    def process_image(self):
        """Process the disk image based on its type."""
        if self.image_path.lower().endswith('.e01'):
            self.check_and_unmount()  # Clean up existing mounts first
            self._mount_ewf()
            self._setup_loop_device()
            self._run_photorec()
        else:
            print("Unsupported image format. Please provide an E01 image.")
            
    def _mount_ewf(self):
        """Mount E01 image using ewfmount."""
        try:
            print(f"Mounting {self.image_path} at {self.mount_point}...")
            subprocess.run([
                "sudo", "ewfmount",
                self.image_path,
                self.mount_point
            ], check=True)
            
            print(f"Successfully mounted E01 image at {self.mount_point}")
            self.mount_points = [self.recovery_dir]
            
            # Wait a moment for the mount to complete
            time.sleep(2)
            
        except subprocess.CalledProcessError as e:
            print(f"Error mounting E01 image: {e}")
            raise

    def _setup_loop_device(self):
        """Set up the loop device for the mounted E01 file."""
        try:
            ewf_file = os.path.join(self.mount_point, "ewf1")
            print(f"Setting up loop device {self.loop_device} for {ewf_file}...")
            subprocess.run([
                "sudo", "losetup",
                "-P",
                self.loop_device,
                ewf_file
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error setting up loop device: {e}")
            raise

    def _run_photorec(self):
        """Run PhotoRec on the mounted image."""
        try:
            # Create a directory for recovered files
            recovery_output = os.path.join(self.recovery_dir, 'recup_files')
            os.makedirs(recovery_output, exist_ok=True)
            
            print(f"Starting file recovery with PhotoRec...")
            print(f"Recovered files will be saved to: {recovery_output}")
            
            # Run PhotoRec with the loop device instead of ewf file
            subprocess.run([
                "sudo", "photorec",
                "/d",  # Specify recovery directory
                recovery_output,
                "/cmd",  # Use command line mode
                self.loop_device,  # Use loop device instead of ewf file
                "search"  # Start search immediately
            ], check=True)
            
            print(f"File recovery completed. Files saved to: {recovery_output}")
            self.mount_points = [recovery_output]
            
        except subprocess.CalledProcessError as e:
            print(f"Error running PhotoRec: {e}")
            print("Continuing with analysis of any recovered files...")

    def cleanup(self):
        """Clean up mounted images and temporary files."""
        try:
            # Ensure we're not in any mounted directory
            os.chdir('/')
            
            # Unmount and cleanup
            self.check_and_unmount()
            
            # Clean up mount point if it exists and is empty
            if os.path.exists(self.mount_point) and not os.listdir(self.mount_point):
                os.rmdir(self.mount_point)
                
        except Exception as e:
            print(f"Error during cleanup: {e}")