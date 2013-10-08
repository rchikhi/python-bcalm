from collections import defaultdict
import string

revcomp_trans=string.maketrans('actg', 'tgac')
def rc(s):
    return string.translate(s, revcomp_trans)[::-1]

class Graph:
    def __init__(self, k):
        self.k = k
        self.nodes = dict()
        self.last_node_index = 0
        self.map = defaultdict(list) # last k-1-mers
        self.maprev = defaultdict(list) # last k-1-mers, reverse complemented
        self.neighbor = defaultdict(list)
    

    def addvertex(self, vertex):
        key = vertex[:self.k-1]
        keyrc = rc(vertex)[:self.k-1]
        idx = self.last_node_index 
        self.nodes[idx] = vertex
        self.map[key] += [idx]
        self.maprev[keyrc] += [idx]
        self.last_node_index += 1

    def importg(self, name):
        for line in open(name):
            vertex = line.strip()[:-1]
            self.addvertex(vertex)

    def output(self, file):
        with open(file,'w') as f:
            for n in self.nodes:
                f.write("%s;\n" % self.nodes[n])

    def add_edge(self, i1, i2, label):
        self.neighbor[i1] += [(i2, label[0])]
        self.neighbor[i2] += [(i1, label[1])]

    def get_edge_label(self, i1, i2):
        return [ l for i,l in self.neighbor[i1] if i == i2 ][0]

    def debruijn(self):
        for i, node in self.nodes.items():
            key = node[-(self.k-1):]
            for other_idx in self.map[key]:
                self.add_edge(i, other_idx, 'OI') # I'm using the In/Out notation, this is a >--> edge
            for other_idx in self.maprev[key]:
                # prevent adding same edge twice
                if i < other_idx:
                    self.add_edge(i, other_idx, 'OO') # >---< edge
            keyrc = rc(node)[-(self.k-1):]
            for other_idx in self.map[keyrc]:
                if i < other_idx:
                    self.add_edge(i, other_idx, 'II') # <---> edge
        self.map.clear()
        self.maprev.clear()

    def degree(self, node_index, in_or_out):
        return len([l for i,l in self.neighbor[node_index] if l == in_or_out])

    def reverse(self, node_index):
        self.nodes[node_index] = rc(self.nodes[node_index])
        self.neighbor[node_index] = [ (i, 'I' if l == 'O' else 'O') for i,l in self.neighbor[node_index] ]

    def compact(self, i_from, i_to, label):
        # modify the graph to be in the >---> case
        if label == 'IO':
            i_from, i_to = i_to, i_from
        elif label == 'OO':
            self.reverse(i_to)
        elif label == 'II':
            self.reverse(i_from)
       
        # the new compacted node is going to be i_to
        newnode = self.nodes[i_from] + self.nodes[i_to][self.k-1:]
        self.nodes[i_to] = newnode
        for neighbor_idx, neighbor_label in self.neighbor[i_from]:
            label_from_neighbor = self.get_edge_label(neighbor_idx,i_from)
            self.neighbor[neighbor_idx].remove((i_from,label_from_neighbor))
            if neighbor_idx != i_to:
                self.neighbor[neighbor_idx] += [(i_to,label_from_neighbor)]
                self.neighbor[i_to] += [(neighbor_idx, neighbor_label)]

        # i1 is discarded
        del self.nodes[i_from]
        del self.neighbor[i_from]

        if newnode > rc(newnode):
            self.reverse(i_to)

        return i_from

    def compress(self):
        nodes_to_examine = self.nodes.keys()[:]
        while len(nodes_to_examine) > 0:
            node_idx = nodes_to_examine[0]
            compacted = False
            for neighbor_idx, node_label in self.neighbor[node_idx]:
                neighbor_label = self.get_edge_label(neighbor_idx, node_idx)
                label = node_label + neighbor_label
                if self.degree(node_idx, node_label) == 1 and self.degree(neighbor_idx, neighbor_label) == 1:
                    deleted_node = self.compact(node_idx, neighbor_idx, label)
                    nodes_to_examine.remove(deleted_node)
                    compacted = True
                    break
            if not compacted:
                nodes_to_examine.remove(node_idx)
