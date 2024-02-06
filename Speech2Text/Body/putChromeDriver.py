import shutil

source_file = "path/to/source/chromedriver.exe"
destination_file = "path/to/destination Disk/Speech2Text/chromedriver.exe"

# Copy the file
shutil.copyfile(source_file, destination_file)

print(f"File copied from {source_file} to {destination_file}")
