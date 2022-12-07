import json
import os
import math

documents_count = (len([name 
for name in os.listdir('.\dataset') 
    if os.path.isfile(os.path.join('.\dataset', name))]))

os.chdir("jsonFiles")

f = open('positional_index.json','r')
positional_index = json.load(f)
f.close()


def get_idf_values():

    idf_vals = dict()

    for key in sorted(positional_index.keys()):
        reference = positional_index[key]
        occurences = reference['document_frequency']
        idf = math.log2(documents_count / occurences)
        idf_vals[key] = idf
    
    with open('idf_values.json', 'w', encoding='utf-8') as file:
        json.dump(idf_vals, file, indent=4)
        file.close()


get_idf_values()