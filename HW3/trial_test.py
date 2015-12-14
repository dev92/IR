
from datetime import datetime
import elasticsearch


queue_map = {}



# class Job(object):
#     def __init__(self, priority, alive, description):
#         self.priority = priority
#         self.description = description
#         self.alive = alive
#         # print 'New job:', description
#         return
#     def __cmp__(self, other):
#         c = cmp(self.priority, other.priority)
#         if c != 0:
#             return -c
#         else:
#             return cmp(self.alive,other.alive)
#
#
# q = Queue.PriorityQueue()
#
# queue_map['Mid-level job'] = Job(1, 1, 'Mid-level job')
# queue_map['Low-level job'] = Job(1, 2, 'Low-level job')
# queue_map['Important job'] = Job(1, 3, 'Important job')
#
# q.put( queue_map['Mid-level job'] )
# q.put( queue_map['Low-level job'])
# q.put( queue_map['Important job'])
#
# print queue_map['Mid-level job']
# print queue_map['Important job'].description
# temp = q.get( queue_map['Important job'] )
# print temp
# queue_map['Important job'] = Job(temp.priority+1,temp.alive,temp.description)
# q.put(queue_map['Important job'])

# while not q.empty():
#     next_job = q.get()
#     print 'Processing job:', next_job.description,next_job.priority
#
# heap = []
#
# entry = [-1,1,"one"]
# heapq.heappush(heap,entry)
# entry = [-1,4,"five"]
# heapq.heappush(heap,entry)
# entry = [-1,3,"ten"]
# heapq.heappush(heap,entry)
#
# heap[map(itemgetter(2),heap).index("ten")][0] += -1

# print heapq.nsmallest(50,heap)
# heapq.heapify(heap)
# heap[map(itemgetter(2),heap).index("ten")][0] += -1
# heap[map(itemgetter(2),heap).index("one")][0] += -3
# heapq.heapify(heap)

# while heap:
#     print heapq.heappop(heap)

# print list(zip(*heap)[2])
# heap[map(itemgetter(2),heap).index("four")][0] += -1
# heapq.heapify(heap)

# print heapq.heappop(heap)
# print heapq.heappop(heap)

# a =  Canonicalize("/wiki/Los_Angeles_Lakers","http://en.wikipedia.org/wiki/List_of_career_achievements_by_Kobe_Bryant")

# path1 = urlparse.urlparse("http://www.example.com///a.html").path
#
# print re.sub("/+","/",path1)
# print a
# print b
#
# cache = {}
#
# robots = RobotsCache()
# # cache["http://en.wikipedia.org"] = robot.set_url("http://en.wikipedia.org/robots.txt")
# # robot.set_url(cache["http://en.wikipedia.org"])
# # robot.read()
# r = requests.head("http://en.wikipedia.org/wiki/LeBron_James")

# print type(r.headers["content-language"])

# charset = r.headers['content-type'].split(';')[1].split("=")[1].lower()
# # print r.headers['content-type']
# print nltk.clean_html((r.text).encode(charset)).strip("\t,\n")
# # print robots.allowed("/wiki/List_of_career_achievements_by_Kobe_Bryant","*")



