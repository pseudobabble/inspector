#!/usr/bin/env python3
from pprint import pprint

from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

#nltk.download()


stop_words = set(stopwords.words('english'))

with open('./test-files/Biodiversity Footprint_Report_IEEP.txt', 'r') as f:
    text = f.read()

text = text.replace('.', '')

blob = TextBlob(text)


print(set(blob.noun_phrases))
