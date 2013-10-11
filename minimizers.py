import string
from itertools import product

NONE, PYHASH, PURE_PYTHON_HASH, CACHED = 0, 1, 2, 3
hash_mode = PURE_PYTHON_HASH 

if hash_mode == PYHASH:
    import pyhash
    hasher = pyhash.murmur3_32()
    def hash_function(seq):
        return hasher(seq) % 1000000
elif hash_mode == PURE_PYTHON_HASH:
    def hash_integer(elem):
        # RanHash
        v = elem * 3935559000370003845 + 2691343689449507681;
        v = v ^ (v >> 21);
        v = v ^ (v << 37);
        v = v ^ (v >>  4);
        v = v * 4768777513237032717;
        v = v ^ (v << 20);
        v = v ^ (v >> 41);
        v = v ^ (v <<  5);
        return v
    def hash_function(seq):
        return hash_integer(hash(seq)) % 1000000

hash_dict = None
def precompute_hashes(m):
    global hash_dict, hash_mode
    if hash_mode == NONE:
        return
    hash_dict = dict([ (''.join(x), hash_function(''.join(x))) for x in product('acgt', repeat=m)]) 
    hash_mode = CACHED
    print "Precomputed hashes"

revcomp_trans=string.maketrans('actg', 'tgac')
def rc(s):
    return string.translate(s, revcomp_trans)[::-1]

def minimizer_singlestrand(seq, size):
    if hash_mode == PYHASH or hash_mode == PURE_PYTHON_HASH:
        minimizer = hash_function(seq[:size])
        for i in xrange(1,len(seq)-size+1):
            minimizer = min(minimizer, hash_function(seq[i:size+i]))
    elif hash_mode == CACHED:
        minimizer = hash_dict[seq[:size]]
        for i in xrange(1,len(seq)-size+1):
            minimizer = min(minimizer, hash_dict[seq[i:size+i]])
    else:
        minimizer = seq[:size]
        for i in xrange(1,len(seq)-size+1):
            minimizer = min(minimizer, seq[i:size+i])
    return minimizer

def minimizer(seq, size):
    return min(minimizer_singlestrand(seq,size), minimizer_singlestrand(rc(seq),size))

def minbutbiggerthan(firstoverlap, lastoverlap, bucket, size):
    l = [ minimizer(firstoverlap, size), minimizer(lastoverlap, size) ]
    for min in sorted(l):
        if min > bucket:
            return min
    return None


