import sys
import logging
from pyspark import SparkConf, SparkContext
from awsglue.context import GlueContext
from pyspark.sql import SparkSession

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
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

# Define Hudi Table Path and Name
hudi_table_path = "s3://data-engineering-sam0612/hudi/"
hudi_table_name = "hudi_table"

# Function to fetch records from the Hudi table using SQL for a particular day
def query_records_by_date(hudi_table_name, query_date):
    try:
        # Load Hudi table into a temporary view
        df = spark.read.format("hudi").load(hudi_table_path)
        df.createOrReplaceTempView(hudi_table_name)

        # Query records from the specific date
        query = f"""
            SELECT * FROM {hudi_table_name}
            WHERE substr(_hoodie_commit_time, 1, 8) = '{query_date.replace("-", "")}'
        """


        result_df = spark.sql(query)

        logger.info(f"Records for {query_date}:")
        result_df.show()

    except Exception as e:
        logger.error(f"Failed to query records for {query_date}: {e}")
        raise e

query_date = "2025-03-03"
query_records_by_date(hudi_table_name, query_date)

logger.info("Script execution completed successfully.")
