import os
import time
def clean_temp_dir(directory_path):
    """
    Deletes files older than 10 minutes from the specified directory.
    
    Args:
        directory_path (str): Path to the temporary directory.
    """
    now = time.time()
    ten_minutes = 10 * 60  # seconds

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)
            if file_age > ten_minutes:
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
					
if __name__ == '__main__':
	clean_temp_dir('./tmp/')