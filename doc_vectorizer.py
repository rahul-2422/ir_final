import json
import math
import re
import os
from nltk.corpus import stopwords

stopwords = set(stopwords.words('english'))

pattern = re.compile(r'''(?x)([A-Z]\.)+|[\$|Rs]?\d+(\.\d+)?%?|\w+''', re.VERBOSE|re.I)

documents_count = (len([name 
for name in os.listdir('.\dataset') 
    if os.path.isfile(os.path.join('.\dataset', name))]))

os.chdir("jsonFiles")

f = open('positional_index.json','r')
positional_index = json.load(f)
f.close()


f = open('idf_values.json','r')
idf_values = json.load(f)
f.close()

def get_tf_values(word):

    word = positional_index[word]
    documents = word["documents"]
    
    tf_values = dict()
    
    for key in documents.keys():
    
        doc_ref = documents[key]
    
        freq = doc_ref["frequency"]
        tf_value = math.log2(freq)
        tf_values[key] = tf_value + 1
    
    return tf_values


def get_tf_idf_value(word, doc_id):

    tf_values = get_tf_values(word)

    tf_idf = tf_values[doc_id] * idf_values[word]
    
    return tf_idf


def get_doc_info(doc):

    doc_info = list()

    for word in doc:
        word = word.group()
        word = word.lower()
        if word in stopwords:
            continue
        else:
            if word in positional_index.keys():
                doc_info.append(word)
    
    return doc_info


def get_doc_vector(doc, doc_id):
    
    doc_info = get_doc_info(doc)

    vector = list()

    for word in sorted(positional_index.keys()):
        if word in doc_info:
            tf_idf = get_tf_idf_value(word, doc_id)
            vector.append(tf_idf)
        else: 
            vector.append(0)
        
    return vector


def get_doc_vector_matrix():

    os.chdir("..")
    os.chdir("dataset")
    files = os.listdir()


    doc_vector_matrix = dict()

    for i in range(0, documents_count):
        doc_id = files[i].split('.')[0]
        file = open(files[i], 'r', encoding = 'utf8')
        words = pattern.finditer(file.read())

        doc_vector_matrix[str(doc_id)] = get_doc_vector(words, doc_id)

    os.chdir("..")
    os.chdir("jsonFiles")

    with open('doc_vectors.json', 'w', encoding='utf-8') as file:
        json.dump(doc_vector_matrix, file, indent=4)
        file.close()

        
get_doc_vector_matrix()
