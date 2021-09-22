import sys
import math
import csv
import pickle

class Node(object):
    def __init__(self, parent=None):
        self.keys = []
        self.values = []
        self.parent = parent

    def index(self, key):
        for idx, item in enumerate(self.keys):
            if item > key:
                return idx
        return len(self.keys)

    def tostring(self):
        return ', '.join(str(x) for x in self.keys)

    def isfull(self, maximum):
        return len(self.keys) >= int(maximum)

    def nodeinsert(self, key, value):
        i = self.index(key)
        self.keys.insert(i, key)
        self.values.insert(i+1, value)


    def borrow(self,i, prevornext):
        if prevornext=='prev':
            prevnode=self.parent.values[i-1]
            key=prevnode.keys.pop()
            value=prevnode.values.pop()
            value.parent=self
            self.keys.insert(0, self.parent.keys[i-1])
            self.values.insert(0, value)
            self.parent.keys[i-1]=key

        if prevornext=='next':
            nextnode=self.parent.values[i+1]
            key=nextnode.keys.pop(0)
            value=nextnode.values.pop(0)
            value.parent=self
            self.keys.append(self.parent.keys[i])
            self.values.append(value)
            self.parent.keys[i]=key

        return self.parent
    def merge(self, idx, prevornext):

        if prevornext=='prev':
            prevnode=self.parent.values[idx-1]
            for value in self.values:
                value.parent=prevnode
            prevnode.keys.append(self.parent.keys[idx-1])
            prevnode.keys.extend(self.keys)
            prevnode.values.extend(self.values)
            del self.parent.keys[idx-1]
            del self.parent.values[idx]

            return prevnode.parent
        if prevornext=='next':
            nextnode=self.parent.values[idx+1]
            for value in nextnode.values:
                value.parent=self
            self.keys.append(self.parent.keys.pop(idx))
            self.keys.extend(nextnode.keys)
            self.values.extend(nextnode.values)

        return self.parent

    def split(self):
        mid =math.ceil(len(self.keys)/2)
        right = Node(self.parent)
        right.keys = self.keys[mid:]
        right.values=self.values[mid:]
        key=self.keys[mid-1]

        for child in right.values:
            child.parent = right

        self.keys = self.keys[:mid-1]
        self.values = self.values[:mid]
        return key, right




class Leaf(Node):
    def __init__(self, parent = None, next_node=None, prev_node=None):
        super().__init__(parent)
        self.next = next_node
        self.prev = prev_node
        if next_node:
            next_node.prev=self
        if prev_node:
            prev_node.next=self

    def leafinsert(self, key, value):
        i = super().index(key)
        self.keys.insert(i, int(key))
        self.values.insert(i, value)

    def delete(self, key):
        i = self.keys.index(key)
        delkey=self.keys.pop(i)
        delvalue=self.values.pop(i)
        return i, delkey, delvalue


    def borrow(self, prevornext):
        if prevornext=='prev':
            replacekey=self.keys[0]
            key = self.prev.keys.pop()
            value = self.prev.values.pop()
            self.leafinsert(key, value)
            return replacekey, key
        if prevornext=='next':
            replacekey=self.next.keys.pop(0)
            key=self.next.keys[0]
            self.leafinsert(replacekey, self.next.values.pop(0))
            return replacekey, key

    def merge(self, prevornext):
        if prevornext=='prev':
            self.prev.keys.extend(self.keys)
            self.prev.values.extend(self.values)
            self.prev.next=self.next
            if self.next:
                self.next.prev=self.prev
            if self.parent:
                idx = self.parent.values.index(self)
                parentnode=self.parent
                del self.parent.keys[idx-1]
                del self.parent.values[idx]

        if prevornext=='next':
            self.keys.extend(self.next.keys)
            self.values.extend(self.next.values)
            if self.next:
                self.next=self.next.next
            if self.next and self.next.next:
                self.next.next.prev=self
            if self.parent:
                idx=self.parent.values.index(self)
                parentnode=self.parent
                del self.parent.keys[idx]
                del self.parent.values[idx+1]

        return parentnode

    def leafsplit(self):
        mid = math.ceil(len(self.keys)/2)
        right = Leaf(self.parent, self.next, self)
        right.keys = self.keys[mid:]
        right.values = self.values[mid:]
        self.keys=self.keys[:mid]
        self.values=self.values[:mid]
        self.next=right
        return right.keys[0], right


