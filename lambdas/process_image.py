from __future__ import print_function

import urllib
import boto3
import subprocess

s3 = boto3.resource('s3')
API_KEY= '5505193c-a06b-4f9a-9165-8c45a5963e00'
SITE_ID = 'http://54.193.4.148'
CASE_ID= 1

def lambda_handler(event, context):
    r''' handles the image files and directs it to ghiro for digital forensics'''
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    bucket= s3.Bucket(bucket_name)
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        bucket.download_file(key, '/tmp/'+ key)
    except Exception as e:
        print(
            'Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(
                key, bucket_name))
        raise e
    try:
        requesturl= 'curl -kis -F image=@/tmp/'+ str(key) +' -F case_id='+ str(CASE_ID) +' -F api_key='+ str(API_KEY) + ' ' + str(SITE_ID) +'/api/images/new'
        subprocess.call(requesturl, shell=True)
    except Exception as e:
        print ('Error occurred while making the API call')
        raise e
