from itertools import product
from ograph import Graph
from minimizers import minimizer, minbutbiggerthan, precompute_hashes
from buckets import Buckets, Superbuckets
from tags import untag, use_tags

def bcalm(input_filename, output_filename, k, m):
    input_file = open(input_filename)
    simple_buckets = False 
    if simple_buckets:
        minimizers = sorted(list(set(map(lambda s: minimizer(''.join(s), m), product('acgt', repeat=m)))))
        buckets = Buckets(minimizers, output_filename)
    else:
        m *= 2
        minimizers = sorted(list(set(map(lambda s: minimizer(''.join(s), m), product('acgt', repeat=m)))))
        buckets = Superbuckets(minimizers, output_filename)
    precompute_hashes(m)


    # partition k-mers
    for line in input_file:
        kmer = line.strip()[:-1]
        bucket_minimizer = minimizer(kmer, m)
        buckets.put(kmer, bucket_minimizer)
    buckets.flush() 
    buckets.stats() 

    # process each bucket in minimizer order
    for bucket_file, bucket_minimizer in buckets.iterate():
        G = Graph(k)
        buckets.flush()
        G.importg(bucket_file)
        G.debruijn()
        G.compress(bucket_minimizer, m)
        for node in G.nodes.values():
            if use_tags:
                node = untag(node)
            min = minbutbiggerthan(node[:k-1],node[-(k-1):], bucket_minimizer, m)
            buckets.put(node, min)
