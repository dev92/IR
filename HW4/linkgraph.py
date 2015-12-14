__author__ = 'Dev'

import elasticsearch
import json

client = elasticsearch.Elasticsearch()

f = open("complete_urls.txt")
link = open("linkgraph.txt",'w')

url_map = {}

unique_id = 1

for line in f.readlines():
    if line.rstrip() not in url_map:
        url_map[line.rstrip()] = unique_id
        unique_id+=1
    file_line = str(url_map[line.rstrip()])
    print line.strip()
    res = client.get(index="basketball",doc_type="page",id=line.rstrip())
    for url in res["_source"]["inlinks"]:
            if url.rstrip() not in url_map:
                url_map[url.rstrip()] = unique_id
                unique_id+=1
            file_line+=(" "+str(url_map[url.rstrip()]))
    file_line+="\n"
    link.write(file_line)

link.close()
with open("catalogue.json",'w') as output:
    json.dump(url_map,output)