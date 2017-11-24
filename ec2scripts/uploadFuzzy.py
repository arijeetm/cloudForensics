from glob import glob
import pymysql
import time, datetime

hostname= '52.53.216.88' # update db hostname
username='ubuntu'
password='insure'
database='FHR'

WORKING_DIRECTORY = './FuzzyHashes/NSRL*'

def insertDB(size, fn, hash):
    insert_stmt = (
        "INSERT INTO FuzzyHash(bsize, fhash, fname, date)  "
        "VALUES (%s, %s, %s, %s)"
    )
    currtime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
    data = (size, hash, fn, currtime)
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

def main():
    data_directories = glob(WORKING_DIRECTORY)
    for dir in data_directories:
        print ('Looking dir into ' + dir)
        filesnames= glob(dir + '/*.ssd')
        for file in filesnames:
            print ('Looking file into ' + file)
            with open(file, 'r') as inf:
                lines = [line.rstrip('\n') for line in inf]
                lines.pop(0)
                for line in lines:
                    size = line.split(':')[0]
                    fname = line.split(',')[1]
                    hash = line[len(size)+1: -len(fname)-1]
                    insertDB(size, fname, hash)

if __name__ == '__main__':
    main()
