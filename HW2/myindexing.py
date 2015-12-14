__author__ = 'Dev'
import Rank_func

def menu():
    print "\n\t\t\t\t\tMENU"
    print "\t***************************************"
    print "\t1)INDEX WITH STOP WORDS AND NO STEMMING"
    print "\t2)INDEX WITHOUT STOP WORDS AND NO STEMMING"
    print "\t3)INDEX WITH STOP WORDS AND STEMMING"
    print "\t4)INDEX WITHOUT STOP WORDS AND STEMMING"
    option = input("\nEnter your choice of indexing:")

    if option == 1:
        import index1
        # index1.create_partialindex(option)
        # Rank_func.start_ranking("./INDEX-1/","(SNST)",option)

    elif option == 2:
        import index2
        # index2.create_partialindex(option)
        # Rank_func.start_ranking("./INDEX-2/","(NSNST)",option)
    elif option == 3:
        import index3
        # index3.create_partialindex(option)
        # Rank_func.start_ranking("./INDEX-3/","(SST)",option)

    elif option == 4:
        import index4
        # index4.create_partialindex(option)
        Rank_func.start_ranking("./INDEX-4/","(NSST)",option)
    else:
        print "Invalid Choice!"

if __name__ == '__main__':
    user = 'y'
    while user == 'y':
        menu()
        user = raw_input("\nDo You Want To Continue[y/n]:").lower()


