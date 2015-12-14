__author__ = 'Dev'


import json
import numpy as np
import re
from Portstemmer import PorterStemmer
import sys
import timeit
import math



temp = []
proximity = {}
alphabets = [chr(i) for i in range(97, 123)]
p = re.compile('[a-zA-Z0-9]+(\.?[a-zA-Z0-9]+)*',re.M|re.I)
st = PorterStemmer()

start_time = timeit.default_timer()

def change_word(line):
    query = []
    for word in re.finditer(p,line):
        if word.group(0) not in stop:
            query.append(word.group(0))
    return query

def create_output(qno,ranklist,filename):
    global output
    output = open(filename,'a')
    rank = 0
    for doc in ranklist:
        rank = rank + 1
        docno = doc_map[doc[0]][0]
        file_line = " ".join([qno,"Q0",docno,str(rank),str(doc[1]),"Exp\n"])
        #print file_line
        output.write(file_line)


with open("stoplist.txt") as sw:
    stop = map((lambda x:x.strip()),sw.readlines())
    stop.extend(alphabets)


with open("new_query.txt") as w:
    lines = w.readlines()

with open("./INDEX-4/document_mapping(NSST).json") as docmap:
    doc_map=json.load(docmap)



index = open("./INDEX-4/finalindex(NSST).txt")

with open("./INDEX-4/new_catalogue(NSST).json") as c:
        catalogue = json.load(c)

with open("./INDEX-4/term_mapping(NSST).json") as t:
    terms = json.load(t)

def proximity_search(positions,docno):


    B = positions

    inner_max_len = max(map(len, B))
    result = np.zeros([len(B), inner_max_len],np.int64)
    for i, row in enumerate(B):
        for j, val in enumerate(row):
            result[i][j] = val
    B = np.array(result)
    csize = B.shape[1]
    rsize = B.shape[0]


    span = []
    exhausted = []
    window = list(B[:,0])
    minelement = min(window)
    pos = window.index(minelement)
    span.append(max(window)-min(window))
    while len(exhausted)!=len(window):
        row = np.where(B==minelement)[0][0]
        col = np.where(B==minelement)[1][0]
        if col+1<csize:
            if B[row][col+1] == 0:
                exhausted.append(minelement)
                new_lst = [m for m in window if m not in exhausted]
                if len(new_lst)>0:
                    minelement = min(new_lst)
                    pos = window.index(minelement)
            else:
                window[pos] = B[row][col+1]
                span.append(max(window)-min(window))
                minelement = min([m for m in window if m not in exhausted])
                pos = window.index(minelement)
                # print window
        else:
            exhausted.append(minelement)
            new_lst = [m for m in window if m not in exhausted]
            if len(new_lst)>0:
                minelement = min(new_lst)
                pos = window.index(minelement)

        # (C - rangeOfWindow) * numOfContainTerms / (lengthOfDocument + V
    return float(((1500.0-min(span))*rsize)/float(len(terms)+doc_map[str(docno)][1]))

for line in lines:
    proximity = {}
    temp = []
    line = line.lower().split()
    query_no = line[0].strip(".")
    if line[4] =="or":
        line = " ".join(line[6:])
    else:
        line = " ".join(line[4:])
    line = change_word(line)
    print "Processing Query: ",query_no
    for word in line:
        print word
        index.seek(catalogue[str(terms[st.stem(word,0,len(word)-1)][0])])
        for dblk in index.readline().strip().split("|"):
            stats = dblk.split()
            if stats[0] not in proximity:
                proximity[stats[0]] = {}
                if query_no not in proximity[stats[0]]:
                    proximity[stats[0]][query_no] = [map(int,stats[1:])]
            else:
                proximity[stats[0]][query_no].append(map(int,stats[1:]))


    for key in proximity:
        matches = len(proximity[key][query_no])
        if matches > 1:
            proximity[key][query_no] = proximity_search(proximity[key][query_no],key)
        else:
            proximity[key][query_no] = float(((1500.0-sys.maxint)*matches)/(float(len(terms)+doc_map[key][1])))

    for key in proximity:
        temp.append((key,proximity[key][query_no]))

    create_output(query_no ,sorted(temp,key= lambda x : x[1],reverse=True)[:100],"./INDEX-4/results_Proximity(100).txt")


output.close()
print "Total Time(min(s)): ",(timeit.default_timer()-start_time)/60




