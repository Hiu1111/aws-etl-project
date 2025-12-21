from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark.sql.functions import col

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

df = spark.read.option("header", "true").csv(
    "s3://etl-raw-data-123/sales/"
)

df_clean = (
    df.dropna()
      .withColumn("amount", col("amount").cast("double"))
      .withColumn("tax", col("amount") * 0.1)
)

df_clean.write.mode("overwrite").parquet(
    "s3://etl-processed-data-123/sales/"
)
