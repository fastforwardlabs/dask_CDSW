import os
import numpy as np
import pandas as pd
import namegenerator 

from explainer.utils import data_dir
from explainer.data import utils

S3_BUCKET = "s3a://ml-field/demo/wine/"
S3_BUCKET_REGION = "us-west-2"

idcol = 'ranName'
labelcol = 'Quality'
cols = (('fixedAcidity', False),
        ('volatileAcidity', False),
        ('citricAcid', False),
        ('residualSugar', False),
        ('chlorides', False),
        ('freeSulfurDioxide', False),
        ('totalSulfurDioxide', False),
        ('density', False),
        ('pH', False),
        ('sulphates', False),
        ('Alcohol', False))


def drop_missing(df):
    '''Remove rows with missing values'''
    return df.replace(r'^\s$', np.nan, regex=True).dropna()

def clean(df):
    # recode "1" as Excellent quality
    return df.Quality.replace('1',"Excellent",inplace=True)

def load_dataset():
    '''Return Wines and labels.'''
    col_Names=[i[0] for i in cols]
    col_Names.append(labelcol)
    
    from pyspark.sql import SparkSession
    from pyspark.sql.types import Row, StructField, StructType, StringType, IntegerType

    spark = SparkSession.builder\
        .appName("Import Wine Table")\
        .config("spark.yarn.access.hadoopFileSystems",S3_BUCKET)\
        .config("spark.hadoop.fs.s3a.s3guard.ddb.region", S3_BUCKET_REGION)\
        .getOrCreate()

    df = spark.sql("SELECT * FROM `default`.`wine`").toPandas()
    spark.stop()
    
    df = drop_missing(df).reset_index()
    df.index.name = 'id'
    clean(df)
    #Add a (random) wine label name in order to have an identifier
    df['ranName'] = df.index.to_series().map(lambda x: namegenerator.gen())
    features, labels = utils.splitdf(df, labelcol)
    features = utils.drop_non_features(features, cols)
    features = utils.categorize(features, cols)
    #labels = pd.Categorical(labels)
    return features, labels
