**Amazon Database Migration Service (DMS)** is a cloud service provided by Amazon Web Services (AWS) that helps you migrate databases to AWS quickly and securely. Whether you're moving your on-premises database to AWS or between AWS databases, DMS simplifies the process of database migration.

### **1. Create a Replication Instance**
A replication instance is used to perform the actual migration between your source and target databases.

- **Step 1:** Go to the AWS DMS Console.
- **Step 2:** Click Create replication instance.
<br>
<br>
<img src="https://bitbucket.org/ivorsource/RDS/raw/175db0f71c29a7a96115874ebe497982ec649135/Pictures/Creating%20Replication%20Instance.png">
<br>
<br>
- **Step 3:** Enter details such as:
	- Name of the replication instance.
	- Instance class (select an instance size based on your needs).
	- VPC (ensure it’s in the same VPC as your source and target databases).
	- Select the **Single-AZ** option.
- **Step 4:** Launch the replication instance.

### **2. Create Source and Target Endpoints**

**SOURCE ENDPOINT**

**Step 1:** Navigate to AWS DMS, go to Endpoints, click Create endpoint, and select Source endpoint.

**Step 2:** Configure Source Endpoint Settings

 - **Endpoint Identifier:** Provide a unique name for the endpoint.
 - **Source Engine:** Choose the source database engine (e.g., MySQL, PostgreSQL, Oracle, SQL Server, etc.).
 - **Access Method:** Choose how AWS DMS will connect to your source database:
	 - AWS Secrets Manager (if using credentials stored in Secrets Manager).
	 - Provide access information manually (if entering connection details manually).
	 
**Step 3:** Provide Connection Details

- **Server name** – Enter the hostname or IP address of the source database.
- **Port** – Specify the database port (e.g., MySQL default is 3306, PostgreSQL is 5432).
- **User name** – Provide the database username.
- **Password** – Enter the database password.
- **Database name** – Enter the specific database you want to migrate.
<br>
<br>
<img src="https://bitbucket.org/ivorsource/RDS/raw/175db0f71c29a7a96115874ebe497982ec649135/Pictures/Source%20Endpoint%20Settings.png">
<br>
<br>

**Step 4:** Test the Connection

- Scroll down and click Test connection.
- Ensure that your AWS DMS instance has the correct network access (VPC, Security Groups, and IAM permissions) to connect to the source database.
<br>

**TARGET ENDPOINT**


**Step 1:** Navigate to AWS DMS, go to Endpoints, click Create endpoint, and select Target endpoint.

**Step 2:** Configure Target Endpoint Settings

- **Endpoint Identifier** – Provide a unique name for the target endpoint.
- **Target Engine** – Select Amazon Kinesis.
- **Kinesis Stream ARN** – Enter the Amazon Resource Name (ARN) of your Kinesis stream.
- **Message Format** – Choose the format for the records sent to Kinesis (e.g., JSON).
- **Service Access Role ARN** – Provide the IAM Role ARN that allows AWS DMS to write to Kinesis.
<br>
<br>
<img src="https://bitbucket.org/ivorsource/RDS/raw/175db0f71c29a7a96115874ebe497982ec649135/Pictures/Target%20Endpoint%20Settings.png">
<br>
<br>

**Step 3:** Test the Connection

- Click Test connection to verify that AWS DMS can write to the Kinesis stream.
- Ensure the IAM role has the necessary permissions and the Kinesis stream exists.


### Create a Data Migration Task in AWS DMS

**Step 1:** Open AWS DMS Console -> click Database migration tasks -> Click Create task.

**Step 2:** Configure Task Settings

- **Task Identifier** – Provide a unique name for the migration task.
- **Replication Instance** – Select the replication instance to use.
- **Source Endpoint** – Select the source database endpoint.
- **Target Endpoint** – Select the target database or Kinesis endpoint.
- **Migration Type** – Choose one of the following:
	- Migrate existing data (one-time migration).
	- Migrate existing data and replicate ongoing changes (CDC – Change Data Capture).
	- Replicate data changes only (continuous CDC)
<br>
<br>

<img src="https://bitbucket.org/ivorsource/RDS/raw/175db0f71c29a7a96115874ebe497982ec649135/Pictures/Migration%20Task%20Settings.png">
<br>
<br>

**Step 3:** Scroll down to the Selection rules section add click new selection rule.

**Step 4**: Define Schema and Table Selection

- **Schema** – Enter the schema name (or leave blank if not schema-specific).
- **Source Name** – Enter the source schema name (e.g., public).
- **Source Table Name** – Specify the table name (e.g., employees).
- **Action** – Select Include to migrate the table(s) or Exclude to ignore them.
<br>
<br>
<img src="https://bitbucket.org/ivorsource/RDS/raw/175db0f71c29a7a96115874ebe497982ec649135/Pictures/Selection%20rule%20settings.png">
<br>
<br>

**Step 5:** Specify S3 Bucket for Report Storage
<br>
<br>
<img src="https://bitbucket.org/ivorsource/RDS/raw/175db0f71c29a7a96115874ebe497982ec649135/Pictures/Selecting%20S3%20Bucket.png">
<br>
<br>

**Step 6:** Click Create database migration task

**Step 7:** After sucessfull creation, you can able to see Insertions, Deletions and all kinds of changes happening in our database table from **Table statistics** column
<br>
<br>
<img src="https://bitbucket.org/ivorsource/RDS/raw/175db0f71c29a7a96115874ebe497982ec649135/Pictures/Checking%20Table%20Statistics.png">
<br>
<br>