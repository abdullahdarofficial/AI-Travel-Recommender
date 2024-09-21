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

        self.data = self.process_data(self.data)
        #print(self.data)

        #print('performing vectorization...')
        #s(self.wait)

        self.tf_idf = TfidfVectorizer(stop_words='english')
        self.vec = CountVectorizer(stop_words='english')

        self.tf_idf_matrix = self.tf_idf.fit_transform(self.data['keywords'])
        self.vec_matrix = self.vec.fit_transform(self.data['keywords'])

        #print('calculating similarity...')
        #s(self.wait)

        self.cosine_sim = cosine_similarity(self.tf_idf_matrix, self.tf_idf_matrix)
        self.sim = cosine_similarity(self.vec_matrix, self.vec_matrix)


    def process_data(self, data):

        #print('processing data...')
        #s(self.wait)

        def update_keywords(row):
            keywords = str(row['keywords'])
            climate = str(row['climate'])
            if climate == 'mix':
                climate = 'cold hot'
            return keywords + ' ' + climate

        data['keywords'] = data.apply(update_keywords, axis=1)
        data.drop('climate', axis=1, inplace=True)
        data = data.drop_duplicates(subset='Country')
        data['keywords'] = data['keywords'].str.replace(r'\s+', ' ')

        #print('data processed')
        #s(self.wait)
        return data


    def get_TF_IDF_recomendation(self, keywords_matrix, budget, num_of_rec=5):

        #idx = self.data[self.data['Country'].str.lower() == country.lower()].index[0]
        self.cosine_sim = cosine_similarity(keywords_matrix, self.tf_idf_matrix)
        sim_scores = list(enumerate(self.cosine_sim[0]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        #print(sim_scores)
        country_indices = [i[0] for i in sim_scores]

        reced = 0
        recommendation = pd.DataFrame(columns=['ID', 'Country', 'Cost Per Day', 'Similarity'])


