import json
import os
import math

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

ps = PorterStemmer()

stopwords = set(stopwords.words('english'))

os.chdir("jsonFiles")

f = open('positional_index.json', 'r')
positional_index = json.load(f)
f.close()

n = int(input('Enter the Previously entered value of n: '))

f = open(str(n)+'-gram-permuterms.json', 'r')
permuterms = json.load(f)
f.close

f = open('idf_values.json','r')
idf_values = json.load(f)
f.close()


print('System allows use of wildcard queries with *')

plainquery = input('Enter the query:')
query = plainquery.split(' ')


# Functions

def merge(n1, n2):
    s1 = set(n1)
    s2 = set(n2)
    return list(s1.intersection(s2))

def processing(word): 
    if n >= len(word): 
        return permuterms[word]
    else: 
        output = []
        for i in range(0, len(word)-n+1):
            if i == 0:
                output = permuterms[word[i:i+n]]
            else: 
                output = merge(output, permuterms[word[i:i+n]])
        return output
    

def permuterm_of_wildcard(word): 
    if word[-1] == '*':
        w = '$' + word[0:-1]
        return processing(w)
    elif word[0] == '*':
        w = word[1:-1]+'$'
        return processing(w)
    else: 
        i = word.find('*')
        w1 = '$' + word[0:i]
        w2 = word[i+1:] + '$'
        return merge(processing(w1), processing(w2))
        



query_vector = []

permu_query_vector = dict()

permuterm_vector = list()

for word in query:
    
    word = word.lower()

    if word in stopwords:
        continue

    if '*' in word:
        words = permuterm_of_wildcard(word)
        words.sort()
        permuterm_vector = words
        query_vector.append('#')
        print(permuterm_vector)

    else: 
        if word in positional_index.keys():
            query_vector.append(word)

        print(query_vector)


try: 
    i = query_vector.index('#')
except:
    i = -1       

if i != -1:
    for j in range(len(permuterm_vector)):

        word = permuterm_vector[j]
        query_vector[i] = word

        query_str = ""
        for k in range(len(query_vector)):
            if k != len(query_vector) - 1:
                query_str += query_vector[k] + " "
            else:
                query_str += query_vector[k]
                        
        permu_query_vector[query_str] = (query_vector[:])

else: 
    permu_query_vector[plainquery] = (query_vector)
            


with open('query_info.json', 'w', encoding='utf-8') as file: 
    json.dump(permu_query_vector,file,indent=2)
    file.close()


f = open('query_info.json','r')
query_info = json.load(f)
f.close()

# Query term vectorization

def get_query_vector(query):

    query_vector = list()
    index = dict()

    for word in query:
        if word in index.keys():
            index[word] += 1 
        else: 
            index[word] = 1

    tf_query = dict()

    for word in query:
        tf_query[word] = math.log2(index[word]) + 1

    for word in sorted(positional_index.keys()):
        if word in query:
            tf_idf = tf_query[word] * idf_values[word]
            query_vector.append(tf_idf)
        else: 
            query_vector.append(0)

    return(query_vector)

def get_query_vector_matrix():

    query_vector_matrix = dict()

    for key in query_info.keys():
        query_vector_matrix[key] = get_query_vector(query_info[key])

    with open('query_vectors.json', 'w', encoding='utf-8') as file:
        json.dump(query_vector_matrix, file, indent=4)
        file.close()
    
get_query_vector_matrix()