class Bplustree(object):
    def __init__(self, degree):
        self.root=Leaf()
        self.degree = int(degree)
        self.leafminimum = math.ceil((self.degree-1)/2)
        self.nodeminimum = math.ceil(self.degree/2)

    def findleaf(self, key, singlekeysearch=None):
        node = self.root
        while not isinstance(node, Leaf):
            if singlekeysearch:
                print(node.tostring())
            node = node.values[node.index(key)]
        return node
    def replace(self, replacekey, key):
        node=self.root
        while replacekey not in node.keys:
            node = node.values[node.index(replacekey)]
            if isinstance(node, Leaf):
                return
        node.keys[node.keys.index(replacekey)]=key

    def ismin(self, node):
        if isinstance(node, Leaf):
            if node == self.root:
                return False
            else:
                return len(node.keys) < self.leafminimum
        if node == self.root:
            return len(node.values) < 2
        return len(node.values) < self.nodeminimum

    def rangedsearch(self, start, end):
        leaf=self.findleaf(start)
        while True:
            try:
                for key, value in zip(leaf.keys, leaf.values):
                    if (key>=int(start) and key<=int(end)):
                        print(key, value, sep=', ')
                leaf=leaf.next
            except:
                break

    def merge(self, leaf, prevornext):
        node=leaf.merge(prevornext)
        while self.ismin(node) and node is not self.root:
            prevornext, k = self.prevornext(node)
            if prevornext=='prev':
                if len(node.parent.values[k-1].keys)+len(node.keys) >= self.degree:
                    node=node.borrow(k,prevornext)
                else:
                    node=node.merge(k, prevornext)
            if prevornext=='next':
                if len(node.parent.values[k+1].keys)+len(node.keys) >= self.degree:
                    node=node.borrow(k, prevornext)
                else:
                    node=node.merge(k, prevornext)

    def prevornext(self, node):
        if node is self.root:
            return
        idx=node.parent.values.index(node)
        if idx==0:
            return 'next', idx
        elif idx == len(node.parent.values)-1:
            return 'prev', idx
        elif len(node.parent.values[idx-1].keys) >= len(node.parent.values[idx+1].keys):
            return 'prev', idx
        else:
            return 'next', idx

    def borrow(self, leaf, prevornext):
        replacekey, key = leaf.borrow(prevornext)
        self.replace(replacekey, key)

    def deletion(self, key):
        leaf = self.findleaf(key)
        i, delkey, delvalue = leaf.delete(key)
        if i==0:
            if len(leaf.keys)==0:
                return
            self.replace(delkey, leaf.keys[0])
        if self.ismin(leaf) and leaf is not self.root:
            prevornext, idx=self.prevornext(leaf)
            if prevornext == 'prev':
                if len(leaf.prev.keys)+len(leaf.keys) >= self.degree:
                    self.borrow(leaf, prevornext)
                else:
                    self.merge(leaf, prevornext)
            if prevornext == 'next':
                if len(leaf.next.keys)+len(leaf.keys) >= self.degree:
                    self.borrow(leaf, prevornext)
                else:
                    self.merge(leaf, prevornext)


    def treeinsert(self, key, value):
        leaf=self.findleaf(key)
        leaf.leafinsert(key, value)
        node = leaf
        while node.isfull(self.degree):
            if isinstance(node, Leaf):
                upkey, upvalue = node.leafsplit()
            else:
                upkey, upvalue = node.split()

            if not node.parent:
                node.parent = Node()
                upvalue.parent = node.parent
                node.parent.values.append(node)
                self.root = node.parent

            node.parent.nodeinsert(upkey,upvalue)
            node=node.parent


def creation(filename, degree):
    tree=Bplustree(int(degree))
    with open(filename, 'wb') as file:
        pickle.dump(tree, file)

def insertion(tree, key, value):
    tree.treeinsert(int(key), int(value))

def singlekeysearch(filename, key):
    with open(filename, 'rb') as file:
        tree=pickle.load(file)
        leaf = tree.findleaf(int(key), True)
        print(leaf.values[leaf.keys.index(int(key))])

def rangedsearch(filename, start, end):
    with open(filename, 'rb') as file:
        tree=pickle.load(file)
        tree.rangedsearch(int(start), int(end))

def deletion(tree, key):
    tree.deletion(int(key))


if __name__ == '__main__':
    if sys.argv[1] == '-c':
        creation(sys.argv[2], sys.argv[3])
    if sys.argv[1] == '-s':
        singlekeysearch(sys.argv[2], sys.argv[3])
    if sys.argv[1] == '-i':
        with open(sys.argv[2], 'rb') as file:
            tree=pickle.load(file)
        with open(sys.argv[3], 'r') as file2:
            reader=csv.reader(file2)
            for key, value in reader:
                insertion(tree,key, value)
        with open(sys.argv[2], 'wb') as file:
            pickle.dump(tree, file)
    if sys.argv[1] == '-r':
        rangedsearch(sys.argv[2], sys.argv[3], sys.argv[4])
    if sys.argv[1] == '-d':
        with open(sys.argv[2], 'rb') as file:
            tree=pickle.load(file)
        with open(sys.argv[3], 'r') as file2:
            reader=csv.reader(file2)
            for key in reader:
                deletion(tree, key[0])
        with open(sys.argv[2], 'wb') as file:
            pickle.dump(tree, file)











