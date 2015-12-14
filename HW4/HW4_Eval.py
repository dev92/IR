__author__ = 'Dev'

import math
import sys,os
import matplotlib.pyplot as plt
from collections import Counter



def F1_Calculation(pr,re):
    if pr+re == 0:
        return 0.0
    else:
        return float((2*pr*re)/float(pr+re))

def DCG_Calculation(rvector):
    total = rvector[0]
    for index,value in enumerate(rvector[1:]):
        total+=float(value/math.log(index+2,2))
    return float(total)



def Calculate_Stats():
    total_stats["relevant"] = 0
    for query in query_ids:
        precision[query] = []
        recall[query] = []
        ndcg[query] = {}
        f1[query] = {}
        total_stats[query] = {}
        filter_results = filter(lambda x:  x[1] >= 1, qrel[query])
        total_stats["relevant"]+=filter_results.__len__()
        relevant = map(lambda y:y[0],filter_results)
        count = 0
        total = 0
        rvector = []
        for i,s in enumerate(result[query]):
            if s in relevant:
                grade = filter(lambda x: x[0]==s,filter_results)[0][1]
                count+=1
                precision[query].append(count/float(i+1))
                recall[query].append(round(count/float(relevant.__len__()),5))
                total+=count/float(i+1)
                rvector.append(grade)
            else:
                precision[query].append(count/float(i+1))
                recall[query].append(round(count/float(relevant.__len__()),5))
                rvector.append(0)


        desc = sorted(rvector,reverse=True)
        dcg = DCG_Calculation(rvector)
        if dcg == 0:
           ndcg[query] = 0
        else:
            ndcg[query] = dcg/DCG_Calculation(desc)
        for k in kvalues:
            try:
                f1[query][k] = F1_Calculation(precision[query][k-1], recall[query][k-1])
            except:
                f1[query][k] = F1_Calculation((precision[query][result[query].__len__()-1]/float(k)),recall[query][result[query].__len__()-1])
        total_stats[query]["rel_ret"] = count
        total_stats[query]["avg"] = total/float(relevant.__len__())
        if relevant.__len__()>result[query].__len__():
            rprec[query] = count/float(relevant.__len__())
        else:
            rprec[query] = precision[query][relevant.__len__()-1]


def Calculate_Total():
    total_queries = query_ids.__len__()
    total_stats["relret"] = 0
    total_stats["ret"] = 0
    total_stats["avg"] = 0
    total_stats["precision"] = {}
    total_stats["recall"] = {}
    total_stats["F1"] = {}
    total_stats["nDCG"] = 0
    total_stats["rprecision"] = 0
    for query in query_ids:
        total_stats["ret"]+=result[query].__len__()
        total_stats["avg"]+=total_stats[query]["avg"]
        total_stats["relret"]+=total_stats[query]["rel_ret"]
        total_stats["rprecision"]+=rprec[query]
        for k in kvalues:
            if k not in total_stats["precision"]:
                try:
                    total_stats["precision"][k] = precision[query][k-1]
                    total_stats["recall"][k] = recall[query][k-1]
                except:
                    total_stats["precision"][k] = precision[query][result[query].__len__()-1]/float(k)
                    total_stats["recall"][k] = recall[query][result[query].__len__()-1]
                total_stats["F1"][k] = f1[query][k]
            else:
                try:
                    total_stats["precision"][k] += precision[query][k-1]
                    total_stats["recall"][k] += recall[query][k-1]
                except:
                    total_stats["precision"][k] += precision[query][result[query].__len__()-1]/float(k)
                    total_stats["recall"][k] += recall[query][result[query].__len__()-1]
                total_stats["F1"][k] += f1[query][k]
        total_stats["nDCG"] += ndcg[query]
    total_stats["nDCG"] = total_stats["nDCG"]/float(total_queries)
    total_stats["rprecision"] = total_stats["rprecision"]/float(total_queries)
    total_stats["avg"] = total_stats["avg"]/float(total_queries)
    for k in kvalues:
        total_stats["precision"][k] = total_stats["precision"][k]/float(total_queries)
        total_stats["recall"][k] = total_stats["recall"][k]/float(total_queries)
        total_stats["F1"][k] = total_stats["F1"][k]/float(total_queries)


