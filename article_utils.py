import urllib
from bs4 import BeautifulSoup
from feed import NewsAPICalls
from database import threadDatabase
import uuid
import pprint
from database import threadDatabase
import threading
import re
import numpy as np
import pandas as pd
from pprint import pprint
import urllib
from bs4 import BeautifulSoup
from pymongo import MongoClient
import uuid
from multiprocessing import Process, freeze_support
# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import LdaModel
from gensim.models import CoherenceModel
import spacy
# Plotting tools
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt

from config import threadConfiguration
from bson import json_util
import jsonify

import uuid
import json
# import logging
import certifi
configFile = threadConfiguration()

database = threadDatabase(configFile)
appFeed = NewsAPICalls(configFile.get_configuration())
database_client = threadDatabase(configFile.get_configuration())
# appFeed = NewsAPICalls(configFile.get_configuration())
# database_client = threadDatabase(configFile.get_configuration())
# %matplotlib inline

# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

from nltk.corpus import stopwords
nlp = spacy.load("en_core_web_sm")
# 5 Prepare stop words 
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

def make_bigrams(texts,bigram_mod):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts,bigram_mod,trigram_mod):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]


def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

def get_article_text(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html)

    # kill all script and style elements
    for script in soup(["script", "style","nav","li",'header','meta','footer',]):
        script.extract()

        # get text
    #text = soup.get_text()
    text = soup.find_all(text=True)
    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'scripts',
        'style',
        'nav',
        'li'
        
    ]

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    words = output.split(' ')
    words = list(filter(lambda x: len(x)<20, words))
    words = list(map(lambda x: x.lower().replace(',','').strip(),words))
    text = ' '.join([word for word in words])
    return text


def get_data_db(topic):
    df.head()
    # Convert to list
    data = df.content.values.tolist()[:4]
    #7
    # Remove Emails
    data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]

    # Remove new line characters
    data = [re.sub('\s+', ' ', sent) for sent in data]

    # Remove distracting single quotes
    data = [re.sub("\'", "", sent) for sent in data]

def get_data():
    """gets da"""
    df = pd.read_json('https://raw.githubusercontent.com/selva86/datasets/master/newsgroups.json')
    print(df.target_names.unique())
    df.head()
    # Convert to list
    data = df.content.values.tolist()[:4]
    #7
    # Remove Emails
    data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]

    # Remove new line characters
    data = [re.sub('\s+', ' ', sent) for sent in data]

    # Remove distracting single quotes
    data = [re.sub("\'", "", sent) for sent in data]

    pprint(data[:1])
    return data




def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))


def run():
    data = get_data()
    data_words = list(sent_to_words(data))

    print(data_words[:1])
    # Build the bigram and trigram models
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)  

    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)
    # Remove Stop Words
    print(type(data_words))
    data_words_nostops = remove_stopwords(data_words)

    # Form Bigrams
    data_words_bigrams = make_bigrams(data_words_nostops,bigram_mod)

    # Initialize spacy 'en' model, keeping only tagger component (for efficiency)
    # python3 -m spacy download en
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

    # Do lemmatization keeping only noun, adj, vb, adv
    data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

    print(data_lemmatized[:1])
    # See trigram example
    print(trigram_mod[bigram_mod[data_words[0]]])

    # Create Dictionary
    id2word = corpora.Dictionary(data_lemmatized)

    # Create Corpus
    texts = data_lemmatized

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]

    # View
    print(corpus[:1])

    # Build LDA model
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                            id2word=id2word,
                                            num_topics=20, 
                                            random_state=100,
                                            update_every=1,
                                            chunksize=100,
                                            passes=10,
                                            alpha='auto',
                                            per_word_topics=True)

    # Print the Keyword in the 10 topics
    pprint(lda_model.print_topics())
    lda_model.save("lda.model")
    doc_lda = lda_model[corpus]


    # Compute Perplexity
    print('\nPerplexity: ', lda_model.log_perplexity(corpus))  # a measure of how good the model is. lower the better.
    # Compute Coherence Score
    coherence_model_lda = CoherenceModel(model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print('\nCoherence Score: ', coherence_lda)

    # pyLDAvis.enable_notebook()
    vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
    vis
    # vis.show()
    # pyLDAvis.show(vis)
    # pyLDAvis.save_html(pyLDAvis.prepared_data_to_html(vis), 'lda.html')



if __name__ == '__main__':
    freeze_support()
    run()





