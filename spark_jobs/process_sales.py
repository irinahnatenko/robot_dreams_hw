from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("ProcessSales").getOrCreate()

# RAW → BRONZE
df_raw = spark.read.option("header", True).csv("data/raw/sales/*")
df_raw.write.mode("overwrite").parquet("data/bronze/sales/")

# BRONZE → SILVER 
df_bronze = spark.read.parquet("data/bronze/sales/")
df_silver = df_bronze \
    .withColumn("price", col("Price").cast("double")) \
    .withColumn("purchase_date", col("PurchaseDate").cast("timestamp")) \
    .withColumnRenamed("CustomerId", "client_id") \
    .withColumnRenamed("Product", "product_name") \
    .select("client_id", "purchase_date", "product_name", "price")

df_silver.write.mode("overwrite").partitionBy("purchase_date").parquet("data/silver/sales/")
