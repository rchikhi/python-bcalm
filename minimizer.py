from ograph import rc
import pyhash
hasher = pyhash.murmur3_32()

def hash_function(seq):
    return hasher(seq) % 1000

def minimizer(seq, size, hash_mode = True):
    if hash_mode:
        minimizer = hash_function(seq[:size])
        for i in xrange(1,len(seq)-size+1):
            minimizer = min(minimizer, hash_function(seq[i:size+i]))
    else:
        minimizer = seq[:size]
        for i in xrange(1,len(seq)-size+1):
            minimizer = min(minimizer,seq[i:size+i])
    return minimizer

def minimizer_rc(seq, size):
    return min(minimizer(seq,size), minimizer(rc(seq),size))

def minbutbiggerthan(firstoverlap, lastoverlap, bucket, size):
    l = [ minimizer(firstoverlap, size), minimizer(rc(firstoverlap), size), \
          minimizer(lastoverlap, size), minimizer(rc(lastoverlap), size) ]
    for min in sorted(l):
        if min > bucket:
            return min
    return None


