import string

hash_mode = False 
if hash_mode:
    import pyhash
    hasher = pyhash.murmur3_32()

revcomp_trans=string.maketrans('actg', 'tgac')
def rc(s):
    return string.translate(s, revcomp_trans)[::-1]

def hash_function(seq):
    return hasher(seq) % 1000000

def minimizer_singlestrand(seq, size):
    if hash_mode:
        minimizer = hash_function(seq[:size])
        for i in xrange(1,len(seq)-size+1):
            minimizer = min(minimizer, hash_function(seq[i:size+i]))
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


