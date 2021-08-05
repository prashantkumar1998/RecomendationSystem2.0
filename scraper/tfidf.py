import pandas as pd
from pandas.core.frame import DataFrame
from pymongo import MongoClient


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)
    return conn[db]


def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id and '_id' in df:
        del df['_id']

    return df

if __name__ == '__main__':
    df = read_mongo('dbdemo', 'news', {}, '127.0.0.1', 27017)
    df.to_csv('1.csv', index=False)

# Import Pandas
import pandas as pd

# Load Movies Metadata
metadata = pd.read_csv('1.csv')

# Print the first three rows
#metadata.head(3)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

import numpy as np
from sklearn.metrics import pairwise_distances

# Below libraries are for feature representation using sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

news_articles = pd.read_csv("1.csv")

'''#news_articles.sort_values('title',inplace=True, ascending=False)
news_articles.drop_duplicates(subset ="title",
                     keep = False, inplace = False)
print("Total number of articles after removing duplicates:", news_articles.shape[0])
print(news_articles)'''

news_articles_temp = news_articles.copy()
tfidf_headline_vectorizer = TfidfVectorizer(min_df = 0)
tfidf_headline_features = tfidf_headline_vectorizer.fit_transform(news_articles_temp['title'])
#print(tfidf_headline_features)

stop_words = set(stopwords.words('english'))
for i in range(len(news_articles_temp["title"])):
    string = ""
    for word in news_articles_temp["title"][i].split():
        word = ("".join(e for e in word if e.isalnum()))
        word = word.lower()
        if not word in stop_words:
          string += word + " "  
    news_articles_temp.at[i,"title"] = string.strip()



def tfidf_based_model(row_index, num_similar_items):
    l=[]
    couple_dist = pairwise_distances(tfidf_headline_features,tfidf_headline_features[row_index])
    indices = np.argsort(couple_dist.ravel())#[0:num_similar_items]
    #print(indices)
    '''df = pd.DataFrame({'date': news_articles['date'][indices].values,
               'headline':news_articles['title'][indices].values,
                'Euclidean similarity with the queried article': couple_dist[indices].ravel()})'''
  
    for i in indices:
        if len(l)<10:
            if news_articles['title'][i] not in l:
                l.append(news_articles['title'][i])
    
    print("="*30,"Queried article details","="*30)
    print('headline : ',news_articles['title'][indices[0]])
    print("\n","="*25,"Recommended articles : ","="*23)
    
    #print(df.iloc[1:,])
    #return df.iloc[1:,].headline
    #print(df)
    return l
#tfidf_based_model(112, 10)


 