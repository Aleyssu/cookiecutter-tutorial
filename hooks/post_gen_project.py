import os
import shutil
from pathlib import Path

REMOVE_PATHS = []
MOVE_PATHS = []

keep_files = '{{ cookiecutter.keep_files }}'

if keep_files == "test1.txt":
    REMOVE_PATHS.append("test2.txt")
elif keep_files == "test2.txt":
    REMOVE_PATHS.append("test1.txt")
elif keep_files == "none":
    REMOVE_PATHS += ["test1.txt", "test2.txt"]

    
path_to_remove: str
for path_to_remove in REMOVE_PATHS:
    path_to_remove = path_to_remove.strip()
    if path_to_remove and os.path.exists(path_to_remove):
        if os.path.isdir(path_to_remove):
            shutil.rmtree(path_to_remove)
        else:
            os.unlink(path_to_remove)