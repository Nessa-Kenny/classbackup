import logging
import boto3
from botocore.exceptions import ClientError


def list_buckets():
    # Retrieve the list of existing buckets
    s3_client = boto3.client('s3')
    response = s3_client.list_buckets()

    # Output the bucket names
    print('Existing buckets:')
    for bucket in response['Buckets']:
        print('\t', bucket["Name"])
    

def list_objects_v2():
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(
        Bucket ='dub123'
    )
    
    print(response)


def download_file():
    s3_client = boto3.client('s3')
    response = s3_client.download_file('dub123','church1','church.jpg')

    
def main():
    import argparse
    parser = argparse.ArgumentParser()
    #parser.add_argument('bucket_name', help='The name of the bucket.')
    #parser.add_argument('--file_name', help='The name of the file to upload.')
    #parser.add_argument('--object_key', help='The object key')

    region = 'us-east-1'
  
    args = parser.parse_args()
    #create_bucket(args.bucket_name)
    #list_buckets()
    list_objects_v2()
    download_file()
    #upload_file(args.file_name,args.bucket_name, args.object_key)
    #delete_object(region, args.bucket_name, args.object_key)
    #delete_bucket(region, args.bucket_name)
 
 

if __name__ == '__main__':
 main()