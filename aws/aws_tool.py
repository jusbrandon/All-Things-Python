import boto3
from botocore.exceptions import ClientError
import logging
from multiprocessing import Pool
from data_processing import general_utilities  # From the data_processing folder, importing code to path walk directory
import time

""" Naming Conventions and Abbreviations 
{
    fn: "file name"    
}
"""


s3 = boto3.resource('s3')  # High level variation
s3_client = boto3.client('s3')  # Low-level variation


class aws_tool(object):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.root_fn = None
        self.folder_path = None

    def get_bucket_object(self):
        pass

    # Transverse a local disk directory and upload items to S3 bucket
    def upload_folder(self, folder_path, multiprocessing_cpu_count=1):
        # Turns "root\file.txt" to "root/file.txt" for parsing
        if "\\" in folder_path:
            folder_path = folder_path.replace("\\", "/")
        self.folder_path = folder_path
        self.root_fn = folder_path.rsplit("/", 1)[1]
        # Grab list of objects to upload
        files_to_upload = general_utilities.grab_all_files(folder_path)  # A List of files to upload
        with Pool(multiprocessing_cpu_count) as pool:
            pool.map(self.upload_file, files_to_upload)

    # # Uploads a single file to the bucket
    def upload_file(self, file_path):
        if "\\" in file_path:
            file_path = file_path.replace("\\", "/")
        if (self.root_fn is None) or (self.folder_path is None):
            uploaded_file_name = file_path.rsplit("/", 1)[1]
        else:
            uploaded_file_name = self.root_fn + file_path.split(self.folder_path, 1)[1]
        try:
            response = s3.meta.client.upload_file(file_path, self.bucket_name, uploaded_file_name)
        except ClientError as e:
            logging.error(e)
