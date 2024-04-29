import spacy  # type: ignore
import os
import pubmed_parser
from bs4 import BeautifulSoup as beau

nlp = spacy.load("en_core_web_sm")

# Creating stopword list:
stopwords = spacy.lang.en.stop_words.STOP_WORDS

data_folder = "data/PMC001xxxxxx"
comparison_text = input("Enter text to compare to the article: ")

temp_dict = {}
data_list = []
summative_score = 0
for filename in os.scandir(data_folder):
    prep_file = open(filename.path, "r").read()
    # pubmed_parser.parse_pubmed_caption(prep_file.read())

    # removing stop words
    filtered_text = " ".join(
        [word for word in prep_file.split() if word not in stopwords]
    )

    soup = beau(filtered_text, "html.parser")
    for data in soup(["style", "script"]):
        data.decompose()
    text = soup.get_text()

    comparing_text_doc = nlp(comparison_text)
    base_doc = nlp(text)
    # Creating a dictionary for the similarity matrix
    try:
        temp_dict = {
            "INPUT": comparison_text,
            "PMID": pubmed_parser.parse_pubmed_xml(prep_file)[0]["pmid"],  # type: ignore
            "SIM_SCORE": base_doc.similarity(comparing_text_doc),
            "SUBJECTS": pubmed_parser.parse_pubmed_xml(prep_file)[0]["subjects"],  # type: ignore
        }
    except:
        temp_dict = {
            "INPUT": comparison_text,
            "PMID": "N/A",  # pubmed_parser.parse_pubmed_caption(soup)[0]["pmid"], #type: ignore
            "SIM_SCORE": base_doc.similarity(comparing_text_doc),
            "SUBJECTS": pubmed_parser.parse_pubmed_xml(prep_file)["subjects"],  # type: ignore
        }
    summative_score += float(temp_dict["SIM_SCORE"])
    data_list.append(temp_dict)
with open("sim_matrix_results.json", "w+") as file:
    for item in data_list:
        file.write(f"{item}" + "\n")

    # print(data_list, "@")


# print(comparison_text, "<->", filename, base_doc.similarity(comparing_text_doc))
