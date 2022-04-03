import configparser

#Importing from the config file(dwh.cfg)
config = configparser.ConfigParser()
config.read('dwh.cfg')



# DROP ALL TABLES
staging_user_table_drop = "DROP TABLE IF EXISTS staging_user"
dim_user_info_table_drop = "DROP TABLE IF EXISTS dim_user_info"
dim_gender_info_table_drop = "DROP TABLE IF EXISTS dim_gender_info"
fact_user_table_drop = "DROP TABLE IF EXISTS fact_user"



# CREATE TABLES(staging)
staging_user_table_create = (

    """CREATE TABLE IF NOT EXISTS staging_user ( 
         id  int, 
         first_name varchar, 
         last_name varchar, 
         email varchar, 
         gender varchar, 
         ip_address varchar )"""

)

# CREATE TABLES( dimensions )

dim_user_info_table_create = (

    """CREATE TABLE IF NOT EXISTS dim_user_info ( 
         user_id int primary key generated always as identity,
         id  int, 
         first_name varchar, 
         last_name varchar, 
         email varchar, 
         ip_address varchar )"""

)


dim_gender_info_table_create = (

    """CREATE TABLE IF NOT EXISTS dim_gender_info ( 
         gender_id int primary key generated always as identity,
         gender varchar )"""

)


# CREATE TABLES( facts )
fact_table_create = (

    """CREATE TABLE IF NOT EXISTS fact_user ( 
         fact_id int IDENTITY(0,1) PRIMARY KEY,
         id  int, 
         gender_id int )"""
)




#===================================================================

# INSERT TABLES( DIMENSIONS )
dim_user_info_table_insert = ("""
    Insert into dim_user_info( id, first_name , last_name , email, ip_address ) 
    select 
           id, 
           first_name, 
           last_name, 
           email, 
           ip_address
    from staging_user
    Where id IS NOT NULL;
""")

dim_gender_info_table_insert = ("""
    Insert into dim_gender_info( gender ) 
    select 
           distinct(gender)
    from staging_user
    Where id IS NOT NULL;
""")



#===================================================================

# INSERT TABLES( FACT  )
fact_table_insert = ("""
    Insert into fact_user( id, gender_id ) 
    SELECT
         su.id,
         dg.gender_id	
    from staging_user su inner join dim_gender_info dg on su.gender = dg.gender
""")



#===================================================================


# STAGING TABLES
# COPY command is used to copy the data from S3 buckets into staging table.

staging_events_copy = ("""
    COPY dev1.public.staging_user FROM 's3://user-test-sfl-1/DATA-1.csv' 
    IAM_ROLE 'arn:aws:iam::224124769737:role/myRedshiftRole' 
    FORMAT AS CSV DELIMITER ',' 
    QUOTE '"' 
    REGION AS 'us-west-2'
    STATUPDATE OFF
    COMPUPDATE OFF
""")


#===================================================================


# QUERY LISTS
create_table_queries = [ staging_user_table_create  , dim_user_info_table_create , dim_gender_info_table_create , fact_table_create ]

drop_table_queries = [ staging_user_table_drop , dim_user_info_table_drop , dim_gender_info_table_drop , fact_user_table_drop ]

insert_table_queries = [ dim_user_info_table_insert ,  dim_gender_info_table_insert , fact_table_insert ]

copy_table_queries = [ staging_events_copy ]