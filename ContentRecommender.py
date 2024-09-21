import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from time import sleep as s
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

class ContentBaseRecommender:

    def __init__(self, data_file='world-countries.csv', wait_time=0.1):
        self.data = pd.read_csv(data_file)
        self.wait = wait_time
