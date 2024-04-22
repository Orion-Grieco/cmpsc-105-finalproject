import random
import spacy #type: ignore
import nltk
import nltk.data
from nltk.corpus import treebank
import os
import re
import pandas as pd
from glob import glob
from bs4 import BeautifulSoup as beau
nlp = spacy.load("en_core_web_sm")

# Creating stopword list:       
stopwords = spacy.lang.en.stop_words.STOP_WORDS

data_folder = "PMC001xxxxxx/"
comparison_text = input("Enter text to compare to the article: ")
print(len(comparison_text.split())/2)
"""
for word in comparison_text.split():
    print(word)
"""

pruned_texts = []
found_score = 0

    
for filename in os.scandir(data_folder):
    #print(filename)
    #file_path = os.path.join(data_folder, filename)

    open_file = open(filename.path, 'r+', encoding = "utf-8")
    open_file = re.sub(u"[^\x01-\x7f]+",u"",open_file.read())

    pmid_soup = beau(open_file,'lxml')
    
    for word in comparison_text.split():
        if word in open_file:
            found_score += 1
            if found_score >= len(comparison_text.split())/2:
                pruned_texts.append(str(pmid_soup.find('pmid'))[1:-1])

print(pruned_texts)
#return(pruned_texts)