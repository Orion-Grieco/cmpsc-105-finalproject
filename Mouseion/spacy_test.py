import random
import spacy #type: ignore
import nltk
import nltk.data
from nltk.corpus import treebank
import os
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as beau
nlp = spacy.load("en_core_web_sm")

# Creating stopword list:       
stopwords = spacy.lang.en.stop_words.STOP_WORDS

corpus = []
data_folder = "PMC001xxxxxx/"
filename = random.choice(os.listdir(data_folder))
file_path = os.path.join(data_folder, filename)

file = open(file_path, 'r+', encoding = "utf-8")
file = re.sub(u"[^\x01-\x7f]+",u"",file.read())
# removing stop words
filtered_text = " ".join([word for word in file.split() if word not in stopwords])

soup = beau(filtered_text, "html.parser")
for data in soup(['style', 'script']):
        data.decompose()
text = soup.get_text()

print(f"File Name and Path : {filename} : {text} + \n")
comparison_text = input("Enter text to compare to the article: ")
comparing_text_doc = nlp(comparison_text)
base_doc = nlp(text)
print(comparison_text, "<->", filename, base_doc.similarity(comparing_text_doc))



