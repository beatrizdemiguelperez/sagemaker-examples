
import pandas as pd
import numpy as np
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

def sentiment_nltk(text):
    result = sid.polarity_scores(text)
    return pd.Series(result)
    
def nltk_dataframe(df):    
    out = df["sentences"].apply(lambda x: sentiment_nltk(x))
    df["sentiment_nltk_pos"] = out['pos']
    df["sentiment_nltk_neg"] = out['neg']
    df["sentiment_nltk_neu"] = out['neu']
    df["sentiment_nltk_compound"] = out['compound']
    df["sentiment_nltk_parsed"] = np.select([out["compound"] <= 0, out["compound"] == 0, out["compound"] > 0], ['neg', 'neu', 'pos'])

