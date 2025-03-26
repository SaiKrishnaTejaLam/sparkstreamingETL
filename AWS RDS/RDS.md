**Amazon RDS (Relational Database Service)** is a fully managed relational database service provided by AWS (Amazon Web Services). It simplifies the process of setting up, operating, and scaling a relational database in the cloud. RDS supports multiple database engines, allowing users to choose from a variety of database options based on their needs. 

# Steps to use Amazon RDS

### **1. Sign In to Your AWS Account**

First, sign in to your AWS Management Console. If you don’t have an AWS account, you’ll need to [create one](https://aws.amazon.com/)

### **2. Navigate to Amazon RDS** 

In the AWS Management Console, search for "RDS" in the search bar at the top or find it under Services → Databases → RDS. 


<img src="https://bitbucket.org/ivorsource/RDS/raw/d0733f5be3078ac4555eefe1aca0e811842a1b04/Pictures/Search%20for%20RDS.png">



### **3. Create a New Database**

On the RDS Dashboard, click on the Create database button to start the process of launching a new RDS instance. 

### **4. Choose Database Engine** 

You'll be prompted to choose the database engine that you'd like to use for your RDS instance. For Free Tier, you can choose from: 

- MySQL 

- PostgreSQL 

- MariaDB 

- Oracle (BYOL - Bring Your Own License) 

- SQL Server Express Edition (Free Edition) 

Select one of these engines. For the purposes of the Free Tier, let’s assume we choose **PostgreSQL.** 

### **5. Choose Use Case**

In the next step, under Use case, select **Free tier.** This automatically configures the settings for a db.t2.micro or db.t3.micro instance with the Free Tier limits. 

Choosing the Free Tier ensures that you are within the free usage limits, including: 

   - 750 hours per month of db.t2.micro or db.t3.micro instance usage. 

   - 20 GB of storage for the database. 

   - 20 GB of automated backups storage. 

<img src="https://bitbucket.org/ivorsource/RDS/raw/d0733f5be3078ac4555eefe1aca0e811842a1b04/Pictures/Selecting%20UseCase.png">

### **6. Configure Database Settings** 

- **DB instance identifier:** Give your instance a unique name (e.g., mydb-instance). This will be the name you use to identify your database in the AWS Management Console. 

- **Master username:** This is the admin username for the database. For PostgreSQL, this could be something like postgres. 

- **Master password:** Create a strong password for your master user. This will be used to access the database. Confirm the password by typing it again.

<img src="https://bitbucket.org/ivorsource/RDS/raw/d0733f5be3078ac4555eefe1aca0e811842a1b04/Pictures/Database%20settings.png">

### **7. Choose DB Instance Class** 

- Under **DB instance class**, choose db.t2.micro or db.t3.micro. These are eligible for the Free Tier and are the smallest instance types offered by AWS. 

- **Storage:** Set the storage to 20 GB (this is the Free Tier limit). Ensure that you are using General Purpose (SSD) storage, as this is what the Free Tier covers. 

### **8. Configure Connectivity** 

- **Virtual Private Cloud (VPC):** Select the default VPC or create a new one if necessary.  

- **Public accessibility:** Select Yes if you want the database to be publicly accessible (i.e., you need to connect to the database from outside AWS). If you’re just using the database from within the same VPC (internal-only use), select No. 

- **VPC security groups:** You can use the default security group or create a new one to specify which IP addresses or network ranges can access your database. 

<img src="https://bitbucket.org/ivorsource/RDS/raw/d0733f5be3078ac4555eefe1aca0e811842a1b04/Pictures/Additional%20Configuration.png">

### **9. Set Backup and Maintenance Options** 

- **Backup:** By default, the backup retention period is set to 7 days, which means AWS will keep backups of your database for 7 days. You can adjust this if needed, but ensure you’re staying within the Free Tier limits of 20 GB of backup storage. 

- **Enable encryption:** Encryption is optional, and you can enable it if required. However, it's not typically necessary for smaller Free Tier setups. 

- **Maintenance window:** Choose a time window for automatic maintenance to occur (e.g., when you expect the least traffic). AWS will automatically apply updates and patches during this time. 

### **10. Review and Launch** 

Once you've configured all settings, review them to ensure everything is correct. 

Ensure the instance type is set to db.t2.micro or db.t3.micro. 

- Check the storage is set to 20 GB. 

- Verify the Free Tier use case is selected. 

- Click Create database to launch your RDS instance. AWS will begin provisioning the instance, and this may take a few minutes. 

 

### **11. Connect to the PostgreSQL Database**

After your PostgreSQL RDS instance is created, you'll need to connect to it using a PostgreSQL-compatible client. Here’s how to connect: 

**a) Find the Endpoint** 

