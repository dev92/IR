__author__ = 'Dev'

import math
import numpy as np
import sys

class RetrievalModels:

    def __init__(self,totaldoc,vocab):


        self.k1 = 1.20
        self.k2 = 100.0
        self.b = 0.75
        self.V = float(vocab)
        self.avg_length = float(totaldoc/84678.0)
        self.D = 84678.0
        self.p = 0.8
        self.C = 1500.0


    def Okapi_Tf(self,tf,dl):
        return float(float(tf)/(tf+0.5+1.5*(dl/self.avg_length)))

    def Tf_Idf(self,df):
        return float(math.log10(self.D/df))

    def Okapi_BM25(self,tf,df,dl,qf):
        first_term = float(math.log10((self.D+0.5)/(df+0.5)))
        second_term = float((tf*(self.k1+1.0))/(tf+(self.k1*((1.0-self.b)+self.b*(dl/self.avg_length)))))
        third_term = float((qf*(self.k2+1.0))/(qf+self.k2))
        return float(first_term*second_term*third_term)

    def Laplace_Smoothing(self,tf,dl):
        return float(math.log10((tf+1.0)/(dl+self.V)))

    def Jelinek_Mercer(self,tf,ttf,dl):
        if dl == 0:
            foreground = 0
        else:
            foreground = float(self.p*(float(tf)/dl))
        background = float((1.0-self.p)*(float(ttf)/self.V))
        return float(math.log10(foreground+background))

    def Proximity_Search(self, positions, doclen, bm25_score):

        B = positions

        inner_max_len = max(map(len, B))
        result = np.zeros([len(B), inner_max_len],np.int64)
        for i, row in enumerate(B):
            for j, val in enumerate(row):
                result[i][j] = val
        B = np.array(result)
        csize = B.shape[1]
        rsize = B.shape[0]

        if rsize > 1:

            span = []
            exhausted = []
            window = list(B[:,0])
            minelement = min(window)
            pos = window.index(minelement)
            span.append(max(window)-min(window))
            while len(exhausted)!=len(window):
                row = np.where(B==minelement)[0][0]
                col = np.where(B==minelement)[1][0]
                if col+1<csize:
                    if B[row][col+1] == 0:
                        exhausted.append(minelement)
                        new_lst = [m for m in window if m not in exhausted]
                        if len(new_lst)>0:
                            minelement = min(new_lst)
                            pos = window.index(minelement)
                    else:
                        window[pos] = B[row][col+1]
                        span.append(max(window)-min(window))
                        minelement = min([m for m in window if m not in exhausted])
                        pos = window.index(minelement)
                else:
                    exhausted.append(minelement)
                    new_lst = [m for m in window if m not in exhausted]
                    if len(new_lst)>0:
                        minelement = min(new_lst)
                        pos = window.index(minelement)
            power = float(math.exp(-min(span)+1))
            return (bm25_score+float(math.log(0.7+power))), float(((self.C-min(span))*rsize)/(float(self.V+doclen)))
        else:
            power = float(math.exp(-sys.maxint))
            return (bm25_score+float(math.log(0.7+power))), float((self.C-sys.maxint)/(float(self.V+doclen)))

