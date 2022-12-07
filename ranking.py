import json
import os
import math

from cosine_similarity import cosine_similarity

os.chdir("jsonFiles")

f = open('doc_vectors.json','r')
doc_vectors = json.load(f)
f.close()

f = open('query_vectors.json','r')
query_vectors = json.load(f)
f.close()

def get_ranking():
    for query in query_vectors.keys():
        for doc in doc_vectors.keys():
            similarity = cosine_similarity(query, doc)