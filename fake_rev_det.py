import pickle
import xgboost as xgb
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def transform_text(text):
    import nltk
    import string
    from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer
    ps = PorterStemmer()
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))
    
    return " ".join(y)

def pred(text):
    import nltk
    with open('model.pkl', 'rb') as f:
        fake_detect_model = pickle.load(f)

    df = pd.DataFrame()
    df['text'] = text
    df['num_characters'] = df['text'].apply(len)
    df['num_words'] = df['text'].apply(lambda x:len(nltk.word_tokenize(x)))
    df['num_sentences'] = df['text'].apply(lambda x:len(nltk.sent_tokenize(x)))
    df['transformed_text'] = df['text'].apply(transform_text)
    tfidf = TfidfVectorizer(max_features=3000)
    X = tfidf.fit_transform(df['transformed_text']).toarray()
    predicted = fake_detect_model.predict(X)
    decode_label = {0 : "computer generated" , 1 : "orignal"}
    return decode_label[predicted]



