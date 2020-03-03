# services/web/server/main/views.py


try:
    from pyspark import SparkContext, SparkConf,SQLContext
    from pyspark.sql.functions import to_date,lit,desc,col
    from pyspark.sql import Row
    from operator import add
    from server.main.utils import get_requireddataframe_fromcsv
    import sys
except:
    print('error')


def create_task(words):
    conf = SparkConf().setAppName('letter count')
    sc = SparkContext(conf=conf)
    seq = words.split()
    data = sc.parallelize(seq)
    counts = data.map(lambda word: (word, 1)).reduceByKey(add).collect()
    sc.stop()
    return dict(counts)

def get_recent(spark_dataframe,given_date=None):
    result_data_frame = spark_dataframe.filter(to_date(spark_dataframe.dateAdded) == lit(given_date)).orderBy(
        spark_dataframe.dateAdded.desc()).limit(1)
    return result_data_frame

def get_brand_count(spark_dataframe,given_date=None):

    result_data_frame = spark_dataframe.filter(to_date(spark_dataframe.dateAdded) == lit(given_date)).groupBy(spark_dataframe.brand).count().orderBy(
        col('count').desc())
    return result_data_frame

def get_by_color(spark_dataframe,given_color=None):
    result_data_frame = spark_dataframe.filter(spark_dataframe.colors.contains(given_color)).orderBy(
        spark_dataframe.dateAdded.desc()).limit(10)
    return result_data_frame

def get_result(function,param=None):
    pandas_dataframe = get_requireddataframe_fromcsv('Latest_women_shoes.csv', ['id', 'brand', 'colors', 'dateAdded'])
    conf = SparkConf().setAppName('Women Catalog')
    sc = SparkContext(conf=conf)
    # df2 = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('sample.csv')
    #used pandas dataframe as using the above the file could not be located.
    sqlContext = SQLContext(sc)
    spark_dataframe = sqlContext.createDataFrame(pandas_dataframe)
    #data=spark_dataframe.select("*").toPandas()

    result_spark_dataframe=getattr(sys.modules[__name__], function)(spark_dataframe,param)

    result_python_dataframe = result_spark_dataframe.toPandas()
    result_dict = result_python_dataframe.to_dict('records')
    sc.stop()
    return result_dict

"""
    def get_brandcount(given_date='2017-03-28'):
    pandas_dataframe = get_requireddataframe_fromcsv('Latest_women_shoes.csv', ['id', 'brand', 'colors', 'dateAdded'])
    conf = SparkConf().setAppName('Women Catalog')
    sc = SparkContext(conf=conf)
    # df2 = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('sample.csv')
    # used pandas dataframe as using the above the file could not be located.
    sqlContext = SQLContext(sc)
    spark_dataframe = sqlContext.createDataFrame(pandas_dataframe)
    # data=spark_dataframe.select("*").toPandas()

    result_python_dataframe = result_spark_dataframe.toPandas()
    result_dict = result_python_dataframe.to_dict()
    return result_dict
"""




