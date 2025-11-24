from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import os
def run_spark_job():
    spark = SparkSession.builder\
                        .appName("DailySalesProcessor")\
                        .master("local[*]")\
                        .getOrCreate()
    input_file = "/opt/airflow/data/incoming/sales_data.csv"
    output_folder = "/opt/airflow/data/processed/sales_report"

    if not os.path.exists(input_file):
        print(f"ERROR: File not found at {input_file}")
        return
    
    # READ
    print(f"Reading data from {input_file}")
    df = spark.read.format("csv")\
                .option("header", True)\
                .option("inferSchema", True)\
                .load(input_file)
    
    # TRANSFORM
    df_transformed = df.withColumn("total_amount", col("quantity") * col("price"))

    df_transformed.show()

    # LOAD
    print(f"Saving data to {output_folder}")
    df_transformed.write.format("csv")\
                        .mode("overwrite")\
                        .option("header", True)\
                        .save(output_folder)


    print("--- Job Finished Successfully ---")
    spark.stop()

if __name__ == "__main__":
    run_spark_job()
