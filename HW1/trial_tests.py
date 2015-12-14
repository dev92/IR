__author__ = 'Dev'

import json
import elasticsearch
import os

from Portstemmer import PorterStemmer

es = elasticsearch.Elasticsearch()
#
#
# es.put_script(lang='groovy',id='getTF',body={
#     "script": "_index[field][term].tf()"
# })
#
# es.indices.refresh(index="ap_dataset")
#
# res = es.search(index="ap_dataset",doc_type="documents",body={
#     "query": {
#         "function_score": {
#             "query": {
#                 "match": {
#                     "text": "celluloid"
#                 }
#             },
#             "functions": [
#                 {
#                     "script_score": {
#                         "script_id": "getTF",
#                         "lang" : "groovy",
#                         "params": {
#                             "term": "celluloid",
#                             "field": "text"
#                         }
#                     }
#                 }
#             ],
#             "boost_mode": "replace"
#         }
#     },
#     "size": 84679,
#     "fields": ["stream_id"]
# })
# terms = res['hits']['hits']
# print sum([key['_score'] for key in terms])


# sample = "the role of Israel in the Iran-Contra Affair The"

#
# sample =  " ".join(map(lambda x:" ".join(x.split("-")),sample.split())).split()

with open("document_lengths.json",'r') as f:
    document_lengths = json.load(f)

print document_lengths["avg_length"]











