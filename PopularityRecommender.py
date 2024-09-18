import pandas as pd  # Import pandas for data manipulation
import numpy as np  # Import numpy for numerical operationsnp


# Class for creating a popularity-based recommender system
class PopularityRecommender():
    # Constructor to initialize the dataset and weights (alpha, beta)
    def __init__(self, dataset='world-popularity.csv', alpha=0.5, beta=0.5):
        self.dataset = pd.read_csv(dataset)  # Load the dataset from a CSV file
        self.alpha = alpha  # Weight for Popularity Index
        self.beta = beta  # Weight for Average Visitors


    # Method to update alpha and beta weights
    def UpdateWeights(self, a, b):
        self.alpha = a  # Update alpha with new value
        self.beta = b  # Update beta with new value


    # Method to calculate popularity based on formula
    def CalculatePopularity(self):
        """
        Popularity Formula:
        Popularity = (((Popularity Index * Avg Visitors) + (Popularity Index * alpha) + (Avg Visitors * beta)) / mean(Popularity Index))/ Max Popularity
        """

        def CalculatePopularityScore(row):

            a = (row['Popularity Index'])*(row['Avg Visitors'])
            a += row['Popularity Index']*self.alpha
            a += row['Avg Visitors']*self.beta
            a /= np.mean(self.dataset['Popularity Index'])

            return a

        self.dataset['Popularity'] = self.dataset.apply(CalculatePopularityScore, axis=1)

        def NormalizePopularity(row):
            return row['Popularity'] / np.max(self.dataset['Popularity'])

        self.dataset['Popularity'] = self.dataset.apply(NormalizePopularity, axis=1)


    def recommend(self):
        self.CalculatePopularity()

        return self.dataset[['ID', 'Country', 'Popularity']]


if __name__ == '__main__':
    PR = PopularityRecommender()
    print(PR.Recommend())