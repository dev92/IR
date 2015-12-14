__author__ = 'Dev'

import urllib2, json
import bs4, urlparse
import robotparser
import requests
from datetime import datetime
import heapq
from operator import itemgetter
from Canonicalization import Canonicalize,base_url
import nltk
import elasticsearch
import socket
from ElasticSearch_setup import setup_index




s = socket.setdefaulttimeout(60)
client = elasticsearch.Elasticsearch()
robot = robotparser.RobotFileParser()

irrelevant_terms = ['foot-ball','football','base-ball','baseball','hockey','youtube','facebook','twitter']


def Frontier_Mgmt(current_heap,next_heap,current_frontier,next_frontier):

    global prev,count,body

    while current_heap and visited.__len__()<12000:
        body = {}
        current_url = heapq.heappop(current_heap)[2]
        current_frontier.remove(current_url)
        parent_domain = base_url(current_url)
        try:
            if prev!=parent_domain:
                robot.set_url(urlparse.urljoin(parent_domain,'robots.txt'))
                prev = parent_domain
                robot.read()
        except:
            continue
        try:
            resp = requests.head(current_url)
        except:
            continue

        if 'content-language' in resp.headers:
           if resp.headers["content-language"] != "en":
               continue

        if not 'content-type' in resp.headers:
            continue

        elif resp.headers['content-type'].split(";")[0] == "text/html":
            try:
                html = urllib2.urlopen(current_url).read()
            except:
                continue
            visited.add(current_url)
            urls_crawled.write(current_url+"\n")
            print current_url
            soup = bs4.BeautifulSoup(html)
            body['clean_text'] = unicode(nltk.clean_html(html),errors="ignore")
            body['raw_html'] = unicode(html,errors="ignore")
            body['outlinks'] = set()
            body['inlinks'] = []
            for links in soup.find_all('a',href=True):

                canonicalized_url = ""

                link = links['href']

                try:
                    canonicalized_url = Canonicalize(link,current_url).encode("utf-8")
                except:
                    canonicalized_url = Canonicalize(link,current_url)


                if canonicalized_url == "":
                    continue

                if any(s in canonicalized_url.lower() for s in irrelevant_terms):
                    continue

                if canonicalized_url in visited:
                    body['outlinks'].add(canonicalized_url)
                    if canonicalized_url in inlink:
                        inlink[canonicalized_url].append(current_url)
                    else:
                        inlink[canonicalized_url] = [current_url]
                    continue


                elif canonicalized_url in current_frontier:
                    current_heap[map(itemgetter(2),current_heap).index(canonicalized_url)][0] += -1
                    body['outlinks'].add(canonicalized_url)
                    if canonicalized_url in inlink:
                        inlink[canonicalized_url].append(current_url)
                    else:
                        inlink[canonicalized_url] = [current_url]
                    continue


                elif canonicalized_url in next_frontier:
                    next_heap[map(itemgetter(2),next_heap).index(canonicalized_url)][0] += -1
                    body['outlinks'].add(canonicalized_url)
                    if canonicalized_url in inlink:
                        inlink[canonicalized_url].append(current_url)
                    else:
                        inlink[canonicalized_url] = [current_url]
                    continue

                try:
                    if not robot.can_fetch(AGENT,canonicalized_url):
                        continue
                except:
                    continue

                if next_frontier.__len__()<20000 and not canonicalized_url in visited:
                    count+=1
                    entry = [-1,count,canonicalized_url]
                    heapq.heappush(next_heap,entry)
                    next_frontier.append(canonicalized_url)
                    body['outlinks'].add(canonicalized_url)
                    inlink[canonicalized_url] = [current_url]

            body["outlinks"] = list(body["outlinks"])
            client.index(index="ir-3",doc_type="documents",id=current_url,body=json.dumps(body))
        else:
            continue
    return next_heap,next_frontier


def WebCrawler():

    global heap_l1,heap_l2,frontier_l1,frontier_l2,visited,inlink,client

    while visited.__len__()<12000 and (heap_l1 or heap_l2):

        heap_l2,frontier_l2 = Frontier_Mgmt(heap_l1,heap_l2,frontier_l1,frontier_l2)
        heapq.heapify(heap_l2)
        heap_l1,frontier_l1 = Frontier_Mgmt(heap_l2,heap_l1,frontier_l2,frontier_l1)
        heapq.heapify(heap_l1)





if __name__ == '__main__':

    heap_l1 = []
    heap_l2 = []
    frontier_l1 = []
    frontier_l2 = []
    visited = set()
    prev = ""
    count = 0
    inlink = {}
    setup_index(client)
    AGENT = "*"


    urls_crawled = open("visited_urls.txt",'w')

    start_time = datetime.now()

    seeds = [
    "http://www.basketball-reference.com/awards/nba_50_greatest.html",
    "http://www.basketball-reference.com/leaders/per_career.html",
    "http://basketball.realgm.com/nba/awards",
    "http://en.wikipedia.org/wiki/List_of_career_achievements_by_Kobe_Bryant"
    ]


    for seed in seeds:
        count+=1
        base = base_url(seed)
        canonicalized_url = Canonicalize(seed,base)
        entry = [0,count ,canonicalized_url]
        heapq.heappush(heap_l1, entry)
        frontier_l1.append(canonicalized_url)
    heapq.heapify(heap_l1)

    print "Starting To Crawl....."

    WebCrawler()

    print "Completed crawling:",visited.__len__()

    print "running time:",(datetime.now()-start_time)

    urls_crawled.close()

    with open("inlink_file.json",'w') as output:
        json.dump(inlink,output)


