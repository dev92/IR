__author__ = 'Dev'

import json
from sklearn import linear_model,svm,tree

with open("feature_matrix.json") as f:
    feature = json.load(f)

with open("graded_qrel.json") as f1:
    grades = json.load(f1)

queries = open("query_desc.51-100.short.txt")

query_ids = set()
result = {}

def create_output(qno,ranklist):
    global output
    output = open("test_results.txt",'a')
    rank = 0
    for doc in ranklist:
        rank = rank + 1
        file_line = " ".join([qno,"Q0",doc[0],str(rank),str(doc[1]),"Exp\n"])
        output.write(file_line)

for line in queries.readlines():
    query_ids.add(line.split()[0].strip("."))

train_queries = sorted(list(query_ids)[:20])
test_queries = list(query_ids)[20:]

matrix = []
ylabel = []

for qid in train_queries:
    for doc in feature[qid]:
        pos = grades[qid].index(doc)
        matrix.append(feature[qid][doc])
        ylabel.append(int(grades[qid][pos+1]))


# model = linear_model.LinearRegression()

model = tree.DecisionTreeClassifier()

model.fit(matrix,ylabel)

matrix_test = []
y_test = []

for qid in test_queries:
    for doc in feature[qid]:
        matrix_test.append(feature[qid][doc])


predict = model.predict(matrix_test)
print predict

i = 0

for qid in test_queries:
    ranks = []
    for doc in feature[qid]:
        ranks.append([doc,predict[i]])
        i+=1
    ranks = sorted(ranks,key=lambda x:x[1],reverse=True)
    create_output(qid,ranks)





