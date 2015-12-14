# __author__ = 'Dev'
#
# import math
# import sys
# from pandas import DataFrame,ExcelWriter
#
#
#
# def F1_Calculation(pr,re):
#     if pr+re == 0:
#         return 0.0
#     else:
#         return float((2*pr*re)/float(pr+re))
#
# def DCG_Calculation(rvector):
#     total = rvector[0]
#     for index,value in enumerate(rvector[1:]):
#         total+=float(value/math.log(index+2))
#     return float(total)
#
#
#
# def Calculate_Stats():
#     total_stats["relevant"] = 0
#     for query in query_ids:
#         precision[query] = {}
#         recall[query] = {}
#         ndcg[query] = {}
#         f1[query] = {}
#         filter_results = filter(lambda x:  x[1] >= 1, qrel[query])
#         total_stats["relevant"]+=filter_results.__len__()
#         relevant = map(lambda y:y[0],filter_results)
#         count = 0
#         total = 0
#         rvector = []
#         for i,s in enumerate(result[query]):
#             if s in relevant:
#                 grade = filter(lambda x: x[0]==s,filter_results)[0][1]
#                 count+=1
#                 precision[query][i+1] = count/float(i+1)
#                 recall[query][i+1] = round(count/float(relevant.__len__()),5)
#                 total+=precision[query][i+1]
#                 rvector.append(grade)
#             else:
#                 precision[query][i+1] = count/float(i+1)
#                 recall[query][i+1] = count/float(relevant.__len__())
#                 rvector.append(0)
#
#
#         desc = sorted(rvector,reverse=True)
#         dcg = DCG_Calculation(rvector)
#         if dcg == 0:
#            ndcg[query] = 0
#         else:
#             ndcg[query] = dcg/DCG_Calculation(desc)
#         for k in kvalues:
#             try:
#                 f1[query][k] = F1_Calculation(precision[query][k], recall[query][k])
#             except KeyError:
#                 f1[query][k] = F1_Calculation((precision[query][result[query].__len__()]/float(k)),recall[query][result[query].__len__()])
#         precision[query]["rel_ret"] = count
#         precision[query]["avg"] = total/float(relevant.__len__())
#         if relevant.__len__()>result[query].__len__():
#             rprec[query] = count/float(relevant.__len__())
#         else:
#             rprec[query] = precision[query][relevant.__len__()]
#
#
# def Calculate_Total():
#     total_queries = query_ids.__len__()
#     total_stats["relret"] = 0
#     total_stats["ret"] = 0
#     total_stats["avg"] = 0
#     total_stats["precision"] = {}
#     total_stats["recall"] = {}
#     total_stats["F1"] = {}
#     total_stats["nDCG"] = 0
#     total_stats["rprecision"] = 0
#     for query in query_ids:
#         total_stats["ret"]+=result[query].__len__()
#         total_stats["avg"]+=precision[query]["avg"]
#         total_stats["relret"]+=precision[query]["rel_ret"]
#         total_stats["rprecision"]+=rprec[query]
#         for k in kvalues:
#             if k not in total_stats["precision"]:
#                 try:
#                     total_stats["precision"][k] = precision[query][k]
#                     total_stats["recall"][k] = recall[query][k]
#                 except KeyError:
#                     total_stats["precision"][k] = precision[query][result[query].__len__()]/float(k)
#                     total_stats["recall"][k] = recall[query][result[query].__len__()]
#                 total_stats["F1"][k] = f1[query][k]
#             else:
#                 try:
#                     total_stats["precision"][k] += precision[query][k]
#                     total_stats["recall"][k] += recall[query][k]
#                 except KeyError:
#                     total_stats["precision"][k] += precision[query][result[query].__len__()]/float(k)
#                     total_stats["recall"][k] += recall[query][result[query].__len__()]
#                 total_stats["F1"][k] += f1[query][k]
#         total_stats["nDCG"] += ndcg[query]
#         total_stats["nDCG"] = total_stats["nDCG"]/float(total_queries)
#     total_stats["rprecision"] = total_stats["rprecision"]/float(total_queries)
#     total_stats["avg"] = total_stats["avg"]/float(total_queries)
#     for k in kvalues:
#         total_stats["precision"][k] = total_stats["precision"][k]/float(total_queries)
#         total_stats["recall"][k] = total_stats["recall"][k]/float(total_queries)
#         total_stats["F1"][k] = total_stats["F1"][k]/float(total_queries)
#
#
#
#
# def Display_Results():
#     for query in query_ids:
#         relevant = filter(lambda x: x[1] >= 1, qrel[query])
#         print "\nQueryid (Num):       "+query
#         print "Total number of documents over query "+query
#         print "\tRetrieved:\t  ",result[query].__len__()
#         print "\tRelevant:\t  ",relevant.__len__()
#         print "\tRel_ret:\t  ",precision[query]["rel_ret"]
#         print "Average precision (non-interpolated) for all rel docs(averaged over queries)"
#         print "{:>24.4f}\n".format(precision[query]["avg"])##Avg precision
#         print "{:>24}{:>7}{:>6}".format("Precision","Recall","F1")
#         for k in kvalues:
#             try:
#                 print "At{:>5d} docs:\t {:^.4f}\t {:^.4f}\t {:^.4f}".format(k,precision[query][k],recall[query][k],f1[query][k])
#             except KeyError:
#                 precision[query][k] = precision[query][result[query].__len__()]/float(k)
#                 recall[query][k] = recall[query][result[query].__len__()]
#                 print "At{:>5d} docs:\t {:^.4f}\t {:^.4f}\t {:^.4f}".format(k,precision[query][k],recall[query][k],f1[query][k])
#         print "R-Precision (precision after R (= num_rel for a query) docs retrieved):"
#         print "{:>10}:{:>13.4f}".format("Exact",rprec[query])
#         print "Normalized Discounted Cumulative Gain for docs retrieved:"
#         print "{:>9}:{:>13.4}".format("nDCG",ndcg["query"])
#
#
# def Display_Summary():
#     print "\n{:>25}".format("SUMMARY")
#     print "Total number of documents over all {} queries ".format(query_ids.__len__())
#     print "\tRetrieved:\t  ",total_stats["ret"]
#     print "\tRelevant:\t  ",total_stats["relevant"]
#     print "\tRel_ret:\t  ",total_stats["relret"]
#     print "Average precision (non-interpolated) for all rel docs(averaged over queries)"
#     print "{:>24.4f}\n".format(total_stats["avg"]) ##Avg precision
#     print "{:>24}{:>7}{:>6}".format("Precision","Recall","F1")
#     for k in kvalues:
#         print "At{:>5d} docs:\t {:^.4f}\t {:^.4f}\t {:^.4f}".format(k,total_stats["precision"][k],total_stats["recall"][k],total_stats["F1"][k])
#     print "R-Precision (precision after R (= num_rel for a query) docs retrieved):"
#     print "{:>10}:{:>13.4f}".format("Exact",total_stats["rprecision"])
#     print "Normalized Discounted Cumulative Gain for docs retrieved:"
#     print "{:>9}:{:>13.4}".format("nDCG",total_stats["nDCG"])
#
#
# if __name__ == '__main__':
#
#     disp = False
#
#     if len(sys.argv) < 3:
#         print "Parameters Missing!"
#         sys.exit(0)
#
#     elif sys.argv[1] == "-q" and len(sys.argv) == 4:
#         qfile = sys.argv[2]
#         rfile = sys.argv[3]
#         disp = True
#
#     elif sys.argv[1]!="-q" and len(sys.argv) == 4:
#         print "[-q] to display summary for each query"
#         sys.exit(0)
#
#     else:
#         qfile = sys.argv[1]
#         rfile = sys.argv[2]
#
#     try:
#         qrel_file = open(qfile)
#     except:
#         print "Qrel File Does not Exist!"
#         sys.exit(0)
#     try:
#         result_file = open(rfile)
#     except:
#         print "Result File Does not Exist!"
#         sys.exit(0)
#
#     query_ids = set()
#     precision = {}
#     recall = {}
#     f1 = {}
#     ndcg = {}
#     rprec = {}
#     kvalues = [5,10,20,50,100]
#     result = {}
#     total_stats = {}
#
#     for lines in result_file.readlines():
#         line = lines.rstrip().split()
#         if line[0] not in query_ids:
#             query_ids.add(line[0])
#             result[line[0]] = [line[2]]
#         else:
#             result[line[0]].append(line[2])
#
#     qrel = {}
#     for lines in qrel_file.readlines():
#         line = lines.rstrip().split()
#         line[3] = int(line[3])
#         if line[0] not in qrel and line[0] in query_ids:
#             qrel[line[0]] = [line[2:4]]
#         elif line[0] not in query_ids:
#             continue
#         else:
#             qrel[line[0]].append(line[2:4])
#
#     query_ids = sorted(query_ids)
#
#
#     Calculate_Stats()
#
#     Calculate_Total()
#
#     if disp:
#         Display_Results()
#         Display_Summary()
#     else:
#         Display_Summary()
#
#     qrel_file.close()
#     result_file.close()
#
# writer = ExcelWriter('Qrel.xlsx')
# assid = ["DP_Pucha"]*200
# for file in [("15011","qrel-web-15011.txt"),("15012","qrel-web-15012.txt"),("15013","qrel-web-15013.txt")]:
#     f1 = open(file[1])

# f2 = open("test.txt")
#
# for line in f2.readlines():
#     print line.split(",")[0].strip("'('")
#
dict = {"a":1,"b":2}

print dict.items()
# file1 = set()
# file2 = set()
#     urls = []
#     grade = []
#     for line in f1.readlines():
#         urls.append(line.split()[2])
#         grade.append(line.split()[3])
#     query = [file[0]]*200
#
#
#     df = DataFrame({"QueryID":query,"AssessorID":assid,"DOCID":urls,"GRADE":grade})
#
#     df.to_excel(writer,sheet_name=file[0],index=False)
#
# writer.save()


#
# print file1.__len__()
# print file2.__len__()
# diff = list(file1-file2)
# print diff

# rank = 1
# f3 = open("ranklist.txt",'a')
#
# f2.seek(0)
# for line in f2.readlines():
#     print line.split()[2]
#     if not line.split()[2] in diff:
#         print line
#         file_line = " ".join(["15013","DP_Pucha",line.split()[2],str(rank),line.split()[3],"Exp\n"])
#         f3.write(file_line)
#         rank+=1
# f3.close()

