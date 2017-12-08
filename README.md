# Data pipeline for File Forensics in Cloud

The system architecture is shown in Figure. It is a pipeline deployed in AWS infrastructure to automate forensics evaluation in Cloud. The forensics investigators needs to drop files into the s3 bucket for persistent storage to start the process. Any incremental changes in the first bucket triggers aws lambda functions to compute the hash of the file and compare it with for known malware and suspicious activities. It moves over the good/undetectable files over to next bucket for further processing by yara analyzers.  
YARA scan compare the signature of the files dropped in the second bucket against the compiled rules of known bad files. It moves over the rest of the good files over to next stage for their fuzzy hash computation by SSDEEP and comparing with known fuzzy hashes of bad files. We are using a centralized MySQL database as a source of truth for known bad files hashes.  
There are separate tables for md5, sha1 hash and fuzzy hashes in this architecture. Bad files detected at any stage in the pipeline is pushed into the database for future pruning at earlier stages. The clean files from SSDEEP evaluation are dropped into an s3 bucket. For any image files changes in this bucket, it triggers a lambda to move the image into a separate workstation for specific image forensics.  
  

# Usage
	run 'make clean build' in lambdas folder  
	run 'make build'  
	Upload the corresponding zip file to lambdas function in AWS and enable the trigger on the s3 bucket  
