import spacy #type: ignore
import os
import pubmed_parser
from pubmed_parser import parse_pubmed_caption
import pandas as pd
from glob import glob
from bs4 import BeautifulSoup as beau
nlp = spacy.load("en_core_web_sm")

# Creating stopword list:       
stopwords = spacy.lang.en.stop_words.STOP_WORDS

data_folder = "PMC001xxxxxx/"
comparison_text = input("Enter text to compare to the article: ")
"""
for word in comparison_text.split():
    print(word)
"""

valid = 0
invalid = 0
success = []
failure = []
for filename in os.scandir(data_folder):
    #print(filename)
    #file_path = os.path.join(data_folder, filename)

    open_file = open(filename.path, 'r+', encoding = "utf-8")
    prep_file = open_file.read()

    pmid_soup = beau(prep_file,'lxml')
    try:
        pmid_val = pubmed_parser.parse_pubmed_caption(prep_file)
    except:
        pmid_val = "Nan"
    # removing stop words
    filtered_text = " ".join([word for word in prep_file.split() if word not in stopwords])

    soup = beau(filtered_text, "html.parser")
    for data in soup(['style', 'script']):
            data.decompose()
    text = soup.get_text()

    #print(f"File Name and Path : {filename} : {text} + \n")
    pmid_val = parse_medline_grant_id(text)
    comparing_text_doc = nlp(comparison_text)
    base_doc = nlp(text)
    print(type(pmid_val), filename)
        try:
            for dict_obj in pmid_val:
        # Creating a dictionary for the similarity matrix
                temp_matrix = dict(INPUT= comparison_text,
                PMID= dict_obj["pmid"],
                SIM_SCORE = base_doc.similarity(comparing_text_doc))
                with(open("sim_matrix_results.json", "a+")) as file:
                    file.write(f"{temp_matrix}"+ "\n")
                    success.append(filename)
                    valid += 1
        except:
            failure.append(filename)
            invalid +=1
            yield
    #print(comparison_text, "<->", filename, base_doc.similarity(comparing_text_doc))
print(f"Out of {valid+invalid} files, \n {valid} were successfully parsed \n {invalid} were unable to be parsed")
with(open("data/failed_entries.txt")) as f_file:
    for item in failure:
        f_file.write(item + "\n")
with(open("data/successful_entries.txt")) as s_file:
    for item in success:
        s_file.write(item + "\n")