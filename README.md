# Python_SFL

The diagram shown below (Diag. 1.0 ) is an accurate representation of the architecture which I used to process the data. The data is stored in S3 bucket. Further the Redshift is configured to ingest data from S3. This is done by defining the IAM Role and attaching permissions to it ( eg. AmazonS3ReadOnlyAccess). Further, a security groups needs to be created in which Inbound and Outbound rules are properly defined. Using the Security groups, access to the Redshift from remote machines can be restricted. 

For the purpose of simplicity, I have used a DC2.large 2 node cluster.

The order of operations is as follows:-

1.	Run the create_tables.py file which creates all the tables inside redshift cluster. This includes dropping all the tables (staging, fact and dimension ) if they exist and creating new ones. Sql_queries.py files contains all the Insert, Create and COPY queries. dwh.cfg file contains the AWS configurations.

2.	Then run the etl.py file where in the  data is actually ingested from S3 into Redshift. I use redshift COPY command to import data from S3 into staging table
a.	 staging_user 

3.	Further, the data is moved from the staging table into the dimension tables:-
a.	Dim_user_info
b.	Dim_gender_info

4.	Further , the fact table also gets created:-
a.	Fact_user


<img width="411" alt="Screen Shot 2022-04-03 at 12 43 15 AM" src="https://user-images.githubusercontent.com/16469133/161417051-f177d11b-4cf3-4dda-af18-734eb49fa89d.png">





<img width="769" alt="Screen Shot 2022-04-03 at 12 42 07 AM" src="https://user-images.githubusercontent.com/16469133/161417011-d97fbac7-f15a-4345-b0bb-d24bc1a22c2e.png">
