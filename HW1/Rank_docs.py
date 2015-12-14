__author__ = 'Dev'

import elasticsearch
from Portstemmer import PorterStemmer
import json
import timeit
from Scoring_funcs import RetrievalModels
import os






def create_output(qno,ranklist,filename):
    global output
    output = open(filename,'a')
    rank = 0
    for doc in ranklist:
        rank = rank + 1
        docno = es.get(index="ap_dataset",doc_type="documents",id=doc[0],_source_exclude="text")
        file_line = " ".join([qno,"Q0",docno['_source']['docno'],str(rank),str(doc[1]),"Exp\n"])
        #print file_line
        output.write(file_line)


def get_response(word):
    result = es.search(index="ap_dataset",doc_type="documents",body={
              "query": {
                "function_score": {
                  "query": {
                    "match": {
                      "text": word
                    }
                  },
                  "functions": [
                    {
                      "script_score": {
                        "script_id": "getTF",
                        "lang" : "groovy",
                        "params": {
                          "term": p.stem(word,0,len(word)-1),
                          "field": "text"
                        }
                      }
                    }
                  ],
                  "boost_mode": "replace"
                }
              },
              "size": 84678,
              "fields": ["stream_id"]
            })
    return result


def change_word(word):
    temp = word.strip(',.()"')
    return temp.lower()



def remove_resultfiles():
    for filename in os.listdir("."):
        if filename.startswith("results_"):
            print "Removed..",filename
            os.remove(filename)

def initialise():
    global doc_okapi,doc_bm25,doc_tfIdf,doc_jelinek,doc_laplace
    global temp_jelinek,temp_laplace,temp_bm25,temp_tfIdf,temp_okapi
    doc_okapi = dict()
    doc_tfIdf = dict()
    doc_bm25 = dict()
    doc_laplace = dict()
    doc_jelinek = dict()
    temp_okapi = []
    temp_tfIdf = []
    temp_bm25 = []
    temp_laplace = []
    temp_jelinek = []





