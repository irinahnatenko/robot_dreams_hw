from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("ProcessSales").getOrCreate()

base_path = "/home/jovyan/data"

# RAW → BRONZE
df_raw = spark.read.option("header", True).option("recursiveFileLookup", "true").csv(f"{base_path}/raw/sales/")
df_raw.write.mode("overwrite").parquet(f"{base_path}/bronze/sales/")

# BRONZE → SILVER 
df_bronze = spark.read.parquet(f"{base_path}/bronze/sales/")
df_silver = df_bronze \
    .withColumn("price", col("Price").cast("double")) \
    .withColumn("purchase_date", col("PurchaseDate").cast("timestamp")) \
    .withColumnRenamed("CustomerId", "client_id") \
    .withColumnRenamed("Product", "product_name") \
    .select("client_id", "purchase_date", "product_name", "price")

df_silver.write.mode("overwrite").parquet(f"{base_path}/silver/sales/")
