from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ProcessUserProfiles").getOrCreate()

base_path = "/home/jovyan/data"

# RAW → BRONZE
df_raw = spark.read.json(f"{base_path}/raw/user_profiles/user_profiles.json")
df_raw.write.mode("overwrite").parquet(f"{base_path}/bronze/user_profiles/")

# BRONZE → SILVER
df_bronze = spark.read.parquet(f"{base_path}/bronze/user_profiles/")
df_bronze.write.mode("overwrite").parquet(f"{base_path}/silver/user_profiles/")