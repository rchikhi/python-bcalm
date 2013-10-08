from ograph import Graph
from lm import Bcalm
import sys

# ---
# hardcoded parameters
minimiser_size = 4
# ---

def naive(input, output):
    G = Graph(k)
    G.importg(input)
    G.debruijn()
    G.compress()
    G.output(output)
    sys.exit()

if len(sys.argv) > 0:
    k = len(open(sys.argv[1]).readline().strip().strip(';'))
    print "auto-detected k:", k
    if '--naive' in sys.argv:
        naive(sys.argv[1], "output.dot")
    else:
        B = Bcalm(sys.argv[1], "output.dot", k, minimiser_size)
        B.createoutfile()
else:
    print "command line: input.dot output.dot [--naive]"
    sys.exit()
