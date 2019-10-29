from Cases.Takeaway.Codes.TakeawayCase import PreProcessingTakeaway
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import nltk
#nltk.download('punkt') #one-time download
#nltk.download('stopwords') #one-time download
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#Question 1) What is the relation between the reviews and the helpfulness?

def CreatingDfBasedOnColumns(columns):
    helpfulness_reviews_df = df_review_combined[columns]
    return helpfulness_reviews_df

def parseStr(s):
    list = []
    s = s.replace("[", "")
    s = s.replace("]", "")
    segments = s.split(',')
    for s in segments:
        list.append(int(s.strip()))
    return list

def HavingHelpfulPercentage(helpfulness_reviews_df):
    helpfulness_reviews_df['helpful_list'] = helpfulness_reviews_df['helpful'].map(lambda name: parseStr(name))
    helpfullnessscores_df = helpfulness_reviews_df['helpful_list'].apply(pd.Series)
    mapping_columnnames = {helpfullnessscores_df.columns[0]: 'helpfulclick',
                           helpfullnessscores_df.columns[1]: 'totalclick'}
    helpfullnessscores_df = helpfullnessscores_df.rename(columns=mapping_columnnames)
    helpfullnessscores_df['helpfulclick'] = pd.to_numeric(helpfullnessscores_df['helpfulclick'])
    helpfullnessscores_df['totalclick'] = pd.to_numeric(helpfullnessscores_df['totalclick'])

    helpfulness_percentage = []

    for index, row in helpfullnessscores_df.iterrows():
        if row["totalclick"] == 0:
            helpfulness_percentage.append(0)
        else:
            per = row["helpfulclick"] / row["totalclick"] * 100
            helpfulness_percentage.append(per)

    helpfullnessscores_df['helpfulness_percentage'] = helpfulness_percentage
    helpfulness_reviews_df['helpfulness_percentage'] = helpfullnessscores_df['helpfulness_percentage']
    helpfulness_reviews_df['helpfulclick'] = helpfullnessscores_df['helpfulclick']
    helpfulness_reviews_df['totalclick'] = helpfullnessscores_df['totalclick']


def GetDistinctNonstopWordsLength(text):
    words = set(word_tokenize(text)) - set(stopwords.words('english'))  # getting important words
    length = len(words)
    return length


def CheckingCorrelations(columnnames):
    correlations = helpfulness_reviews_df[columnnames].corr()
    print(correlations)

    fig = plt.figure(figsize=[8, 6])
    ax = fig.add_subplot(111)
    cax = ax.matshow(correlations, vmin=-1, vmax=1)
    fig.colorbar(cax)
    ticks = np.arange(0, 3, 1)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(corrnames)
    ax.set_yticklabels(corrnames)
    plt.show()


if __name__ == '__main__':
    ta_data_root = "C:/Users/bengisu.oniz/PyProjects/Main/Cases/Takeaway/Data/"
    df_review_combined = PreProcessingTakeaway(ta_data_root)
    columnnames_helpfulness_reviews = ["metadataid", 'asin', 'reviewid', 'reviewerid', 'reviewername', 'helpful',
                                       "reviewtext", "overall"]
    helpfulness_reviews_df = CreatingDfBasedOnColumns(columnnames_helpfulness_reviews)
    HavingHelpfulPercentage(helpfulness_reviews_df)

    helpfulness_reviews_df['review_word_count'] = helpfulness_reviews_df['reviewtext'].map(
        lambda text: GetDistinctNonstopWordsLength(text))

    corrnames = ['helpfulness_percentage', 'overall', 'review_word_count']
    CheckingCorrelations(corrnames)


