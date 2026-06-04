import os
import glob

def test_bin_scripts_are_executable():
    bin_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bin")
    bin_files = glob.glob(os.path.join(bin_dir, "*"))
    
    assert len(bin_files) > 0, "No files found in bin directory"
    
    for bin_file in bin_files:
        if os.path.isfile(bin_file):
            assert os.access(bin_file, os.X_OK), f"File {bin_file} is missing the executable bit (+x)"
