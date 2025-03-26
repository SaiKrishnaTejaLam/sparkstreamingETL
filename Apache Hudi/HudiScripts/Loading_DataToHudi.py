import sys
import logging
from pyspark import SparkConf, SparkContext
from awsglue.context import GlueContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Print sys.path for debugging
print("\n.  ------>.   ".join(sys.path))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create SparkConf and set configurations
conf = SparkConf()
conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
conf.set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.hudi.catalog.HoodieCatalog")
conf.set("spark.sql.extensions", "org.apache.spark.sql.hudi.HoodieSparkSessionExtension")

# Initialize SparkContext with the configurations
try:
    logger.info("Initializing SparkContext with KryoSerializer...")
    sc = SparkContext(conf=conf)
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    
    logger.info("GlueContext initialized successfully.")
except Exception as e:
    logger.error("Failed to initialize GlueContext: %s", e)
    sys.exit(1)

# Debug: Print all Spark configurations to verify they are applied correctly
# logger.info("Printing all Spark configurations to verify...")
# spark_conf = spark.sparkContext.getConf().getAll()
# for conf in spark_conf:
#     logger.info(f"Config: {conf[0]} = {conf[1]}")

# Sample Data
data = [
    ("1", "Alice", 25),
    ("2", "Bob", 30),
    ("3", "Charlie", 35)
]

schema = StructType([
    StructField("id", StringType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])

# Create DataFrame
try:
    logger.info("Creating DataFrame from sample data...")
    df = spark.createDataFrame(data, schema)
    logger.info("DataFrame created successfully.")
except Exception as e:
    logger.error("Failed to create DataFrame: %s", e)
    sys.exit(1)

# Define Hudi Table Path and Options
hudi_table_path = "s3://data-engineering-sam0612/hudi/"

hudi_options = {
    "hoodie.table.name": "hudi_table",
    "hoodie.datasource.write.storage.type": "COPY_ON_WRITE",  # or "MERGE_ON_READ"
    "hoodie.datasource.write.recordkey.field": "id",
    "hoodie.datasource.write.precombine.field": "age",
    "hoodie.datasource.write.operation": "upsert",  # Options: "bulk_insert", "insert", "upsert"
    "hoodie.datasource.hive_sync.enable": "true",
    "hoodie.datasource.hive_sync.database": "default",
    "hoodie.datasource.hive_sync.table": "hudi_table",
    "hoodie.datasource.hive_sync.use_jdbc": "false",
    "hoodie.write.commit.auto.retry.times": "5"  # Increases commit stability
}

# Write DataFrame to Hudi Table in S3
try:
    logger.info("Writing DataFrame to Hudi Table in S3...")
    
    df.write.format("org.apache.hudi") \
        .options(**hudi_options) \
        .mode("overwrite") \
        .save(hudi_table_path)
    
    logger.info("Hudi Table written successfully to %s", hudi_table_path)
except Exception as e:
    logger.error("Failed to write Hudi Table: %s", e)
    # Print the full Java stack trace
    if hasattr(e, "java_exception"):
        logger.error("Java Exception: %s", e.java_exception.toString())
    if hasattr(e, "message"):
        logger.error("Error Message: %s", e.message)
    sys.exit(1)

logger.info("Glue job completed successfully.")