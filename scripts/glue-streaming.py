import sys
import pandas as pd
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import logging
from pyspark.sql import DataFrame, Row
import datetime
from awsglue import DynamicFrame
import json

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)


logger = glueContext.get_logger()

# Script generated for node Kinesis Stream
dataframe_KinesisStream_node1 = glueContext.create_data_frame.from_options(
    connection_type="kinesis",
    connection_options={
        "typeOfData": "kinesis",
        "streamARN": "arn:aws:kinesis:us-east-1:<acc-number>:stream/quest-data-stream",
        "classification": "json",
        "startingPosition": "latest",
        "inferSchema": "true",
    },
    transformation_ctx="dataframe_KinesisStream_node1",
)

logger = glueContext.get_logger()

# Run the transformation for each batch of data
def processBatch(data_frame, batchId):
    if data_frame.count() > 0:
        # loads the dataframe into a dynamicframe
        dynamicframe = DynamicFrame.fromDF(data_frame, glueContext, "from_data_frame")
        # dynamicframe to pandas dataframe
        pandas_dataframe = dynamicframe.toDF().toPandas()
        assert list(pandas_dataframe.columns) == [
            "command",
            "dest",
            "source",
        ], pandas_dataframe
        # Iterating through each user request
        for index, row in pandas_dataframe.iterrows():

            if row.command == "copy":
                file_type = row.source.split(".")[-1]
                source = (
                    spark.read.format(file_type)
                    .options(inferSchema="true")
                    .load(row.source)
                )
                source.write.format(file_type).mode("overwrite").save(row.dest)


glueContext.forEachBatch(
    frame=dataframe_KinesisStream_node1,
    batch_function=processBatch,
    options={
        "windowSize": "1 seconds",
        "checkpointLocation": args["TempDir"] + "/" + args["JOB_NAME"] + "/checkpoint/",
    },
)
job.commit()
