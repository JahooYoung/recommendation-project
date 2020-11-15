from pyspark.sql import SparkSession

MONGODB_URI = 'mongodb://node1:27017,node2:27017,node3:27017,node4:27017/rcmd_db.movie_rcmd_rating?replicaSet=mongorepl'

def main():
    spark = SparkSession.builder\
        .master('yarn') \
        .appName('Movie Recommendation') \
        .config('spark.mongodb.input.uri', MONGODB_URI) \
        .config('spark.mongodb.output.uri', MONGODB_URI) \
        .config('spark.yarn.archive', 'hdfs:///home/spark_jars.zip') \
        .getOrCreate()
    # spark = SparkSession.builder\
    #     .appName('Movie Recommendation') \
    #     .config('spark.mongodb.input.uri', MONGODB_URI) \
    #     .config('spark.mongodb.output.uri', MONGODB_URI) \
    #     .getOrCreate()
    sc = spark.sparkContext

    print('===================================== started!')

    # virtual_ratings_rdd = spark.read.csv("hdfs:///home/ratings.csv", header=True).rdd
    # virtual_ratings_rdd.saveAsTextFile('hdfs:///home/virtual_ratings')

    # print('===================================== hdfs ok!')

    true_ratings_df = spark.read.format('mongo').load()
    true_ratings_df.write.format('mongo').mode('overwrite').save()

    print('===================================== mongo ok!')

    spark.stop()

if __name__ == '__main__':
    main()
