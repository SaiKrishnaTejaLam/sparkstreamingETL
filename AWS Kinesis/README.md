## Amazon Kinesis: Real-Time Data Streaming

What is Amazon Kinesis?

Amazon Kinesis is a fully managed service that allows you to process real-time data streams at massive scale. It enables the ingestion, storage, and real-time processing of streaming data from various sources. 
Kinesis is designed to handle large volumes of data and is commonly used in real-time analytics, log and event data collection, and integrating with other AWS services for further processing.

In a Change Data Capture (CDC) pipeline, Kinesis is used to capture data changes (like inserts, updates, and deletes) from a source system, such as a database, and stream this data to 
downstream services for processing and storage.

## Purpose of Amazon Kinesis in a CDC Pipeline

In a CDC pipeline, Kinesis serves several key purposes:

**1.Real-Time Data Streaming:** Kinesis enables real-time streaming of data changes from the source system (e.g., Amazon RDS) to downstream processing systems (e.g., AWS Glue, Amazon S3). 
							This ensures that data is processed as soon as changes occur in the source database.

**2.Data Buffering:** Kinesis temporarily buffers data in shards before it is consumed by downstream services. This ensures that even if downstream systems experience temporary delays, no data is lost.

**3.Scalability:** Kinesis can scale to handle large volumes of data. As data throughput grows, the number of shards in the stream can be increased to maintain performance and avoid bottlenecks.

**4.Fault Tolerance:** Kinesis retains the ingested data for a configurable retention period (up to 24 hours by default). If there are delays or failures in downstream processing, 
					Kinesis ensures that the data is available for reprocessing.
					
					
**Steps to Create a Kinesis Data Stream for CDC**
	
**Step 1: Create Kinesis Data Stream**
    

**1.Sign in to AWS Console & Open Kinesis:**

*Go to the AWS Management Console and sign in.

*In the Services menu, search for and select Amazon Kinesis.

<img src="https://bitbucket.org/ivorsource/kinesis/raw/f355ab55d7283068ce89e2ef303c4123f34184d5/images/k.png">


**2.Create a Data Stream:**

*Click on Create data stream.

*Enter Stream Name: Name your stream (e.g., Kinesis-postgresql).

<img src="https://bitbucket.org/ivorsource/kinesis/raw/f355ab55d7283068ce89e2ef303c4123f34184d5/images/k-2.png">


**3.Choose Capacity Mode:**

*On-demand: Auto-scales based on your workload.

*Provisioned: Manually set the number of shards.


<img src="https://bitbucket.org/ivorsource/kinesis/raw/f355ab55d7283068ce89e2ef303c4123f34184d5/images/k-3.png">


**4.Set Number of Shards (if using Provisioned):**

*1 shard = 1 MB/sec input, 2 MB/sec output. Choose based on your expected throughput (you can start with 1-2 shards, then scale as needed).

*Review: Confirm the configuration.

*Click Create stream.

*After creating you can see your created data stream.

<img src="https://bitbucket.org/ivorsource/kinesis/raw/f355ab55d7283068ce89e2ef303c4123f34184d5/images/k-4.png">
<br>
<br>
<br>
<br>
<br>
<br>
<img src="https://bitbucket.org/ivorsource/kinesis/raw/f355ab55d7283068ce89e2ef303c4123f34184d5/images/image%20(2).png">


**Step 2: Enable Data Capture via Kinesis**


**1.Configure Data Producers to Push Data to Kinesis:**

*Use CDC tools (like AWS DMS) or other applications to capture changes from your database and push them to your Kinesis stream.

*Data format: Ensure data captured in CDC is in a format that can be processed by Kinesis (e.g., JSON, CSV).


**2.Set up the Data Producer:**

*You will need to implement a Kinesis Producer to send CDC events (inserts, updates, deletes) to the Kinesis stream. This can be done by using the Kinesis Producer Library (KPL) or other custom applications.

*Ensure the data follows a structure that can be consumed by downstream systems (like AWS Lambda, EC2, etc.).


**Step 3: Monitor the Kinesis Stream**
	

**1.Monitor the Kinesis Data Stream:**

*In the Kinesis Console, you can monitor stream activity (records, shards, and throughput).

*Track how much data is flowing into the stream to ensure it matches your expected throughput.


<img src="https://bitbucket.org/ivorsource/kinesis/raw/f355ab55d7283068ce89e2ef303c4123f34184d5/images/image.png">
<br>
<br>
<br>
<br>
<img src="https://bitbucket.org/ivorsource/kinesis/raw/f355ab55d7283068ce89e2ef303c4123f34184d5/images/image%20(1).png">


**2.Check for Errors:**

*If you are using Provisioned mode, make sure to monitor for throttling or shard splitting events, and adjust the number of shards if needed.

*Ensure data records are being successfully ingested and there is no loss of data in the stream.


**Step 4: Process CDC Data in Kinesis**

**1.Use Kinesis Data Analytics:**

*Set up Kinesis Data Analytics to run real-time SQL queries on the incoming CDC data.

*You can perform operations like windowed aggregation, filtering, and other analytics in real time.


**2.Set Up Data Consumers:**

*You can use Kinesis Consumers such as EC2 instances, custom applications, or other AWS services like Kinesis Data Firehose to process and analyze the CDC data.