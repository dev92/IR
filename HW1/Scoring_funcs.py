__author__ = 'Dev'

import math
import elasticsearch
import json

class RetrievalModels:

    def __init__(self):
        es = elasticsearch.Elasticsearch()
        res = es.search(index="ap_dataset",doc_type="documents",body={
   "size": 0,
   "aggs": {
      "unique_terms": {
         "cardinality": {
              "field":"text"
         }
      }
   }
})
        with open("document_lengths.json") as f:
            doc_stats = json.load(f)
        self.k1 = 1.20
        self.k2 = 100.0
        self.b = 0.75
        self.V = res["aggregations"]["unique_terms"]['value']
        self.avg_length = doc_stats["avg_length"]
        #Avg length : 247.81119062802617
        #Total document length : 20984156
        self.D = 84678.0
        self.p = 0.8


    def Okapi_Tf(self,tf,dl):
        return float(float(tf)/(tf+0.5+1.5*(dl/self.avg_length)))

    def Tf_Idf(self,df):
        return float(math.log10(self.D/df))

    def Okapi_BM25(self,tf,df,dl,qf):
        first_term = float(math.log10((self.D+0.5)/(df+0.5)))
        second_term = float(tf*(self.k1+1.0)/(tf+self.k1*((1.0-self.b)+self.b*(dl/self.avg_length))))
        third_term =float(qf*(self.k2+1.0)/(qf+self.k2))
        return first_term*second_term*third_term

    def Laplace_smoothing(self,tf,dl):
        return float(math.log10((tf+1.0)/(dl+self.V)))

    def Jelinek_Mercer(self,tf,ttf,dl):
        if dl == 0:
            foreground = 0
        else:
            foreground = float(self.p*(float(tf)/dl))
        background = float((1.0-self.p)*(float(ttf)/self.V))
        return float(math.log10(foreground+background))

