from itertools import product
from ograph import Graph
from minimizers import minimizer, minbutbiggerthan
from buckets import Buckets, Superbuckets

def bcalm(input_filename, output_filename, k, m):
    input_file = open(input_filename)
    if 4**m > 1000:
        sys.exit("Error: m too large, will open too many files")

    simple_buckets = False 
    if simple_buckets:
        minimizers = sorted(list(set(map(lambda s: minimizer(''.join(s), m), product('acgt', repeat=m)))))
        buckets = Buckets(minimizers, output_filename)
    else:
        m *= 2
        minimizers = sorted(list(set(map(lambda s: minimizer(''.join(s), m), product('acgt', repeat=m)))))
        buckets = Superbuckets(minimizers, output_filename)


    # partition k-mers
    for line in input_file:
        kmer = line.strip()[:-1]
        bucket_minimizer = minimizer(kmer, m)
        buckets.put(kmer, bucket_minimizer)
    buckets.stats() 

    # process each bucket in minimizer order
    for bucket_file, bucket_minimizer in buckets.iterate():
        G = Graph(k)
        buckets.flush()
        G.importg(bucket_file)
        G.debruijn()
        G.compress(bucket_minimizer, m)
        for node in G.nodes.values():
            min = minbutbiggerthan(node[:k-1],node[-(k-1):], bucket_minimizer, m)
            buckets.put(node, min)
