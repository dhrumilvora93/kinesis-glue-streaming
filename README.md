# kinesis-glue-streaming

This is a simple glue job that streams data from a Kinesis stream to a S3 Bucket.

## Archtechture:
![alt text](info/image.png)
Users providing input command to kinesis data streams using aws-cli. A constant runnning glue job will pick up the command perform ETL and load data in S3.

## Prerequisites
- AWS CLI

## Usage

To update the glue job:
Perform updates in `glue-streaming.py` and then upload it to s3 bucket

To create the stack:
```
aws cloudformation create-stack --stack-name <stack-name> --capabilities CAPABILITY_IAM --template-body file://template.yml
```

To delete the stack:
```
aws cloudformation delete-s tack --stack-name <stack-name>
```

Command to pass from Kafka Streams:
```
aws kinesis put-record --profile rearc-data-dev --stream-name <stream-name> --partition-key <partition-key> --data '{"source":"<s3-input-path>","dest":"<s3-destination-path>","command":"copy"}' --cli-binary-format raw-in-base64-out
```

## Output
![alt text](info/output.gif)