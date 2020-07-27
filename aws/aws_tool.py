import boto3
from botocore.exceptions import ClientError
import logging
from data_processing import general_utilities  # From the data_processing folder, importing code to path walk directory


""" Naming Conventions and Abbreviations 
{
    fn: "file name"    
}
"""
class aws_tool(object):
    def __init__(self, bucket_name):
        self.s3 = boto3.resource('s3')  # High level variation
        self.s3_client = boto3.client('s3')  # Low-level variation
        self.bucket_name = bucket_name

    def get_bucket_object(self):
        pass

    # Transverse a local disk directory and upload items to S3 bucket
    def upload_folder(self, folder_path):
        # Turns "root\\file.txt" to "root/file.txt" for parsing
        if "\\" in folder_path:
            folder_path = folder_path.replace("\\", "/")
        # Grab list of objects to upload
        files_to_upload = general_utilities.grab_all_files(folder_path)
        root_fn = folder_path.rsplit("/", 1)[1]
        for file_location in files_to_upload:
            uploaded_file_name = root_fn + file_location.split(folder_path, 1)[1]
            try:
                response = self.s3.meta.client.upload_file(file_location, self.bucket_name, uploaded_file_name)
            except ClientError as e:
                logging.error(e)
