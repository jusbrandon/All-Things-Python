from os import walk
import multiprocessing
import psutil

from pprint import pprint


# Grab all files from a folder with root directory
def grab_all_files(folder_path):
    f = []
    for (dir_path, dir_names, file_path) in walk(folder_path):
        temp = [dir_path.replace("\\", "/") + "/" + files for files in file_path]
        f.extend(temp)
    return f

# Grab System's Data
def get_system_data():
    system_data = {}
    system_data["CPU Count"] = multiprocessing.cpu_count()/2
    system_data["Total Physical Memory available"] = psutil.virtual_memory()


