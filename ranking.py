import json
import os
from math import log10, floor
import numpy
from cosine_similarity import cosine_similarity

os.chdir("jsonFiles")

f = open('doc_vectors.json','r')
doc_vectors = json.load(f)
f.close()

f = open('query_vectors.json','r')
query_vectors = json.load(f)
f.close()

f = open("relevance_feedback.json", 'r')
relevance_feedback = json.load(f)
f.close()

def round_to_1(x):
    return round(x, -int(floor(numpy.log10(x, where = x >0))))


def get_ranking():
    ranking = dict()
    for query in query_vectors.keys():
        similarity = dict()
        for doc in doc_vectors.keys():
            if(query in relevance_feedback.keys() and doc in relevance_feedback[query].keys() and relevance_feedback[query][doc] > 0):
                similarity[str(doc)] = cosine_similarity(query_vectors[query], doc_vectors[doc]) + log10((relevance_feedback[query][doc])) 
            else:
                similarity[str(doc)] = cosine_similarity(query_vectors[query], doc_vectors[doc])
        final_similarity =  dict(sorted(similarity.items(), key = lambda x : x[1], reverse = True))
        ranking[query] = (list(final_similarity.keys())[:10])
        
    with open('ranking.json', 'w', encoding='utf-8') as file:
        json.dump(ranking, file, indent=4)
        file.close()
  
get_ranking()