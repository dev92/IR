__author__ = 'Dev'

import elasticsearch
import json
import timeit
import threading
import os

vocab = {}

def get_length(es,start,end,document_lengths):
    es.indices.refresh(index="spam-filter")
    for i in range(start, end):
        total = 0
        res = es.termvector(index="spam-filter",doc_type="email",id=i,body={
             "fields" : ['text'],
                    "offsets" : False,
                    "payloads" : False,
                    "positions" : False,
                    "term_statistics" : True,
                    "field_statistics" : False
                })
        if res['term_vectors']:
            terms = res['term_vectors']['text']['terms']
            for term in terms:
                total = total+terms[term]['term_freq']
        else:
            total = total + 0
        document_lengths[i] = total



if __name__ == '__main__':

    for file in os.listdir("."):
        if file.endswith(".json"):
            os.remove(file)



    document_lengths1={}
    document_lengths2={}
    document_lengths3={}
    document_lengths4={}
    document_lengths5={}

    es1 = elasticsearch.Elasticsearch()
    es2 = elasticsearch.Elasticsearch()
    es3 = elasticsearch.Elasticsearch()
    es4 = elasticsearch.Elasticsearch()
    es5 = elasticsearch.Elasticsearch()


    t1 = threading.Thread(target=get_length,args = (es1,1,20001,document_lengths1))
    t2 = threading.Thread(target=get_length,args = (es2,20001,40001,document_lengths2))
    t3 = threading.Thread(target=get_length,args = (es3,40001,60001,document_lengths3))
    t4 = threading.Thread(target=get_length,args = (es4,60001,80001,document_lengths4))
    t5 = threading.Thread(target=get_length,args = (es5,80001,84679,document_lengths5))

    start_time  = timeit.default_timer()

    print "Calculating document lengths..."

    t1.start();t2.start();t3.start();t4.start();t5.start()

    t1.join();t2.join();t3.join();t4.join();t5.join()

    document_lengths1.update(document_lengths2)
    document_lengths1.update(document_lengths3)
    document_lengths1.update(document_lengths4)
    document_lengths1.update(document_lengths5)

    totallength = 0

    for key in document_lengths1:
        totallength+=document_lengths1[key]

    document_lengths1["total_length"] = totallength
    document_lengths1["avg_length"] = totallength/84678.0

    with open("document_lengths.json",'w') as output:
        json.dump(document_lengths1,output)

    print "Document File Generated!"

    print "Time Taken(mins):",(timeit.default_timer()-start_time)/60








