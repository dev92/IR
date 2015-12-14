__author__ = 'Dev'

import math
from datetime import datetime
import json


with open("new_catalogue.json") as mapping:
    catalogue = json.load(mapping)

def form_graph(vertices):
    pages.add(vertices[0])
    inlinks[vertices[0]] = set(vertices[1:])
    for vertex in vertices[1:]:
        if vertex not in outlinks:
            outlinks[vertex] = [vertices[0]]
        else:
            outlinks[vertex].append(vertices[0])
        outlinks[vertex] = list(set(outlinks[vertex]))


def initial_rank(nodes):
    for node in nodes:
        pagerank[node] = 1/float(len(nodes))

def Perplexity(pages):
    entropy = []
    for page in pages:
        entropy.append(pagerank[page]*math.log(pagerank[page],2))
    return math.pow(2,-sum(entropy))

def PageRank(vertices):
    sinkPr = 0
    for vertex in sink:
        sinkPr+=pagerank[vertex]
    for page in vertices:
        newrank[page] = (0.15)/float(len(vertices))
        newrank[page]+=(0.85*sinkPr)/float(len(vertices))
        for inlink in inlinks[page]:
            if inlink in inlinks:
                newrank[page]+=(0.85*pagerank[inlink])/float(len(outlinks[inlink]))
        pagerank[page] = newrank[page]

def converge(value):
    global count
    if value < 1  and count < 5:
        count+=1
        return False
    elif value > 1:
        count = 0
        return False
    else:
        return True

def Create_file(scores):
    output = open("urlrank.txt",'w')
    for page,score in scores:
        try:
            output.write(catalogue[page]+"\t"+str(score)+"\n")
        except:
            continue
    output.close()




if __name__ == '__main__':

    file = open("linkgraph.txt")
    inlinks = {}
    outlinks = {}
    pagerank = {}
    sink = set()
    newrank = {}
    pages = set()
    inlink_count = []
    scores = []
    iterations = 0
    count = 0
    start = datetime.now()
    print "Starting to Rank.."
    for line in file.readlines():
        line = line.split()
        form_graph(line)
    for page in pages:
        if page not in outlinks:
            sink.add(page)
    print "Completed forming graph in:",(datetime.now()-start)
    initial_rank(pages)
    initial = Perplexity(pages)
    PageRank(pages)
    new_value = Perplexity(pages)
    diff = abs(new_value - initial)
    while not converge(diff):
        iterations+=1
        initial = new_value
        PageRank(pages)
        new_value = Perplexity(pages)
        diff = abs(new_value - initial)

    for page in pages:
        scores.append([page,pagerank[page]])

    Create_file(sorted(scores,key=lambda x:x[1],reverse=True))


    print "Completed Ranking in:",(datetime.now()-start)
    print "Took "+iterations.__str__()+" iterations to converge"




