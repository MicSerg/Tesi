from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from autocorrect import Speller
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
from multiprocessing import Pool


def parallelize_dataframe(df, func):
    df_split = np.array_split(df, 2)
    pool = Pool(4)
    x = pool.map(func, df_split)
    df = pd.concat(x)
    pool.close()
    pool.join()
    return df


def text_processed(df, text_stem, index):
    df["processed_text"][index] = text_stem


def compound_logic(compound):
    sentiment = ''
    if compound <= -0.050:
        sentiment = 'negative'
        return sentiment
    else:
        sentiment = 'positive'
        return sentiment


def vader_sentiment(df, sentiment, index):
    df["vader_sentiment"][index] = sentiment


def analyze_df(df):
    pd.set_option('mode.chained_assignment', None)
    for index, row in enumerate(df['text']):
        print(index)
        spell = Speller(fast=True)
        ps = PorterStemmer()
        analyzer = SentimentIntensityAnalyzer()
        tokenize_value = []

        text_spell = spell(str(row))

        words = word_tokenize(text_spell)

        for idx, w in enumerate(words):
            tokenize_value.append(ps.stem(w))
            next_odd = len(words) - 1
            if next_odd == idx:
                text_stem = " ".join([str(elem) for elem in tokenize_value])

                vs = analyzer.polarity_scores(text_stem)

                text_processed(df, text_stem, index)

                compound = vs['compound']
                sentiment = compound_logic(compound)

                vader_sentiment(df, sentiment, index)

    return df


if __name__ == '__main__':
    reviews_df = pd.read_csv('data/processed/recensioniRange.csv', delimiter=';', low_memory=False)
    reviews_df['processed_text'] = ''
    reviews_df['vader_sentiment'] = ''

    review = parallelize_dataframe(reviews_df, analyze_df)
    review = analyze_df(reviews_df)

    review.to_csv("data/processed/recensioniRange.csv", sep=";", index=False)
