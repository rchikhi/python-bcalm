import sys
with open(sys.argv[1]+".dot",'w') as r:
    with open(sys.argv[1]) as f:
        r.write("digraph G { \n")
        for line in f:
            current = line.strip().lower().split()[0]
            r.write("%s;\n" % current)
        r.write("}")
