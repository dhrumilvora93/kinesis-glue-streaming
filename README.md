# kinesis-glue-streaming



This is a sample Glue job that streams data from a Kinesis stream to a S3 Bucket.

## Prerequisites
- AWS CLI
- S3 Bucket
- IAM Role for glue job

## Usage

To update the glue job:
Perform updates in `sample.py` and then upload it to s3 bucket

To create the stack:
```
aws cloudformation create-stack --stack-name <stack-name> --capabilities CAPABILITY_IAM --template-body file://template.yml
```

To delete the stack:
```
aws cloudformation delete-s tack --stack-name <stack-name>
```




