__author__ = 'Dev'

from Portstemmer import PorterStemmer
import json
import timeit
from Scoring_funcs import RetrievalModels
import os
import re



p = re.compile('[a-zA-Z0-9]+(\.?[a-zA-Z0-9]+)*',re.M|re.I)
st = PorterStemmer()
alphabets = [chr(i) for i in range(97, 123)]


def create_output(path,qno,ranklist,filename):
    global output
    output = open(path+filename,'a')
    rank = 0
    for doc in ranklist:
        rank = rank + 1
        docno = doc_map[str(doc[0])][0]
        file_line = " ".join([qno,"Q0",docno,str(rank),str(doc[1]),"Exp\n"])
        #print file_line
        output.write(file_line)




def modify_query(line,option):
    if option == 1:
        query = []
        for word in re.finditer(p,line):
            query.append(word.group(0))
        return query
    elif option == 2:
        query = []
        for word in re.finditer(p,line):
            if word.group(0) not in stop:
                query.append(word.group(0))
        return query
    elif option == 3:
        query = []
        for word in re.finditer(p,line):
            query.append(st.stem(word.group(0),0,len(word.group(0))-1))
        return query
    elif option == 4:
        query = []
        for word in re.finditer(p,line):
            if word.group(0) not in stop:
                query.append(st.stem(word.group(0),0,len(word.group(0))-1))
        return query



def remove_resultfiles(path):
    for filename in os.listdir(path):
        if filename.startswith("results_"):
            os.remove(path+filename)
            print "Removed Existing",filename


def initialise():
    global doc_okapi,doc_bm25,doc_tfIdf,doc_jelinek,doc_laplace,proximity
    global temp_jelinek,temp_laplace,temp_bm25,temp_tfIdf,temp_okapi,temp_proximity,temp_combine
    doc_okapi = dict()
    proximity = dict()
    doc_tfIdf = dict()
    doc_bm25 = dict()
    doc_laplace = dict()
    doc_jelinek = dict()
    temp_okapi = []
    temp_tfIdf = []
    temp_bm25 = []
    temp_proximity = []
    temp_combine = []
    temp_laplace = []
    temp_jelinek = []



def get_response(wid):
    index.seek(catalogue[wid])
    result = index.readline().strip().split("|")
    return result