def Rank_docs(lines):
    for line in lines:
        initialise()
        line = map(change_word,line.split())
        line = " ".join(map(lambda x: " ".join(x.split("-")),line)).split()
        query_no = line[0]
        if line[4] =="or":
            line = list(set(line[6:])-set(stop))
        else:
            line = list(set(line[4:])-set(stop))
        print "Processing Query: ",query_no
        es.indices.refresh(index="ap_dataset")
        for word in line:
            #print word

            res = get_response(word)

            hit_list = []
            if res['hits']['max_score'] == 0:
                print "zero word:",word

            df = res['hits']['total']
            terms = res['hits']['hits']
            ttf = sum([key['_score'] for key in terms])
            for hit in terms:
                doc_id = int(hit['_id'])
                if not doc_id in doc_okapi:
                    doc_okapi[doc_id]={}
                    doc_tfIdf[doc_id] = {}
                    doc_bm25[doc_id] = {}
                    doc_laplace[doc_id] = {}
                    doc_jelinek[doc_id] = {}
                    if not query_no in doc_okapi[doc_id]:
                        score = r.Okapi_Tf(hit['_score'],document_lengths[hit['_id']])
                        doc_okapi[doc_id][query_no] = [score]
                        doc_tfIdf[doc_id][query_no] = [score*r.Tf_Idf(df)]
                        doc_bm25[doc_id][query_no] = [r.Okapi_BM25(hit['_score'],df,document_lengths[hit['_id']],line.count(word))]
                        doc_laplace[doc_id][query_no] = [r.Laplace_smoothing(hit['_score'], document_lengths[hit['_id']])]
                        doc_jelinek[doc_id][query_no] = [r.Jelinek_Mercer(hit['_score'],ttf,document_lengths[hit['_id']])]

                elif not query_no in doc_okapi[doc_id]:
                    score = r.Okapi_Tf(hit['_score'],document_lengths[hit['_id']])
                    doc_okapi[doc_id][query_no] = [score]
                    doc_tfIdf[doc_id][query_no] = [score*r.Tf_Idf(df)]
                    doc_bm25[doc_id][query_no] = [r.Okapi_BM25(hit['_score'],df,document_lengths[hit['_id']],line.count(word))]
                    doc_laplace[doc_id][query_no] = [r.Laplace_smoothing(hit['_score'], document_lengths[hit['_id']])]
                    doc_jelinek[doc_id][query_no] = [r.Jelinek_Mercer(hit['_score'],ttf,document_lengths[hit['_id']])]
                else:
                    score = r.Okapi_Tf(hit['_score'],document_lengths[hit['_id']])
                    doc_okapi[doc_id][query_no].append(score)
                    doc_tfIdf[doc_id][query_no].append(score*r.Tf_Idf(df))
                    doc_bm25[doc_id][query_no].append(r.Okapi_BM25(hit['_score'],df,document_lengths[hit['_id']],line.count(word)))
                    doc_laplace[doc_id][query_no].append(r.Laplace_smoothing(hit['_score'],document_lengths[hit['_id']]))
                    doc_jelinek[doc_id][query_no].append(r.Jelinek_Mercer(hit['_score'],ttf,document_lengths[hit['_id']]))
                hit_list.append(doc_id)
            remaining_docs = list(set(docIds)-set(hit_list))
            for i in remaining_docs:
                if not i in doc_okapi:
                    doc_okapi[i]={}
                    doc_tfIdf[i] = {}
                    doc_bm25[i] = {}
                    doc_laplace[i] = {}
                    doc_jelinek[i] = {}
                    if not query_no in doc_okapi[i]:
                        doc_okapi[i][query_no] = [0]
                        doc_tfIdf[i][query_no] = [0]
                        doc_bm25[i][query_no] = [0]
                        doc_laplace[i][query_no] = [r.Laplace_smoothing(0,document_lengths[str(i)])]
                        doc_jelinek[i][query_no] = [r.Jelinek_Mercer(0,ttf,document_lengths[str(i)])]

                elif not query_no in doc_okapi[i]:
                    doc_okapi[i][query_no] = [0]
                    doc_tfIdf[i][query_no] = [0]
                    doc_bm25[i][query_no] = [0]
                    doc_laplace[i][query_no] = [r.Laplace_smoothing(0,document_lengths[str(i)])]
                    doc_jelinek[i][query_no] = [r.Jelinek_Mercer(0,ttf,document_lengths[str(i)])]

                else:
                    doc_okapi[i][query_no].append(0)
                    doc_tfIdf[i][query_no].append(0)
                    doc_bm25[i][query_no].append(0)
                    doc_laplace[i][query_no].append(r.Laplace_smoothing(0,document_lengths[str(i)]))
                    doc_jelinek[i][query_no].append(r.Jelinek_Mercer(0,ttf,document_lengths[str(i)]))

        for doc in docIds:
           temp_okapi.append((doc,sum(doc_okapi[doc][query_no])))
           temp_tfIdf.append((doc,sum(doc_tfIdf[doc][query_no])))
           temp_bm25.append((doc,sum(doc_bm25[doc][query_no])))
           temp_laplace.append((doc,sum(doc_laplace[doc][query_no])))
           temp_jelinek.append((doc,sum(doc_jelinek[doc][query_no])))

        create_output(query_no ,sorted(temp_okapi,key= lambda x : x[1],reverse=True)[:100],"results_Okapi.txt")
        create_output(query_no ,sorted(temp_tfIdf,key= lambda x : x[1],reverse=True)[:100],"results_Tf-Idf(1000).txt")
        create_output(query_no ,sorted(temp_bm25,key= lambda x : x[1],reverse=True)[:100],"results_BM25.txt")
        create_output(query_no ,sorted(temp_laplace,key= lambda x : x[1],reverse=True)[:100],"results_Laplace.txt")
        create_output(query_no ,sorted(temp_jelinek,key= lambda x : x[1],reverse=True)[:100],"results_Jelinek.txt")







if __name__ == '__main__':

    remove_resultfiles()

    document_lengths = {}
    docIds = range(1,84679)


    es = elasticsearch.Elasticsearch(timeout=200,max_retries=5)
    r = RetrievalModels()
    p = PorterStemmer()

    with open("stoplist.txt") as sw:
        stop = map((lambda x:x.strip()),sw.readlines())


    with open("document_lengths.json",'r') as f:
        document_lengths = json.load(f)

    with open("query_desc.51-100.short.txt") as w:
        lines = w.readlines()

    es.put_script(lang='groovy',id='getTF',body={
    "script": "_index[field][term].tf()"
})


    start_time = timeit.default_timer()
    es.indices.refresh(index="ap_dataset")
    Rank_docs(lines)
    output.close()
    print "Total Time(min(s)): ",(timeit.default_timer()-start_time)/60