def precision_recall():
    total_stats["pr@re"] = [0,0,0,0,0,0,0,0,0,0,0]
    for query in query_ids:
        prec_at_recall[query] = []
        i = 0
        for value in pr_rec:
            while(i<result[query].__len__() and recall[query][i] < value):
                i+=1
            if i<result[query].__len__():
                max_prec = max(precision[query][i:])
                prec_at_recall[query].append(round(max_prec,4))
            else:
                prec_at_recall[query].append(0)
        total_stats["pr@re"] = [x+y for x,y in zip(total_stats["pr@re"],prec_at_recall[query])]
    total_stats["pr@re"] = map(lambda z:z/float(query_ids.__len__()),total_stats["pr@re"])


def Display_Results():
    for query in query_ids:
        relevant = filter(lambda x: x[1] >= 1, qrel[query])
        print "\nQueryid (Num):       "+query
        print "Total number of documents over query "+query
        print "\tRetrieved:\t  ",result[query].__len__()
        print "\tRelevant:\t  ",relevant.__len__()
        print "\tRel_ret:\t  ",total_stats[query]["rel_ret"]
        print "Interpolated Recall - Precision Averages:"
        for r,p in zip(pr_rec,prec_at_recall[query]):
            print "\tAt {:>5.2f}\t{:^.4f}".format(r,p)
        print "Average precision (non-interpolated) for all rel docs(averaged over queries)"
        print "{:>24.4f}\n".format(total_stats[query]["avg"])##Avg precision
        print "{:>24}{:>7}{:>6}".format("Precision","Recall","F1")
        for k in kvalues:
            try:
                print "At{:>5d} docs:\t {:^.4f}\t {:^.4f}\t {:^.4f}".format(k,precision[query][k-1],recall[query][k-1],f1[query][k])
            except:
                precision_k = precision[query][result[query].__len__()-1]/float(k)
                recall_k = recall[query][result[query].__len__()-1]
                print "At{:>5d} docs:\t {:^.4f}\t {:^.4f}\t {:^.4f}".format(k,precision_k,recall_k,f1[query][k])
        print "R-Precision (precision after R (= num_rel for a query) docs retrieved):"
        print "{:>10}:{:>13.4f}".format("Exact",rprec[query])
        print "Normalized Discounted Cumulative Gain for docs retrieved:"
        print "{:>9}:{:>14.4f}".format("nDCG",ndcg[query])


def Display_Summary():
    print "\n{:>25}".format("SUMMARY")
    print "Total number of documents over all {} queries ".format(query_ids.__len__())
    print "\tRetrieved:\t  ",total_stats["ret"]
    print "\tRelevant:\t  ",total_stats["relevant"]
    print "\tRel_ret:\t  ",total_stats["relret"]
    print "Interpolated Recall - Precision Averages:"
    for r,p in zip(pr_rec,total_stats["pr@re"]):
        print "\tAt {:>5.2f}\t{:^.4f}".format(r,p)
    print "Average precision (non-interpolated) for all rel docs(averaged over queries)"
    print "{:>24.4f}\n".format(total_stats["avg"]) ##Avg precision
    print "{:>24}{:>7}{:>6}".format("Precision","Recall","F1")
    for k in kvalues:
        print "At{:>5d} docs:\t {:^.4f}\t {:^.4f}\t {:^.4f}".format(k,total_stats["precision"][k],total_stats["recall"][k],total_stats["F1"][k])
    print "R-Precision (precision after R (= num_rel for a query) docs retrieved):"
    print "{:>10}:{:>13.4f}".format("Exact",total_stats["rprecision"])
    print "Normalized Discounted Cumulative Gain for docs retrieved:"
    print "{:>9}:{:>14.4f}".format("nDCG",total_stats["nDCG"])