def Rank_docs(lines,docIds,r,option,path):
    for line in lines:
        initialise()
        line = line.lower().split()
        query_no = line[0].strip(".")
        if line[4] =="or":
            line = " ".join(line[6:])
        else:
            line = " ".join(line[4:])
        line = modify_query(line,option)
        print "Processing Query: ",query_no
        for word in line:
            print word
            term_stat = terms[word]
            wordid = term_stat[0]
            ttf = term_stat[1]
            res = get_response(str(wordid))
            hit_list = []
            df = len(res)
            for hit in res:
                doc_stats = hit.split()
                doc_id = int(doc_stats[0])
                # print doc_id
                tf = len(doc_stats[1:])
                positions = map(int,doc_stats[1:])
                if doc_id not in doc_tfIdf:
                    doc_okapi[doc_id]={}
                    doc_tfIdf[doc_id] = {}
                    doc_bm25[doc_id] = {}
                    proximity[doc_id] = {}
                    if not query_no in doc_tfIdf[doc_id]:
                        score = r.Okapi_Tf(tf,doc_map[doc_stats[0]][1])
                        doc_okapi[doc_id][query_no] = [score]
                        doc_tfIdf[doc_id][query_no] = [score*r.Tf_Idf(df)]
                        doc_bm25[doc_id][query_no] = [r.Okapi_BM25(tf,df,doc_map[doc_stats[0]][1],line.count(word))]
                        proximity[doc_id][query_no] = [positions]


                else:
                    score = r.Okapi_Tf(tf,doc_map[doc_stats[0]][1])
                    doc_okapi[doc_id][query_no].append(score)
                    doc_tfIdf[doc_id][query_no].append(score*r.Tf_Idf(df))
                    doc_bm25[doc_id][query_no].append(r.Okapi_BM25(tf,df,doc_map[doc_stats[0]][1],line.count(word)))
                    proximity[doc_id][query_no].append(positions)


                if doc_id not in doc_jelinek:
                    doc_laplace[doc_id] = {}
                    doc_jelinek[doc_id] = {}
                    if not query_no in doc_jelinek[doc_id]:
                        doc_laplace[doc_id][query_no] = [r.Laplace_smoothing(tf, doc_map[doc_stats[0]][1])]
                        doc_jelinek[doc_id][query_no] = [r.Jelinek_Mercer(tf,ttf,doc_map[doc_stats[0]][1])]

                else:
                    doc_laplace[doc_id][query_no].append(r.Laplace_smoothing(tf,doc_map[doc_stats[0]][1]))
                    doc_jelinek[doc_id][query_no].append(r.Jelinek_Mercer(tf,ttf,doc_map[doc_stats[0]][1]))
                hit_list.append(doc_id)
            remaining_docs = list(set(docIds)-set(hit_list))
            for i in remaining_docs:
                if not i in doc_jelinek:
                    doc_laplace[i] = {}
                    doc_jelinek[i] = {}
                    if not query_no in doc_jelinek[i]:
                        doc_laplace[i][query_no] = [r.Laplace_smoothing(0,doc_map[str(i)][1])]
                        doc_jelinek[i][query_no] = [r.Jelinek_Mercer(0,ttf,doc_map[str(i)][1])]
                else:
                    doc_laplace[i][query_no].append(r.Laplace_smoothing(0,doc_map[str(i)][1]))
                    doc_jelinek[i][query_no].append(r.Jelinek_Mercer(0,ttf,doc_map[str(i)][1]))

        for doc in docIds:
           temp_laplace.append((doc,sum(doc_laplace[doc][query_no])))
           temp_jelinek.append((doc,sum(doc_jelinek[doc][query_no])))

        for key in doc_tfIdf:
            bm25_score = sum(doc_bm25[key][query_no])
            temp_okapi.append((key,sum(doc_okapi[key][query_no])))
            temp_tfIdf.append((key,sum(doc_tfIdf[key][query_no])))
            temp_bm25.append((key,bm25_score))
            combine_score,prox_score = r.proximity_search(proximity[key][query_no],doc_map[str(key)][1], bm25_score)
            temp_combine.append((key,combine_score))
            temp_proximity.append((key,prox_score))


        create_output(path,query_no ,sorted(temp_okapi,key= lambda x : x[1],reverse=True)[:1000],"results_Okapi.txt")
        create_output(path,query_no ,sorted(temp_tfIdf,key= lambda x : x[1],reverse=True)[:1000],"results_Tf-Idf.txt")
        create_output(path,query_no ,sorted(temp_bm25,key= lambda x : x[1],reverse=True)[:1000],"results_BM25.txt")
        create_output(path,query_no ,sorted(temp_laplace,key= lambda x : x[1],reverse=True)[:1000],"results_Laplace.txt")
        create_output(path,query_no ,sorted(temp_jelinek,key= lambda x : x[1],reverse=True)[:1000],"results_Jelinek.txt")
        # create_output(path,query_no ,sorted(temp_combine,key= lambda x : x[1],reverse=True)[:1000],"results_25proximity.txt")
        create_output(path,query_no ,sorted(temp_proximity,key= lambda x : x[1],reverse=True)[:1000],"results_Proximity.txt")










def start_ranking(path,file,option):


    remove_resultfiles(path)
    global doc_map,catalogue,terms,stop

    docIds = range(1,84679)

    with open("stoplist.txt") as sw:
        stop = map((lambda x:x.strip()),sw.readlines())
        stop.extend(alphabets)


    with open("query_desc.51-100.short.txt") as w:
        lines = w.readlines()

    global index
    index = open(path+"finalindex"+file+".txt")

    with open(path+"new_catalogue"+file+".json") as c:
        catalogue = json.load(c)

    with open(path+"term_mapping"+file+".json") as t:
        terms = json.load(t)

    with open(path+"document_mapping"+file+".json") as docmap:
        doc_map=json.load(docmap)

    r = RetrievalModels(doc_map["total"],len(terms))

    start_time = timeit.default_timer()
    Rank_docs(lines,docIds,r,option,path)
    index.close()
    output.close()
    print "RESULT FILES GENERATED!"
    print "Total Time(min(s)): ",(timeit.default_timer()-start_time)/60.0



