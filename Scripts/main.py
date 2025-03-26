import json
import logging
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr, from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Hardcoded parameters
JOB_NAME = "my_kinesis_to_hudi"
STREAM_NAME = "upstream"
HUDI_TABLE_PATH = "s3://data-engineering-sam0612/kinesis_hudi/"
REGION = "us-east-1"
STARTING_POSITION = "LATEST"  # Options: "TRIM_HORIZON" or "LATEST"

# Initialize Spark and Glue contexts
conf = SparkConf()
conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
conf.set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.hudi.catalog.HoodieCatalog")
conf.set("spark.sql.extensions", "org.apache.spark.sql.hudi.HoodieSparkSessionExtension")

sc = SparkContext(conf=conf)
glueContext = GlueContext(sc)
spark = glueContext.spark_session
sc.setLogLevel("DEBUG")  # Enable debug logging

logger.info("Spark and Glue contexts initialized.")

# Define schema for incoming JSON data
data_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("time_stamp", StringType(), True)
])

metadata_schema = StructType([
    StructField("timestamp", StringType(), True),
    StructField("record-type", StringType(), True),
    StructField("operation", StringType(), True),
    StructField("partition-key-type", StringType(), True),
    StructField("schema-name", StringType(), True),
    StructField("table-name", StringType(), True),
    StructField("transaction-id", IntegerType(), True)
])

event_schema = StructType([
    StructField("data", data_schema, True),
    StructField("metadata", metadata_schema, True)
])

logger.info("Schemas defined.")

# Read streaming data from Kinesis
logger.info(f"Reading streaming data from Kinesis stream: {STREAM_NAME}")
kinesis_df = spark.readStream.format("kinesis") \
    .option("streamName", STREAM_NAME) \
    .option("endpointUrl", f"https://kinesis.{REGION}.amazonaws.com") \
    .option("startingPosition", STARTING_POSITION) \
    .load()

logger.info("Kinesis stream read successfully.")

# Convert binary data to string and parse JSON
logger.info("Parsing JSON data from Kinesis stream.")
parsed_df = kinesis_df.selectExpr("CAST(data AS STRING) as json_record") \
    .withColumn("json_data", from_json(col("json_record"), event_schema)) \
    .select(
        col("json_data.data.id"),
        col("json_data.data.name"),
        col("json_data.data.gender"),
        col("json_data.data.time_stamp"),
        col("json_data.metadata.operation").alias("operation")
    )

# Filter out records with NULL values in the `data` fields
logger.info("Filtering out records with NULL values in the `data` fields.")
filtered_df = parsed_df.filter(
    col("id").isNotNull() &
    col("name").isNotNull() &
    col("gender").isNotNull() &
    col("time_stamp").isNotNull()
)

# Log the schema of the processed DataFrame
logger.info("Schema of processed DataFrame:")
filtered_df.printSchema()

# Log a sample of the processed data
logger.info("Sample data from processed DataFrame:")
filtered_df.writeStream \
    .format("console") \
    .option("truncate", "false") \
    .start() \
    .awaitTermination(timeout=10)  # Log sample data for 10 seconds

# Define function to write to Hudi using foreachBatch()
def write_to_hudi(batch_df, batch_id):
    logger.info(f"Processing batch ID: {batch_id}")
    logger.info(f"Number of records in batch: {batch_df.count()}")

    if batch_df.isEmpty():
        logger.info("Skipping empty batch.")
        return

    # Log a sample of the batch data
    logger.info("Sample data in batch:")
    batch_df.show(5, truncate=False)

    hudi_options = {
        "hoodie.table.name": "dummy_table",
        "hoodie.datasource.write.recordkey.field": "id",
        "hoodie.datasource.write.precombine.field": "time_stamp",
        "hoodie.datasource.write.operation": "upsert",
        "hoodie.datasource.write.hive_style_partitioning": "true",
        "hoodie.datasource.write.table.type": "COPY_ON_WRITE",
        "path": HUDI_TABLE_PATH
    }

    logger.info("Writing batch to Hudi table.")
    try:
        # Specify the fully qualified class name for Hudi
        batch_df.write.format("org.apache.hudi").options(**hudi_options).mode("append").save()
        logger.info(f"Batch {batch_id} written to Hudi table successfully.")
    except Exception as e:
        logger.error(f"Error writing batch {batch_id} to Hudi table: {str(e)}")
        raise e

    # Read and display all records from the Hudi table
    logger.info("Reading and displaying all records from the Hudi table:")
    hudi_df = spark.read.format("hudi").load(HUDI_TABLE_PATH)
    
    # Convert to Pandas DataFrame for better formatting
    hudi_pandas_df = hudi_df.toPandas()
    
    # Log the Hudi table records
    logger.info("\n" + "=" * 80)
    logger.info("Hudi Table Records:")
    logger.info("\n" + hudi_pandas_df.to_string(index=False))
    logger.info("=" * 80 + "\n")

# Use foreachBatch() for Hudi micro-batching
logger.info("Starting streaming query.")
query = filtered_df.writeStream \
    .foreachBatch(write_to_hudi) \
    .outputMode("append") \
    .option("checkpointLocation", HUDI_TABLE_PATH + "/checkpoints") \
    .start()

logger.info("Streaming query started. Waiting for termination.")
query.awaitTermination()