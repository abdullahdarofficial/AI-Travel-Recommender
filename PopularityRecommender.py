import pandas as pd
import numpy as np


class PopularityRecommender():
    def __init__(self, dataset='world-popularity.csv', alpha=0.5, beta=0.5):
        self.dataset = pd.read_csv(dataset)
        self.alpha = alpha
        self.beta = beta


    def UpdateWeights(self, a, b):
        self.alpha = a
        self.beta = b



if __name__ == '__main__':
    PR = PopularityRecommender()
