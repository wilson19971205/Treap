import random
import typing
from collections.abc import Iterator
from typing import List, Optional, cast

from py_treaps.treap import KT, VT, Treap
from py_treaps.treap_node import TreapNode


# Example usage found in test_treaps.py
class TreapMap(Treap[KT, VT]):
    # Add an __init__ if you want. Make the parameters optional, though.
    def __init__(self):
        self.MAX_PRIORITY = 65535
        self.root = None # save root node for the treapmap
        self.remove_value = None # the value to return in remove function

    def get_root_node(self) -> TreapNode:
        # return root node
        return self.root

    def __lookup__(self, node, key: KT):
        # check the node existance first
        if node is None:
            return None
        # when finding the key
        if key == node.key:
            return node.value
        # go left if the key is less than node key
        elif key < node.key:
            return self.__lookup__(node.left_child, key)
        # go right if the key is greater or equal than node key
        else:
            return self.__lookup__(node.right_child, key)

    def lookup(self, key: KT) -> Optional[VT]:
        return self.__lookup__(self.root, key)

    def lookup_node(self, node, key: KT) -> Optional[VT]:
        # same algorithm in __lookup__ function, but return the node for saving
        # the exist key node in the treap, insert into the right treap after split up
        if node is None:
            return None
        if key == node.key:
            return node
        elif key < node.key:
            return self.lookup_node(node.left_child, key)
        else:
            return self.lookup_node(node.right_child, key)

    def right_rotation(self, node):
        L = node.left_child
        LR = node.left_child.right_child
        L.right_child = node
        node.left_child = LR
        return L

    def left_rotation(self, node):
        R = node.right_child
        RL = node.right_child.left_child
        R.left_child = node
        node.right_child = RL
        return R

    def __insert__(self, node, key: KT, value: VT, priority=None):
        # check if we have a root or not, or we get to the leaf and append the treapnode
        # priority is optional, it is used for the split function to append the max priority node
        # and re-append the hold node
        if node is None:
            if priority is None:
                return TreapNode(key, value)
            else:
                node = TreapNode(key, value)
                node.priority = priority
                return node
        if key == node.key:
            node.value = value
            if priority is not None:
                node.priority = priority
        elif key < node.key:
            node.left_child = self.__insert__(node.left_child, key, value, priority)
            if node.left_child and node.left_child.priority > node.priority:
                node = self.right_rotation(node)
        else:
            node.right_child = self.__insert__(node.right_child, key, value, priority)
            if node.right_child and node.right_child.priority > node.priority:
                node = self.left_rotation(node)
        return node

    def insert(self, key: KT, value: VT, priority=None) -> None:
        self.root = self.__insert__(self.root, key, value, priority)

    def __remove__(self, node, key: KT):
        # when the node is not exist
        if node is None:
            return None
        # when the node is exist
        if key == node.key:
            # if the node has no child
            if node.left_child is None and node.right_child is None:
                self.remove_value = node.value
                node = None
            # if the node has two child nodes
            elif node.left_child and node.right_child:
                if node.left_child.priority < node.right_child.priority:
                    node = self.left_rotation(node)
                    node.left_child = self.__remove__(node.left_child, key)
                else:
                    node = self.right_rotation(node)
                    node.right_child = self.__remove__(node.right_child, key)
            # if the node has only one child
            else:
                self.remove_value = node.value
                child = node.left_child if (node.left_child) else node.right_child
                node = child
        # go to the left or right according to the key
        elif key < node.key:
            node.left_child = self.__remove__(node.left_child, key)
        elif key > node.key:
            node.right_child = self.__remove__(node.right_child, key)
        
        return node 

    def remove(self, key: KT) -> Optional[VT]:
        # return the remove node value if exist, else return None
        self.remove_value = None
        self.root = self.__remove__(self.root, key)
        return self.remove_value

    def split(self, threshold: KT) -> "List[Treap[KT, VT]]":
        # save the node if the threshold key node exist
        # if threshold key node exist, remove it
        # insert the threshold key node with MAX_PRIORITY
        # then we got left and right treap
        # insert the hold threshold key node that we save(if exist) to the right treap
        hold = self.lookup_node(self.root, threshold)
        if hold is not None:
            self.remove(threshold)
        self.insert(threshold, str(threshold), self.MAX_PRIORITY)
        left_treap = TreapMap()
        right_treap = TreapMap()
        left_treap.root = self.root.left_child
        right_treap.root = self.root.right_child
        if hold is not None:
            right_treap.insert(hold.key, hold.value, hold.priority)
        return [left_treap, right_treap]

    def join(self, _other: "Treap[KT, VT]") -> None:
        # declare a node with MAX_PRIORITY
        # compare two treap with their root node key to decide which goes to left or right
        # make the self.root = new root
        # reomve the new root to finish join function 
        new_root = TreapNode("new_root", "new_root")
        new_root.priority = self.MAX_PRIORITY
        if self.root.key < _other.root.key:
            new_root.left_child = self.root
            new_root.right_child = _other.root
        else:
            new_root.right_child = self.root
            new_root.left_child = _other.root
        self.root = new_root
        self.remove("new_root")

    def meld(self, other: "Treap[KT, VT]") -> None: # KARMA
        raise AttributeError

    def difference(self, other: "Treap[KT, VT]") -> None: # KARMA
        raise AttributeError

    def balance_factor(self) -> float: # KARMA
        raise AttributeError

    def printTreap(self, root, space):
        # print the treap
        height = 10
        if root is None:
            return
        space += height
        self.printTreap(root.right_child, space)
        for i in range(height, space):
            print(end = " ")
        print((root.value, root.priority))
        self.printTreap(root.left_child, space)

    def __str__(self, root) -> str:
        pass # Your code here

    def iter(self, root):
        # first check if the root exist or not
        # in-order traversal to yield the key in sort order
        if root is None:
            return self
        if root.left_child:
            yield from self.iter(root.left_child)
        yield root.key
        if root.right_child:
            yield from self.iter(root.right_child)
        
    def __iter__(self) -> typing.Iterator[KT]:  
        return self.iter(self.root)
       
    def __next__(self):
        # stop iteration if the root did not exist
        if self.root is not None:
            self.iter(self.root)
        else:
            raise StopIteration
