from os import walk


# Grab all files from a folder with root directory
def grab_all_files(folder_path):
    f = []
    for (dir_path, dir_names, file_path) in walk(folder_path):
        temp = [dir_path.replace("\\", "/") + "/" + files for files in file_path]
        f.extend(temp)
    return f

