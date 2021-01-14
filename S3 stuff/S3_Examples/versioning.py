# source: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-examples.html
# some of the code included here is taken or adapted from the Amazon S3 examples available on Boto3 documentation

# This code will create a specified bucket
# submit the file to the bucket
# provide an object key to the file
# then delete the bucket and the file


import logging
import boto3
from botocore.exceptions import ClientError



       
        
def put_bucket_versioning():  
    s3_client = boto3.client('s3')
    response = s3_client.put_bucket_versioning(
    Bucket='dub123',## Your Bucket Name here
    VersioningConfiguration={
        'MFADelete': 'Disabled',
        'Status': 'Enabled',
    },
    )
    
    print(response)


    
    
    
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('bucket_name', help='The name of the bucket.')
    parser.add_argument('--file_name', help='The name of the file to upload.')
    parser.add_argument('--object_key', help='The object key')

    region = 'us-east-1'
  
    args = parser.parse_args()
    #create_bucket(args.bucket_name)
    #list_buckets()
    #upload_file(args.file_name,args.bucket_name, args.object_key)
    get_bucket_versioning()
    put_bucket_versioning()
    bucket_versioning()
    delete_object(region, args.bucket_name, args.object_key)
    delete_bucket(region, args.bucket_name)
 
 

if __name__ == '__main__':
 main()