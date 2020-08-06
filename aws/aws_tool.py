# Created by Brandon Nguyen
# Last modified: 7/30/2020
# Created for the purpose of using boto3/aws simply by calling the functions of a class

# Credits To
# - Glen Thompson for the progress bar -- "https://tinyurl.com/y3b6fqmt"


import boto3
from botocore.exceptions import ClientError
import logging
import os
import sys
import time
from multiprocessing import Pool  # Better for CPU Bound process  i.e (number crunching, processing)
from multiprocessing.dummy import Pool as ThreadPool  # Better for I/O Bound process i.e network, http/database request
from data_processing import general_utilities  # From the data_processing folder, importing code to traverse directory
from pprint import pprint

""" Naming Conventions and Abbreviations 
{
    fn: "file name"    
}
"""
s3 = boto3.resource('s3')  # High level variation
s3_client = boto3.client('s3')  # Low-level variation


class aws_tool(object):
    def __init__(self):
        self.root_fn = None
        self.folder_path = None

    def get_bucket_object(self, bucket_name):
        bucket = s3.Bucket(bucket_name)
        bucket_objects = [contents.key for contents in bucket.objects.all()]
        return bucket_objects

    def get_buckets(self):
        buckets = [bucket.name for bucket in s3.buckets.all()]
        return buckets

    def get_size(self, bucket_name, key):
        bucket = s3.Bucket(bucket_name)
        contente_size = [obj.get()["ContentLength"] for obj in bucket.objects.all() if key in obj.key]
        assert len(contente_size) == 1, "No object exist with with the name of '{}'".format(key)
        return contente_size[0]

    # Traverse a local disk directory and upload items to S3 bucket
    def upload_folder(self, bucket_name, folder_path, multiprocessing_cpu_count=1):
        # Turns "root\file.txt" to "root/file.txt" for parsing
        if "\\" in folder_path:
            folder_path = folder_path.replace("\\", "/")
        self.folder_path = folder_path
        self.root_fn = folder_path.rsplit("/", 1)[1]
        # Grab list of objects to upload
        files_to_upload = general_utilities.grab_all_files(folder_path)
        # Upload list of files using Threading
        with ThreadPool(multiprocessing_cpu_count) as pool:
            pool.starmap(self.upload_file, zip([bucket_name]*len(files_to_upload), files_to_upload))

    # # Uploads a single file to the bucket
    def upload_file(self, bucket_name, file_path):
        total_length = int(os.path.getsize(file_path))
        upload = 0

        def progress(chunk):
            nonlocal upload
            upload += chunk
            done = int(50 * upload / total_length)
            sys.stdout.write("\r[%s%s]%s%s%s" % ('=' * done, ' ' * (50 - done), ' ', done*2, '%'))
            sys.stdout.flush()

        if "\\" in file_path:
            file_path = file_path.replace("\\", "/")
        if (self.root_fn is None) or (self.folder_path is None):
            uploaded_file_name = file_path.rsplit("/", 1)[1]
        else:
            uploaded_file_name = self.root_fn + file_path.split(self.folder_path, 1)[1]
        try:
            response = s3.meta.client.upload_file(file_path, bucket_name, uploaded_file_name, Callback=progress)
        except ClientError as e:
            logging.error(e)

    def download_bucket(self, bucket_name, prefix=None, multiprocessing_cpu_count=1):
        bucket_objects = self.get_bucket_object(bucket_name)
        if prefix:
            s3_keys = [obj for obj in bucket_objects if prefix in obj]
        else:
            s3_keys = [obj for obj in bucket_objects]
        with ThreadPool(multiprocessing_cpu_count) as pool:
            pool.starmap(self.download_bucket_file, zip([bucket_name]*len(s3_keys), s3_keys, [True]*len(s3_keys)))

    def download_bucket_file(self, bucket_name, s3_key, absolute_path=False):

        total_length = self.get_size(bucket_name=bucket_name, key=s3_key)
        upload = 0
        def progress(chunk):
            nonlocal upload
            upload += chunk
            done = int(50 * upload / total_length)
            sys.stdout.write("\r[%s%s]%s%s%s" % ('=' * done, ' ' * (50 - done), ' ', done*2, '%'))
            sys.stdout.flush()

        if absolute_path:
            try:
                os.makedirs(s3_key.rsplit("/", 1)[0])
            except Exception as e:
                if "Cannot create a file when that file already exists" in str(e):
                    pass
                else:
                    logging.error(e)
                    raise e
            save_file_as = s3_key
        elif "/" in s3_key:
            save_file_as = s3_key.rsplit("/", 1)[1]
        else:
            save_file_as = s3_key
        try:
            s3.Bucket(bucket_name).download_file(s3_key, save_file_as, Callback=progress)
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                logging.error("Object does not exist")
            else:
                logging.error(e)
                raise e