def Plot_prec_recall():
    for query in query_ids:
        plt.plot(pr_rec,prec_at_recall[query])
        y1,y2 = plt.axis()[2:]
        plt.axis([0.0,1.0,y1,y2])
        plt.ylabel("Precision")
        plt.xlabel("Recall")
        plt.title("Precision Vs. Recall for Query: "+query)
        plt.savefig("./Plots/"+query+".png")
        plt.close()

def Plot_summary():
    plt.plot(pr_rec,total_stats["pr@re"])
    y1,y2 = plt.axis()[2:]
    plt.axis([0.0,1.0,y1,y2])
    plt.ylabel("Precision")
    plt.xlabel("Recall")
    plt.title("Average Precision Vs. Recall for all "+str(query_ids.__len__())+" Queries")
    plt.savefig("./Plots/Summary.png")
    plt.close()

def CommonGrade(grades):
    if len(grades) == 1:
        return grades[0]
    elif len(grades) > len(set(grades)):
        c = Counter(grades)
        return c.most_common(1)[0][0]
    else:
        return int(round(reduce(lambda x,y:x+y,grades)/len(grades)))



if __name__ == '__main__':

    disp = False

    if len(sys.argv) < 3:
        print "Parameters Missing!"
        sys.exit(0)

    elif sys.argv[1] == "-q" and len(sys.argv) == 4:
        qfile = sys.argv[2]
        rfile = sys.argv[3]
        disp = True

    elif sys.argv[1]!="-q" and len(sys.argv) == 4:
        print "[-q] to display summary for each query"
        sys.exit(0)

    else:
        qfile = sys.argv[1]
        rfile = sys.argv[2]

    try:
        qrel_file = open(qfile)
    except:
        print "Qrel File Does not Exist!"
        sys.exit(0)
    try:
        result_file = open(rfile)
    except:
        print "Result File Does not Exist!"
        sys.exit(0)

    if not os.path.isdir("Plots"):
        os.mkdir("./Plots")

    for figures in os.listdir("./Plots/"):
        if figures.endswith(".png"):
            os.remove("./Plots/"+figures)

    query_ids = set()
    precision = {}
    recall = {}
    f1 = {}
    ndcg = {}
    rprec = {}
    pr_rec = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    result = {}
    prec_at_recall = {}
    total_stats = {}
    max_size = 0

    for lines in result_file.readlines():
        line = lines.rstrip().split()
        if line[0] not in query_ids:
            query_ids.add(line[0])
            result[line[0]] = [line[2]]
        else:
            result[line[0]].append(line[2])
        if max_size < result[line[0]].__len__():
            max_size = result[line[0]].__len__()

    if max_size > 100 and max_size < 1000:
        kvalues = [5,10,20,50,100,max_size]
    elif max_size == 1000:
        kvalues = [5,10,20,50,100,200,500,1000]
    else:
        kvalues = [5,10,20,50,100]

    qrel = {}
    for lines in qrel_file.readlines():
        line = lines.rstrip().split()
        line[3:] = map(int,line[3:])
        grade = CommonGrade(line[3:])
        if line[0] not in qrel and line[0] in query_ids:
            qrel[line[0]] = [[line[2].strip('""'),grade]]
        elif line[0] not in query_ids:
            continue
        else:
            qrel[line[0]].append([line[2].strip('""'),grade])

    query_ids = sorted(query_ids)


    Calculate_Stats()

    Calculate_Total()

    precision_recall()

    if disp:
        Display_Results()
        Display_Summary()
        Plot_prec_recall()
        Plot_summary()
    else:
        Display_Summary()
        Plot_summary()

    qrel_file.close()
    result_file.close()

