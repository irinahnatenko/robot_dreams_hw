
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ProcessCustomers").getOrCreate()

base_path = "/home/jovyan/data"

# RAW → BRONZE
df_raw = spark.read.option("header", True).option("recursiveFileLookup", "true").csv(f"{base_path}/raw/customers/")
df_raw.write.mode("overwrite").parquet(f"{base_path}/bronze/customers/")

# BRONZE → SILVER
df_bronze = spark.read.parquet(f"{base_path}/bronze/customers/")

df_silver = df_bronze \
    .withColumnRenamed("CustomerId", "client_id") \
    .withColumnRenamed("FirstName", "first_name") \
    .withColumnRenamed("LastName", "last_name") \
    .withColumnRenamed("Email", "email") \
    .withColumnRenamed("RegistrationDate", "registration_date") \
    .withColumnRenamed("State", "state")

df_silver.write.mode("overwrite").parquet(f"{base_path}/silver/customers/")
