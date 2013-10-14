import sys
counter = 0
with open(sys.argv[1]+".fa",'w') as r:
    with open(sys.argv[1]) as f:
        for line in f:
            current = line.strip().upper()[:-1]
            r.write(">%d\n%s\n" % (counter,current))
            counter += 1
