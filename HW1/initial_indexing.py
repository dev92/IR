__author__ = 'Dev'

import json
import elasticsearch
import timeit
import os


doc_id = 0

def setup_index(client):
    client.indices.delete(index=["ap_dataset"],ignore=404)
    client.indices.create(index="ap_dataset", body={
            "settings": {
                "index": {
                    "store": {
                        "type": "default"
                    },
                    "number_of_shards": 1,
                    "number_of_replicas": 1
                },
                "analysis": {
                    "analyzer": {
                        "my_english": {
                            "type": "english",
                            "stopwords_path": "stoplist.txt"
                        }
                    }
                }
            }
        })
    client.indices.put_mapping(index="ap_dataset",doc_type="documents",body={
  "documents": {
    "properties": {
      "docno": {
        "type": "string",
        "store": True,
        "index": "not_analyzed"
      },
      "text": {
        "type": "string",
        "store": True,
        "index": "analyzed",
        "term_vector": "with_positions_offsets_payloads",
        "analyzer": "my_english"
      }
    }
  }
})


def parse(content,start,end,client):
    global doc_id
    body ={}
    for s,e in zip(start, end):
        doc_id+=1
        text =[]
        begin = [i for i in range(s+1,e) if content[i].startswith("<TEXT>")]
        fin = [i for i in range(s+1,e) if content[i].startswith("</TEXT>")]
        doc = [content[d].split()[1] for d in range(s+1,e) if content[d].startswith("<DOCNO>")]
        body["docno"] = doc[0]
        for l,k in zip(begin,fin):
            if len(content[l].strip())>6:
                text.append(content[l].strip("<TEXT>"))
            text.append("".join(content[l+1:k]))
        body["text"] = "".join(text).strip()
        client.create(index="ap_dataset",doc_type="documents",id=doc_id,body=json.dumps(body,sort_keys=True))




if __name__ == '__main__':

    es = elasticsearch.Elasticsearch()

    if es.indices.exists(index="ap_dataset"):
        print "Index Available"
        es.indices.delete(index=["ap_dataset"],ignore=404)
        print "Index Deleted!"

    start_time = timeit.default_timer()
    print "Starting to Index.."
    setup_index(es)

    for filename in os.listdir("ap89_collection"):
        with open("ap89_collection/"+filename) as f:
            content = f.readlines()

        start =  [i for i,k in enumerate(content) if k.startswith("<DOC>")]
        end = [i for i,k in enumerate(content) if k.startswith("</DOC>")]

        parse(content,start,end,es)

    print "Indexing Completed!"
    print "Runtime(min) is:",(timeit.default_timer() - start_time)/60






