import os
import json
import numpy
from math import log10, floor

def round_to_1(x):
    return round(x, -int(floor(numpy.log10(x, where = x >0))))


os.chdir("jsonFiles")

f = open('ranking.json')
ranking = json.load(f)
f.close()

f = open('relevance_feedback.json', "r")
relevance_feedback = json.load(f)
f.close()


eval = [0, 1, 1, 1, 0, 0, 1, 1, 0, 0]

print("Give input as 1 if Relevant doc and 0 if non Relevant doc for the retrievd Documents : ")

total_relevant = 0

evaluation = dict()

for j in list(ranking.values())[0]:
    i = int(input("Doc id : " + j + " - "))
    if i == 1:
        total_relevant+=1
        evaluation[j] = 1
    else:
        evaluation[j] = 0


if(list(ranking.keys())[0] in relevance_feedback.keys()):
    existing_rel_feedback = relevance_feedback[list(ranking.keys())[0]]
    for i in existing_rel_feedback.keys():
        existing_rel_feedback[i]+=evaluation[i]
    relevance_feedback[(list(ranking.keys())[0])] = dict(existing_rel_feedback.items())
    
else:
    relevance_feedback[(list(ranking.keys())[0])] = dict(evaluation.items())    

with open("relevance_feedback.json", "w", encoding='utf-8') as file:
    json.dump(relevance_feedback, file, indent=4)
    file.close()

relevant = 0
retrieved = 0

# print(list(evaluation.values()))

for i in list(evaluation.values()):
    retrieved += 1
    if i == 1:
        opinion = "R "
        relevant += 1
    else: 
        opinion = "NR"
    print(opinion, "Precision : ", round_to_1(relevant / retrieved), "\t\tRecall : ", round_to_1(relevant / total_relevant))

print("\nRelevant docs retrieved : ", relevant)
print("Total no of relevant docs: ", total_relevant)
print("Total no of documents retrieved : ", retrieved)



