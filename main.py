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
    input = sys.argv[1]
else:
    sys.exit("command line: input.dot output.dot [--naive]")

if len(sys.argv) > 1:
    output = sys.argv[2]
else:
    output = "output.dot"

k = len(open(sys.argv[1]).readline().strip().strip(';'))
print "auto-detected k:", k
if '--naive' in sys.argv:
    naive(input, output)
else:
    B = Bcalm(input, output, k, minimiser_size)
    B.createoutfile()


