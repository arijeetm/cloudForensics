import urllib
import boto3
import pymysql
from md5checker import make_hash

hostname= '54.241.144.63'
username='ubuntu'
password='insure'
database='hashdb'
dstbucket= 'insure-bloom'
pwd= '/tmp/'

def isBadHash(md5, sha1):
    try:
        conn = pymysql.connect(host=hostname, user=username, passwd=password, db=database)
        cur = conn.cursor()
        cur.execute("SELECT status from hashtables where md5='" + md5 +"' and sha1='" + sha1 + "'")
        print cur.fetchall()
        return cur.fetchall() == 'BAD'
    except Exception as e:
        print ('Error occurred while connecting to database {}'.format(hostname))
        raise e
    finally:
        conn.close()

def lambda_handler(event, context):
    r''' handles the image files and directs it to ghiro for digital forensics'''
    bucket= event['Records'][0]['s3']['bucket']['name']
    srcbucket = boto3.resource('s3').Bucket(bucket)
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        srcbucket.download_file(key, pwd+ key)
    except Exception as e:
        print(
            'Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(
                key, bucket))
        raise e
    try:
        md5hash= make_hash(pwd+ key)
        sha1= make_hash(pwd+ key, algo='sha1')
    except Exception as e:
        print ('Error occurred while computing hash of the file {}', key)
        raise e

    if isBadHash(md5hash, sha1)== False:
        boto3.client('s3').copy_object(Bucket=dstbucket, CopySource={'Bucket': bucket, 'Key': key},
                       Key=key)

