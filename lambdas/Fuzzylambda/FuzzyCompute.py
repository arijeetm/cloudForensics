import urllib
import boto3
import pymysql
import ssdeep
import subprocess
hostname= '54.241.144.63'
username='ubuntu'
password='insure'
database='hashdb'
dstbucket= 'insure-bloom'

s3 = boto3.client('s3')

def isBadHash(input_hash):
    try:
        conn = pymysql.connect(host=hostname, user=username, passwd=password, db=database)
        cur = conn.cursor()
        cur.execute("SELECT status from hashtables where md5='" + input_hash +"'")
        print cur.fetchall()
        return cur.fetchall() == 'BAD'
    except Exception as e:
        print ('Error occurred while connecting to database for {}'.format(input_hash))
        raise e
    finally:
        conn.close()

def lambda_handler(event, context):
    r''' handles the image files and directs it to ghiro for digital forensics'''
    srcbucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        response = s3.get_object(Bucket=srcbucket, Key=key)
    except Exception as e:
        print(
            'Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(
                key, srcbucket))
        raise e
    try:
        hashval= ssdeep.hash(response['Body'].read())
    except Exception as e:
        print ('Error occurred while computing hash of the file {}', key)
        raise e

    try:
        if isBadHash(hashval)== False:
            s3.copy_object(Bucket=dstbucket, CopySource={'Bucket': srcbucket, 'Key': key},
                           Key=key)
    except Exception as e:
        print ('Error occurred while comparing hash of the file {}'.format(key))
        raise e

