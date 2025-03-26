import sys
import logging
from pyspark import SparkConf, SparkContext
from awsglue.context import GlueContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

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

# Define Hudi Table Path and Options
hudi_table_path = "s3://data-engineering-sam0612/hudi/"

hudi_read_options = {
    "hoodie.table.name": "hudi_table",
    "hoodie.datasource.read.storage.type": "COPY_ON_WRITE",  # or "MERGE_ON_READ"
}

# Read DataFrame from Hudi Table in S3
try:
    logger.info("Reading DataFrame from Hudi Table in S3...")
    
    df = spark.read.format("org.apache.hudi") \
        .options(**hudi_read_options) \
        .load(hudi_table_path)
    
    logger.info("Hudi Table read successfully from %s", hudi_table_path)
    
    # Show the DataFrame and schema
    logger.info("Initial Data in the Hudi Table:")
    df.show()
    logger.info("Initial Schema of the Hudi Table:")
    df.printSchema()
    
except Exception as e:
    logger.error("Failed to read Hudi Table: %s", e)
    # Print the full Java stack trace
    if hasattr(e, "java_exception"):
        logger.error("Java Exception: %s", e.java_exception.toString())
    if hasattr(e, "message"):
        logger.error("Error Message: %s", e.message)
    sys.exit(1)

# Perform Schema Evolution: Add a New Column

# Define the new schema with an additional column (e.g., "salary")
new_schema = StructType([
    StructField("id", StringType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("salary", DoubleType(), True),
    StructField("Pincode", IntegerType(), True)# New column
])

# Sample Data for Upsert with the new schema
upsert_data = [
    ("1", "Alice", 26, 50000.0,75080),  # Update Alice's age and add salary
    ("4", "David", 40, 60000.0,70172)   # Insert a new record with salary
]

# Create DataFrame for Upsert with the new schema
try:
    logger.info("Creating DataFrame for Upsert with the new schema...")
    upsert_df = spark.createDataFrame(upsert_data, new_schema)
    logger.info("Upsert DataFrame created successfully.")
    
    # Show the Upsert DataFrame
    logger.info("Upsert Data with New Schema:")
    upsert_df.show()
    logger.info("Upsert Schema:")
    upsert_df.printSchema()
except Exception as e:
    logger.error("Failed to create Upsert DataFrame: %s", e)
    sys.exit(1)

# Hudi Options for Writing (Upsert)
hudi_write_options = {
    "hoodie.table.name": "hudi_table",
    "hoodie.datasource.write.storage.type": "COPY_ON_WRITE",  # or "MERGE_ON_READ"
    "hoodie.datasource.write.recordkey.field": "id",          # Primary key
    "hoodie.datasource.write.precombine.field": "age",        # Precombine field
    "hoodie.datasource.write.operation": "upsert",            # Upsert operation
    "hoodie.datasource.hive_sync.enable": "true",             # Sync with Hive
    "hoodie.datasource.hive_sync.database": "default",        # Hive database
    "hoodie.datasource.hive_sync.table": "hudi_table",        # Hive table
    "hoodie.datasource.hive_sync.use_jdbc": "false",          # Disable JDBC sync
    "hoodie.write.commit.auto.retry.times": "5"               # Retry commits
}

# Perform Upsert Operation with the new schema
try:
    logger.info("Performing Upsert operation with the new schema...")
    
    upsert_df.write.format("org.apache.hudi") \
        .options(**hudi_write_options) \
        .mode("append") \
        .save(hudi_table_path)
    
    logger.info("Upsert operation completed successfully.")
    
    # Read the updated Hudi Table
    updated_df = spark.read.format("org.apache.hudi") \
        .options(**hudi_read_options) \
        .load(hudi_table_path)
    
    logger.info("Data in the Hudi Table after Schema Evolution:")
    updated_df.show()
    logger.info("Updated Schema of the Hudi Table:")
    updated_df.printSchema()
    
except Exception as e:
    logger.error("Failed to perform Upsert operation: %s", e)
    # Print the full Java stack trace
    if hasattr(e, "java_exception"):
        logger.error("Java Exception: %s", e.java_exception.toString())
    if hasattr(e, "message"):
        logger.error("Error Message: %s", e.message)
    sys.exit(1)

logger.info("Glue job completed successfully.")