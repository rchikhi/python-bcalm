import string

#-------- parameter
use_tags = True 
#--------

current_tag = 0
tag_template = "+tag%d+"
tags_filename = ".bcalmtmp/tags"
tags_file = None

revcomp_trans=string.maketrans('actg', 'tgac')
def rc(s):
    return string.translate(s, revcomp_trans)[::-1]

def tag(s, k):
    global current_tag, tags_file
    if tags_file is None:
        tags_file = open(tags_filename,"w")
    if len(s) < 10*k:
        return s
    start, middle, end = s[:k], s[k:-k], s[-k:]
    tags_file.write("%d %s\n" % (current_tag, middle))
    s2 = start + (tag_template % current_tag) + end
    current_tag += 1
    return s2

def untag(s):
    global tags_file
    is_DNA = True
    res = ""
    for c in s.split('+'):
        if not is_DNA:
            reverse_tag = (c[0] != 't')
            t = rc(c) if reverse_tag else c
            n = t[3:]
            if tags_file is not None:
                tags_file.close()
            tags_file = open(tags_filename)
            for line in tags_file:
                tags_file_n, seq = line.split()
                if n == tags_file_n:
                    res += rc(seq) if reverse_tag else seq
                    break
        else:
            res += c
        is_DNA = not is_DNA
    if tags_file is not None:
        tags_file.close()
        tags_file = None
    return res

def test():
    print tag("abcdefghijkl",3) == "abc+tag0+jkl"
    print tag("abcdefghijkl",3) == "abc+tag1+jkl"
    print tag("1234567890123",3) == "123+tag2+123"
    print untag("123+tag2+123") == "1234567890123"
    print untag("123+2gat+123") == "1230987654123"
    print untag("123+tag2+123abc+tag1+jklabc+0cta+jkl") == "1234567890123abcdefghijklabcihcfedjkl"
