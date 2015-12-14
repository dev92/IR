
import elasticsearch
import json
from datetime import datetime
from ElasticSearch_setup import setup_index


if __name__ == '__main__':


    client = elasticsearch.Elasticsearch()

    setup_commonindex(client)

    visited = open("complete_urls.txt")

    start = datetime.now()

    for link in visited.readlines():
        print link.rstrip()
        flag = 0
        body ={}
        try:
            res = client.get(index="basketball",id=link.rstrip(),doc_type="page")
        except elasticsearch.NotFoundError:
            flag = 1
        try:
            myindex = client.get(index="ir-hw3",id=link.rstrip(),doc_type="documents")
        except:
            continue
        if flag == 1:
            body["clean_text"] = myindex["_source"]['clean_text']
            body["raw_html"] = myindex["_source"]['raw_html']
            body["outlinks"] = myindex["_source"]['outlinks']
            body["inlinks"] = myindex["_source"]['inlinks']
            client.index(index="basketball",doc_type="page",id =link.rstrip(),body=json.dumps(body))
        else:
            # print link.rstrip()
            body["doc"] = {}
            res["_source"]["inlinks"].extend(myindex["_source"]["inlinks"])
            body["doc"]["inlinks"] = list(set(res["_source"]["inlinks"]))
            client.update(index="basketball",id=link.rstrip(),doc_type="page",body=json.dumps(body))


    print "time:",datetime.now()-start

