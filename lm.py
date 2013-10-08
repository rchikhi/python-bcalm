import os, sys
from itertools import product
from ograph import Graph, minimiser, minimiser_rc, minbutbiggerthan

class Bcalm:
    def __init__(self, input_filename, output_filename, k, m):
        self.input_file = open(input_filename)
        self.output_file = open(output_filename,'w')
        self.k = k
        self.m = m
        self.nb_buckets = 4**m
        if self.nb_buckets > 1000:
            sys.exit("Error: m too large, will open too many files")
        self.bucket_names = sorted(map(''.join, product('acgt', repeat=self.m)))
        if not os.path.exists(".bcalmtmp"):
            os.mkdir(".bcalmtmp")
        else:
            os.system("rm .bcalmtmp/*")
        self.bucket_files = dict()
        for bucket in self.bucket_names:
            self.bucket_files[bucket] = open(".bcalmtmp/" + bucket,'w')

    def buckets_stats(self):
        for bucket in self.bucket_names:
            os.system('wc -l .bcalmtmp/' + bucket + "|grep -v ^0")

    def createoutfile(self):
        self.partition_kmers()
        for bucket in self.bucket_names:
            G = Graph(self.k)
            G.importg(".bcalmtmp/" + bucket)
            G.debruijn()
            G.compress()
            for node in G.nodes.values():
                self.goodplace(node, bucket)
    
    def put_in_bucket(self, node, bucket):
        file = self.bucket_files[bucket] if bucket is not None else self.output_file
        file.write("%s;\n" % node)
        file.flush()

    def partition_kmers(self):
        for line in self.input_file:
            kmer = line.strip()[:-1]
            bucket = minimiser_rc(kmer, self.m)
            self.put_in_bucket(kmer, bucket)
        self.buckets_stats()
        
    def goodplace(self, node, bucket):
        min = minbutbiggerthan(node[:self.k-1],node[-(self.k-1):], bucket, self.m)
        self.put_in_bucket(node, min)
