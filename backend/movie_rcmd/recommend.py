import os
from pyspark.sql import SparkSession

MONGODB_URI = 'mongodb://node1:27017,node2:27017,node3:27017,node4:27017/?replicaSet=mongorepl'

def main():
    spark = SparkSession.builder\
        .master('yarn') \
        .appName('Movie Recommendation') \
        .config('spark.mongodb.input.uri', MONGODB_URI) \
        .config('spark.mongodb.output.uri', MONGODB_URI) \
        .config('spark.yarn.archive', 'hdfs:///home/spark_jars.zip') \
        .getOrCreate()
    sc = spark.sparkContext

    print('started!')

    true_ratings_df = spark.read.format('mongo') \
        .option('database', 'rcmd_db') \
        .option('collection', 'movie_rcmd_rating') \
        .load() \

    true_ratings_df.write.format('mongo').mode('overwrite') \
        .option('database', 'rcmd_db') \
        .option('collection', 'movie_rcmd_rating') \
        .save()

    virtual_ratings_rdd = spark.read.csv("hdfs:///home/ratings.csv", header=True).rdd
    virtual_ratings_rdd.saveAsTextFile('hdfs:///home/virtual_ratings')

    spark.stop()

if __name__ == '__main__':
    main()
