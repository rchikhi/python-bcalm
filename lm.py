import os, sys
from itertools import product
from ograph import Graph
from minimizers import minimizer, minbutbiggerthan

class Bcalm:
    def __init__(self, input_filename, output_filename, k, m):
        self.input_file = open(input_filename)
        self.output_file = open(output_filename,'w')
        self.k = k
        self.m = m
        self.nb_buckets = 4**m
        if self.nb_buckets > 1000:
            sys.exit("Error: m too large, will open too many files")
        self.bucket_names = sorted(list(set(map(lambda s: minimizer(''.join(s), m), product('acgt', repeat=self.m)))))
        if not os.path.exists(".bcalmtmp"):
            os.mkdir(".bcalmtmp")
        else:
            os.system("rm -f .bcalmtmp/*")
        self.bucket_files = dict()
        for bucket in self.bucket_names:
            self.bucket_files[bucket] = open(".bcalmtmp/" + str(bucket),'w')

    def buckets_stats(self):
        for bucket in self.bucket_names:
            os.system('wc -l .bcalmtmp/' + str(bucket) + "|grep -v ^0")

    def createoutfile(self):
        self.partition_kmers()
        for bucket in self.bucket_names:
            G = Graph(self.k)
            self.flush()
            G.importg(".bcalmtmp/" + str(bucket))
            G.debruijn()
            G.compress(bucket)
            for node in G.nodes.values():
                self.goodplace(node, bucket)
    
    def put_in_bucket(self, node, bucket):
        file = self.bucket_files[bucket] if bucket is not None else self.output_file
        file.write("%s;\n" % node)

    def flush(self):
        for bucket in self.bucket_names:
            self.bucket_files[bucket].flush()

    def partition_kmers(self):
        for line in self.input_file:
            kmer = line.strip()[:-1]
            bucket = minimizer(kmer, self.m)
            self.put_in_bucket(kmer, bucket)
        self.buckets_stats()
        
    def goodplace(self, node, bucket):
        min = minbutbiggerthan(node[:self.k-1],node[-(self.k-1):], bucket, self.m)
        self.put_in_bucket(node, min)