Go to the RDS Console → Databases. 

Click on your PostgreSQL instance. 

Under the Connectivity & security tab, locate the Endpoint (e.g., mydb-instance.cxjzy123xyz.us-west-1.rds.amazonaws.com). This is the host address of your RDS instance.

<img src="https://bitbucket.org/ivorsource/RDS/raw/d0733f5be3078ac4555eefe1aca0e811842a1b04/Pictures/RDS%20Endpoint.png">

**b) Use a PostgreSQL Client to Connect** 

You can use any PostgreSQL client, such as pgAdmin, DBeaver, or the psql command-line tool. 


If you prefer a GUI like pgAdmin, you can connect using the following steps: 

**1.** Open pgAdmin and click on Add New Server.

**2.** In the General tab, give the connection a name (e.g., My RDS PostgreSQL). 


**3.** In the Connection tab, provide the following details: 


 - **Host name/address:** Enter the Endpoint from your RDS instance (e.g., mydb-instance.cxjzy123xyz.us-west-1.rds.amazonaws.com). 

 - **Port:** The default PostgreSQL port is 5432. 

 - **Maintenance database:** Use postgres (or the name of the database you created). 

 - **Username:** Use the master username you created during setup. 

 - **Password** Enter the master password you set up during creation. 
	  
		

**4.** Click Save to connect. 

Now you should be able to access and manage your PostgreSQL database through pgAdmin. 

## Steps to Enable SSL Mode in pgAdmin 4

Go to pgAdmin 4 → Select Server → Click Properties → Navigate to Parameters tab → Set **sslmode** to require → Click Save → Reconnect to apply changes.

<img src="https://bitbucket.org/ivorsource/RDS/raw/175db0f71c29a7a96115874ebe497982ec649135/Pictures/PgAdmin.png">
<br>
<br>
<br>


# To create an Amazon RDS database instance on the AWS Free Tier using the AWS CLI, follow these steps:

**Step 1:** Install & Configure AWS CLI (If Not Installed)
If you haven't set up the AWS CLI, install it and configure it with your credentials:

- 1. **Install AWS CLI**: Download and install from [AWS CLI Download](https://aws.amazon.com/cli/)

- 2. **Configure AWS CLI:** aws configure

                   Enter:
                   AWS Access Key
                   AWS Secret Key
                   Region (e.g., us-east-1)
                   Output format (default is json)
                   
**Step 2:** Create an RDS Instance (Free Tier),
Run the following command to create a PostgreSQL database instance under the Free Tier:

                aws rds create-db-instance \
    --db-instance-identifier mypgfreedb \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --allocated-storage 20 \
    --master-username adminuser \
    --master-user-password MySecurePassword123 \
    --backup-retention-period 7 \
    --availability-zone us-east-2a \
    --publicly-accessible \
    --no-multi-az \
    --storage-type gp2 \
    --db-name mypgdatabase \
    --port 5432 \
    --vpc-security-group-ids sg-xxxxxxxx \
    --region us-east-2

                      
**Parameters Explained**

    --db-instance-identifier → Unique name for the DB instance
    --db-instance-class → db.t3.micro (Free Tier eligible)
    --engine → Database engine (mysql, postgres, mariadb)
    --allocated-storage → 20 GB (Free Tier limit)
    --master-username → Admin username
    --master-user-password → Admin password
    --availability-zone → AWS region availability zone
    --publicly-accessible → Allow external connections
    --no-multi-az → Single availability zone (Free Tier)
    --storage-type → gp2 (SSD storage)
    --db-name → Database name
    --port → Default MySQL port 3306
    --vpc-security-group-ids → Replace with your Security Group ID
    
**Step 3:** Verify Database Creation

          aws rds describe-db-instances --db-instance-identifier myfreedb
          
Look for "DBInstanceStatus": "available" to confirm successful creation.

**Step 4:** Connect to PostgreSQL RDS
Once the RDS instance is available, retrieve the endpoint:

     aws rds describe-db-instances --query "DBInstances[0].Endpoint.Address" --output text
     
Connect using psql (PostgreSQL CLI):

    psql -h mypgfreedb.xxxxx.us-east-2.rds.amazonaws.com -U adminuser -d mypgdatabase
    
Enter the password when prompted.





