import os, sys
from minimizers import minimizer
from collections import defaultdict

class Buckets:
    def __init__(self, minimizers, overflow_filename = None, prefix = "b"):
        if overflow_filename is not None:
            self.overflow_file = open(overflow_filename, 'w')
        self.minimizers = minimizers
        self.bucket_files = dict()
        self.prefix = prefix
        if not os.path.exists(".bcalmtmp"):
            os.mkdir(".bcalmtmp")
        os.system("rm -f .bcalmtmp/" + prefix + "*")
        for bucket in minimizers:
           self.bucket_files[bucket] = open(".bcalmtmp/" + prefix + str(bucket),'w')

    def stats(self):
        for bucket in self.minimizers:
            os.system('wc -l .bcalmtmp/' + self.prefix + str(bucket) + "|grep -v ^0")

    def iterate(self):
        return [ (".bcalmtmp/" + self.prefix + str(b), b) for b in self.minimizers]

    def flush(self):
        for bucket in self.minimizers:
            self.bucket_files[bucket].flush()

    def put(self, node, bucket, label=""):
        file = self.bucket_files[bucket] if bucket in self.minimizers else self.overflow_file
        file.write("%s;%s\n" % (node, label if label is not None else ""))

    def close(self):
        for bucket in self.minimizers:
           self.bucket_files[bucket].close()

class Superbuckets():
    def __init__(self, minimizers, output_filename):
        self.nb_superbuckets = 256
        nb_buckets_per_superbucket = len(minimizers) / self.nb_superbuckets
        if nb_buckets_per_superbucket > 1000:
            sys.exit("Not enough superbuckets to contain all the buckets")

        self.bucket_superbucket_association = dict([ (bucket, i / self.nb_superbuckets) \
                                                    for (i, bucket) in enumerate(minimizers) ])
        self.superbuckets_names = sorted(list(set(self.bucket_superbucket_association.values())))

        self.superbuckets = Buckets(self.superbuckets_names, output_filename, prefix="s")
        self.bucket_superbucket_association[None] = None # needed for output
        self.current_buckets = None
    
    def iterate(self):
        for superbucket_name in self.superbuckets_names:
            if os.stat(".bcalmtmp/s" + str(superbucket_name))[6] == 0:
                continue # check if superbucket is empty
            self.superbuckets.flush()
            print "Processing superbucket",superbucket_name
            self.create_buckets(superbucket_name)
            for elt in self.current_buckets.iterate():
                yield elt

    def create_buckets(self, superbucket_name):
        minimizers = sorted([ bucket for (bucket, i) in \
                            self.bucket_superbucket_association.items() if i == superbucket_name ])
        if self.current_buckets is not None:
            self.current_buckets.close()
        self.current_buckets = Buckets(minimizers)
        # split superbucket into buckets
        with open(".bcalmtmp/s" + str(superbucket_name)) as f:
            for line in f:
                vertex, bucket = line.strip().split(';')
                if bucket.isdigit(): # hack, bucket names with hash-minimizers are numbers
                    bucket = long(bucket)
                self.current_buckets.put(vertex, bucket)

    def put(self, node, bucket):
        if (self.current_buckets is not None and \
            bucket in self.current_buckets.minimizers and\
            bucket is not None):
            self.current_buckets.put(node, bucket)
        else:
            superbucket = self.bucket_superbucket_association[bucket]
            self.superbuckets.put(node, superbucket, label=bucket)

    def stats(self):
        self.superbuckets.stats()

    def flush(self):
        self.superbuckets.flush()
        if self.current_buckets is not None:
            self.current_buckets.flush()

