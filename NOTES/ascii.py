start=32
#for i in range(start, start+95):

for row in range(11):
    for col in range(9):
        
        x = row+32 + 11*col
        if x <= 127:
            print "%3d %s" % (x-31, chr(x)),
    print
