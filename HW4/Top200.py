__author__ = 'Dev'

import elasticsearch

client = elasticsearch.Elasticsearch()

output = open("ranklist.txt",'w')

hits = client.search(index="basketball",doc_type="page",body={
    "query": {
        "match": {
            "clean_text":"Michael Jordan Retirement"
        }
    },
    "_source": {
        "exclude": ["clean_text","raw_html","outlinks","inlinks"]
    },
    "size": 200
})

rank = 1
for hit in hits["hits"]["hits"]:
    file_line = " ".join(["15011","DP_Pucha",hit["_id"],str(rank),str(hit["_score"]),"Exp\n"])
    output.write(file_line)
    rank+=1


output.close()