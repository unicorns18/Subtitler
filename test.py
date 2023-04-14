import sys
from pathlib import Path

def add_parent_path():
    """
    Adds the parent directory of the current file to sys.path
    """
    # Get the path of the current file
    current_file_path = Path(__file__).resolve()
    # Get the parent directory of the current file
    parent_dir_path = current_file_path.parent
    # Add the parent directory to sys.path
    sys.path.append(str(parent_dir_path))