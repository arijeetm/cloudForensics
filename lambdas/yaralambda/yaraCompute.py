import urllib
import boto3
import pymysql
from md5checker import make_hash
import yara
import time, datetime

hostname= '52.53.232.186' # update db hostname
username='ubuntu'
password='insure'
database='FHR'

s3= boto3.resource('s3')
toolbucket= s3.Bucket('insure-tools')
dstbucket= 'insure-filtered'
rule_file='compiled_rules'
pwd= '/tmp/'
s3_client= boto3.client('s3')

def insertTodb(file):
    try:
        md5hash= make_hash(file)
        sha1= make_hash(file, algo='sha1')
    except Exception as e:
        print ('Error occurred while computing hash of the file {}', file)
        raise e
    print ('inserting hash ' + md5hash)
    insert_stmt = (
        "INSERT INTO File(sha1, md5, status, date, certainty)  "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    currtime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
    accuracy = 100 # giving high bias to feedback to evolve db and make it faster wit time and volume
    data = (sha1, md5hash, 'BAD', currtime, accuracy) # BAD is special keyword for suspicious or malware file from feedback
    try:
        conn = pymysql.connect(host=hostname, user=username, passwd=password, db=database)
        cur = conn.cursor()
        cur.execute(insert_stmt, data)
        conn.commit()
    except Exception as e:
        print ('Error occurred while connecting to database {}'.format(hostname))
        raise e
    finally:
        conn.close()

def lambda_handler(event, context):
    r''' handles the image files and directs it to ghiro for digital forensics'''
    bucket= event['Records'][0]['s3']['bucket']['name']
    srcbucket = s3.Bucket(bucket)
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        toolbucket.download_file(rule_file, pwd+ rule_file)
        rules= yara.load(pwd+ rule_file)
    except Exception as e:
        print(
            'Error getting rules from bucket. Make sure they exist and your bucket is in the same region as this function.')
        raise e

    try:
        srcbucket.download_file(key, pwd + key)
        m= rules.match(pwd+ key)
    except Exception as e:
        print(
            'Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(
                key, bucket))
        raise e

    # if known bad file add to db for pruning
    if len(m) > 0:
        insertTodb(pwd+ key)
    else:
        s3_client.copy_object(Bucket=dstbucket, CopySource={'Bucket': bucket, 'Key': key},
                              Key=key)
        s3_client.delete_object(Bucket=bucket, Key=key)

