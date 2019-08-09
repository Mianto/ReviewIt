from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import re
import pickle


def sentiment_analyzer(file_path):
    """
    Main Function for Sentiment Analysis using VaderSentiment
    """
    df = pd.read_csv(file_path, encoding="ISO-8859-1")
    analyzer = SentimentIntensityAnalyzer()

    result = {'pos': 0, 'neg': 0, 'neu': 0}

    for review in df['review'][0: 10]:
        vs = analyzer.polarity_scores(review)
        if vs['compound'] <= -0.05:
            result['neg'] += 1
        elif vs['compound'] >= 0.05:
            result['pos'] += 1
        else:
            result['neu'] += 1

    return result


def extract_bigrams():
    """
    Main Function to extract bigram according to tf-idf scores
    """

    di = {}
    corpus = create_corpus()
    stop_words = get_stop_words()
    build_count_vectorizer(corpus, stop_words)

    for i in range(len(corpus)):
        doc = corpus[i]
        tf_idf_vector=tfidf_transformer.transform(cv.transform([doc]))
        sorted_items = sort_coo(tf_idf_vector.tocoo())
        keywords = extract_topn_from_vector(feature_names, sorted_items, 5)
        di.update(keywords)





def update_corpus(corpus_file_path):
    """
    Helper function to create corpus from reviews
    """
    df = pd.read_csv(file_path, encoding="ISO-8859-1")

    for review in df['review']:
        # Remove punctuation
        text = re.sub('[^a-zA-Z]', ' ', review)

        # Convert to lowercase
        text = text.lower()

        # remove special characters and digits
        text=re.sub("(\\d|\\W)+"," ",text)

        # Convert to list from string
        text = text.split()

        corpus.append(text)

    return corpus


def get_stop_words(stop_file_path):
    """
    Helper function to load stop words from file into set
    """
    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)


def build_count_vectorizer(corpus, stop_words):
    """
    Helper function to build model and dump using pickle
    """
    cv = CountVectorizer(max_df=0.8, stop_words=stop_words, max_features=10000, ngram_range=(2, 2))
    vector_train = cv.fit_transform(corpus)
    pickle.dump(cv.vocabulary_, open('features.pkl', 'wb'))


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """
    Helper function to get the feature names and tf-idf score of top n items
    """
    #use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:

        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    #create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]

    return results