import os, sys
from itertools import product
from minimizers import minimizer

class Buckets:
    def __init__(self, m, output_filename):
        self.m = m
        self.nb_buckets = 4**m
        self.output_file = open(output_filename, 'w')

        if self.nb_buckets > 1000:
            sys.exit("Error: m too large, will open too many files")
        if not os.path.exists(".bcalmtmp"):
            os.mkdir(".bcalmtmp")
        else:
            os.system("rm -f .bcalmtmp/*")

        self.minimizers = sorted(list(set(map(lambda s: minimizer(''.join(s), m), product('acgt', repeat=self.m)))))
        self.bucket_files = dict()
        for bucket in self.minimizers:
            self.bucket_files[bucket] = open(".bcalmtmp/" + str(bucket),'w')

    def stats(self):
        for bucket in self.minimizers:
            os.system('wc -l .bcalmtmp/' + str(bucket) + "|grep -v ^0")

    def iterate(self):
        return [ (".bcalmtmp/" + str(b), b) for b in self.minimizers]

    def flush(self):
        for bucket in self.minimizers:
            self.bucket_files[bucket].flush()

    def put(self, node, bucket):
        file = self.bucket_files[bucket] if bucket is not None else self.output_file
        file.write("%s;\n" % node)
