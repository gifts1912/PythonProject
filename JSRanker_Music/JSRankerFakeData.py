import os
import re
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup
import nltk.data

from gensim.models.word2vec import Word2Vec

def load_dataset(name, nrows=None):
    datasets = {
        'unlabeled_train': 'unlabeledTrainData.tsv',
        'labeled_train': 'labeledTrainData.tsv',
        'test': 'testData.tsv'
    }

    if name not in datasets:
        raise ValueError(name)
    data_file = os.path.join(".", "data", datasets[name])


    df = pd.read_csv(data_file, sep = '\t', escapechar='\\', nrows=nrows)

    print("Number of reviews {}".format(df.shape[0]))
    return df

df = load_dataset('unlabeled_train')

df.head()
