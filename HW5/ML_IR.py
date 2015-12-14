from __future__ import division
__author__ = 'Dev'

import os
import json
import sys
from sklearn import linear_model,svm,tree
import random


def create_output(qno,ranklist,fname):
    global output
    output = open(fname,'a')
    rank = 0
    for doc in ranklist:
        rank = rank + 1
        file_line = " ".join([qno,"Q0",doc[0],str(rank),str(doc[1]),"Exp\n"])
        output.write(file_line)

def Train_Model(train_queries):
    matrix = []
    ylabel = []
    for qid in train_queries:
        for doc in result[qid]:
            pos = qrel[qid].index(doc)
            matrix.append(result[qid][doc])
            ylabel.append(int(qrel[qid][pos+1]))
    model.fit(matrix,ylabel)



def Test_Model(test_queries):
    matrix_test = []
    for qid in test_queries:
        print "Query:",qid
        for doc in result[qid]:
            matrix_test.append(result[qid][doc])

    return model.predict(matrix_test)





def Generate_Rankfile(predicted,test_queries,fname):
    i = 0
    for qid in test_queries:
        ranks = []
        for doc in result[qid]:
            ranks.append([doc,predicted[i]])
            i+=1
        ranks = sorted(ranks,key=lambda x:x[1],reverse=True)
        create_output(qid,ranks,fname)


def Remove_existing():
    for rfile in os.listdir("."):
        if rfile.endswith("_model.txt"):
            os.remove(rfile)


def FeatureMatrix(file):
    print "Adding "+file.split("_")[1].strip(".txt")+" Scores as a feature"
    f = open("./Features/"+file)
    for query in query_ids:
        processed  = []
        if query not in result:
            result[query] = {}
        f.seek(0)
        lines = filter(lambda x: x.split()[2] in qrel[query] and x.split()[0] == query,f.readlines())
        for line in lines:
            line = line.split()
            processed.append(line[2])
            if line[2] not in result[query]:
                result[query][line[2]] = [float(line[4])]
            else:
                result[query][line[2]].append(float(line[4]))
        for i in range(0,len(qrel[query]),2):
            if qrel[query][i] not in result[query] :
                result[query][qrel[query][i]] = [-sys.maxint]
            elif qrel[query][i] not in processed:
                result[query][qrel[query][i]].append(-sys.maxint)






if __name__ == '__main__':


    Remove_existing()

    qrel_file = open("qrels.adhoc.51-100.AP89.txt")
    qrel  = {}
    queries = open("query_desc.51-100.short.txt")

    query_ids = set()
    result = {}

    for line in queries.readlines():
        query_ids.add(line.split()[0].strip("."))

    query_ids = list(query_ids)

    for line in qrel_file.readlines():
        line = line.split()
        if line[0] in query_ids and line[0] not in qrel:
            qrel[line[0]] = line[2:4]
        elif not line[0] in query_ids:
            continue
        else:
            qrel[line[0]].extend(line[2:4])

    print "Starting to Form Feature Matrix.."

    for file in os.listdir("./Features/"):
        if file.startswith("results_"):
            FeatureMatrix(file)



    # model = linear_model.LinearRegression()       # Linear Regression
    model = tree.DecisionTreeClassifier()         # Decision Tree


    print "Training Model..."



    random.shuffle(query_ids)

    Train_Model(query_ids[:20])


    print "Testing Model on Test Queries:"

    predicted = Test_Model(query_ids[20:])


    Generate_Rankfile(predicted,query_ids[20:],"test_model.txt")

    output.close()

    print "Testing Model on Trainining Queries:"

    predicted = Test_Model(query_ids[:20])


    Generate_Rankfile(predicted,query_ids[:20],"train_model.txt")

    output.close()

    print "Result files Generated!"


    with open("feature_matrix.json",'w') as fmatrix:
        json.dump(result,fmatrix)

    with open("graded_qrel.json",'w') as q:
        json.dump(qrel,q)



