__author__ = 'Dev'


import os
import timeit
import re
import json
import Finalindex
import shutil

docno = 0
termid = 0
total_length = 0

index= {}
doc_map = {}
term_map = {}
count = 0
term_offset = {}
alphabets = [chr(i) for i in range(97, 123)]
p = re.compile('[a-zA-Z0-9]+(\.?[a-zA-Z0-9]+)*',re.M|re.I)




def generate_fileline(lines):
    for key in lines:
        if key not in term_offset:
            term_offset[key] = [output.tell()]
            json.dump(lines[key],output)
            output.write("\n")
        else:
            term_offset[key].append(output.tell())
            json.dump(lines[key],output)
            output.write("\n")


def parse(content,start,end,stop):
    global docno,termid,count,index,total_length
    for s, e in zip(start, end):
        text = []
        pos = 0
        docno+=1
        count+=1
        begin = [i for i in range(s + 1, e) if content[i].startswith("<TEXT>")]
        fin = [i for i in range(s + 1, e) if content[i].startswith("</TEXT>")]
        doc = [content[d].split()[1] for d in range(s+1,e) if content[d].startswith("<DOCNO>")]
        doc_map[docno] = [doc[0]]
        for l, k in zip(begin, fin):
            if len(content[l].strip()) > 6:
                text.append(content[l].strip("<TEXT>").strip().lower())
            text.append("".join(content[l + 1:k]).lower())
        for word in re.finditer(p, "".join(text).strip()):
            match = word.group(0)
            if not match in stop:
                pos+=1
                if not match in term_map:
                    ttf = 0
                    termid+=1
                    ttf+=1
                    term_map[match]=[termid,ttf]
                    index[termid] = {}
                    if docno not in index[termid]:
                        index[termid][docno] = [pos]

                elif term_map[match][0] not in index:
                    index[term_map[match][0]] = {}
                    if docno not in index[term_map[match][0]]:
                        index[term_map[match][0]][docno] = [pos]
                    term_map[match][1]+=1

                elif docno not in index[term_map[match][0]]:
                    index[term_map[match][0]][docno] = [pos]
                    term_map[match][1]+=1

                else:
                    index[term_map[match][0]][docno].append(pos)
                    term_map[match][1]+=1
        doc_map[docno].append(pos)
        total_length+=pos
        if count == 1000:
            count = 0
            generate_fileline(index)
            index = {}

def create_partialindex(option):

    if os.path.isdir("INDEX-2"):
        shutil.rmtree("INDEX-2")
        print "Removed Existing INDEX-2"


    os.mkdir("INDEX-2")
    global output
    output = open("./INDEX-2/partialindex(NSNST).json",'w')

    start_time = timeit.default_timer()
    print "Starting to Create Partial Inverted Index..."

    global index
    global count
    index = {}
    count = 0

    with open("stoplist.txt") as sw:
        stop = map((lambda x: x.strip()), sw.readlines())
        stop.extend(alphabets)
        stop = list(set(stop))
        stop.append("")

    for file in os.listdir("ap89_collection"):
        # print file
        with open("ap89_collection/"+file) as f:
            content = f.readlines()

        start = [i for i, k in enumerate(content) if k.startswith("<DOC>")]
        end = [i for i, k in enumerate(content) if k.startswith("</DOC>")]

        parse(content, start, end, stop)

    if count != 0:
        print "last few documents"
        count = 0
        generate_fileline(index)
        index = {}

    output.close()

    with open("./INDEX-2/catalogue(NSNST).json",'w') as offset:
        json.dump(term_offset,offset)

    doc_map["total"] = total_length

    with open("./INDEX-2/document_mapping(NSNST).json",'w') as docmap:
        json.dump(doc_map,docmap)

    with open("./INDEX-2/term_mapping(NSNST).json",'w') as termmap:
        json.dump(term_map,termmap)

    if output.closed:
        print "Starting to Merge...."
        Finalindex.form_finalindex(option)

    print "Running Time(mins)", (timeit.default_timer() - start_time) / 60.0










