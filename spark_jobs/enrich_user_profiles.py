from pyspark.sql import SparkSession
from pyspark.sql.functions import split, trim, col, coalesce

spark = SparkSession.builder.appName("EnrichUserProfiles").getOrCreate()

base_path = "/home/jovyan/data"

df_silver = spark.read.parquet(f"{base_path}/silver/customers/")

df_profiles_raw = spark.read.option("multiline", "false").json(f"{base_path}/raw/user_profiles/user_profiles.json")

df_profiles = df_profiles_raw \
    .withColumn("first_name", trim(split(col("full_name"), " ").getItem(0))) \
    .withColumn("last_name", trim(split(col("full_name"), " ").getItem(1)))

df_enriched = df_silver.alias("silver").join(
    df_profiles.alias("profile"),
    on=[
        col("silver.first_name") == col("profile.first_name"),
        col("silver.last_name") == col("profile.last_name")
    ],
    how="left"
).select(
    col("silver.Id").alias("client_id"),
    coalesce(col("silver.first_name"), col("profile.first_name")).alias("first_name"),
    coalesce(col("silver.last_name"), col("profile.last_name")).alias("last_name"),
    col("silver.email"),
    col("silver.registration_date"),
    coalesce(col("silver.state"), col("profile.state")).alias("state")
)

df_enriched.write.mode("overwrite").parquet(f"{base_path}/gold/user_profiles_enriched/")