import pandas
import numpy as np

def get_requireddataframe_fromcsv(file,columns=None):
    dataframe = pandas.read_csv(file,usecols = columns)
    dataframe = dataframe.replace('', np.nan)
    dataframe = dataframe.dropna()
    dataframe = dataframe.drop_duplicates()
    return dataframe