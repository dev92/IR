import timeit
import json
import os


def form_finalindex(choice):

    if choice == 1:
        path = './INDEX-1/'
        filename = "(SNST).json"
    elif choice == 2:
        path = './INDEX-2/'
        filename = "(NSNST).json"
    elif choice == 3:
        path = './INDEX-3/'
        filename = "(SST).json"
    elif choice == 4:
        path = './INDEX-4/'
        filename = "(NSST).json"



    with open(path+"catalogue"+filename) as offset:
        catalogue = json.load(offset)

    index = open(path+"partialindex"+filename)

    new = {}
    new_filename = filename.replace(".json",".txt")
    finalindex = open(path+"finalindex"+new_filename,'w')

    # start_time = timeit.default_timer()
    for dblock in catalogue:
        line = []
        for pos in catalogue[dblock]:
            index.seek(pos)
            temp = json.loads(index.readline())
            for key in temp:
                line.append(" ".join([key, " ".join(map(str, temp[key]))]))
        text = "|".join(line)
        new[dblock] = finalindex.tell()
        finalindex.write(text + "\n")

    # print "Running Time(mins)", (timeit.default_timer() - start_time) / 60.0

    finalindex.close()
    print "Final Inverted Index Created!"
    os.remove(path+"partialindex"+filename)
    os.remove(path+"catalogue"+filename)
    with open(path+"new_catalogue"+filename,'w') as n:
        json.dump(new, n)



