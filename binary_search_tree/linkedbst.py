"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log, inf


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node is not None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self.
        Algorithm Preorder(tree)
        1. Visit the root.
        2. Traverse the left subtree, i.e., call Preorder(left-subtree)
        3. Traverse the right subtree, i.e., call Preorder(right-subtree)

        Shorter: Root - Left - Right or RAB
                 R (root)
                /        \
            A (left)  B (right)
        """

        lyst = list()

        def recurse(node):
            if node is not None:
                lyst.append(node.data)
                recurse(node.left)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def inorder(self):
        """Supports an inorder traversal on a view of self.
        Algorithm Inorder(tree)
        1. Traverse the left subtree, i.e., call Inorder(left-subtree)
        2. Visit the root.
        3. Traverse the right subtree, i.e., call Inorder(right-subtree)

        Shorter: Left - Root - Right or ARB
                 R (root)
                /        \
            A (left)  B (right)
        """
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self.
        Algorithm Postorder(tree)
        1. Traverse the left subtree, i.e., call Postorder(left-subtree)
        2. Traverse the right subtree, i.e., call Postorder(right-subtree)
        3. Visit the root.

        Shorter: Left - Right - Root or ABR
                 R (root)
                /        \
            A (left)  B (right)
        """
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                recurse(node.right)
                lyst.append(node.data)

        recurse(self._root)
        return iter(lyst)

    def levelorder(self):
        """Supports a levelorder traversal on a view of self
        A demonstration of levelorder traversal
               1
              / \
             2   3     numbers in nodes ==
            / \   \    order in which the node is
           4   5   6   visited during levelorder traversal
          /   /     \
         7   8       9
        """

        lyst = list()

        def recurse(node, nodelevel=0, level=0):
            if level < nodelevel or node is None:
                return
            elif level == nodelevel:
                lyst.append(node.data)
            else:
                recurse(node.left, nodelevel+1, level)
                recurse(node.right, nodelevel+1, level)

        for i in range(self.height()+1):
            recurse(self._root, level=i)
        return iter(lyst)

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while currentNode.right is not None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while currentNode is not None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved is None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left is None \
                and currentNode.right is not None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left is None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''

            if top is None:
                return -1
            return max(height1(top.left), height1(top.right))+1

        return height1(self._root)

    def isBalanced(self):
        '''
        Return True if tree is balanced
        :return:
        2 * log2(n + 1) - 1
        '''

        height = self.height()
        n = 0
        for _ in self:
            n += 1
        return height < 2*log(n+1, 2)

    def rangeFind(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        found = list()
        for i in self:
            if low <= i <= high:
                found.append(i)
        return found

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''

        nodes = list()
        for i in self:
            nodes.append(i)
        nodes.sort()

        def helper(tree, nodes, i_start, i_end):
            if not (i_start+1 < i_end):
                return
            middle = (i_start+i_end)//2
            tree.add(nodes[middle])
            helper(tree, nodes, middle, i_end)
            helper(tree, nodes, i_start, middle)
        self.clear()
        helper(self, nodes, 0, len(nodes))

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        '''
        successor = inf
        for i in self:
            if i > item:
                successor = min(successor, i)
        return successor if successor is not inf else None
        '''
        def recurse(node, item, min_larger=inf):
            if node is None:
                return min_larger
            if node.data > item:
                return min(node.data, recurse(node.left, item), min_larger)
            else:
                return min(recurse(node.right, item), min_larger)

        successor = recurse(self._root, item)
        successor = None if successor is inf or\
                    successor <= item else successor
        return successor

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        '''
        predecessor = -inf
        for i in self:
            if i < item:
                predecessor = max(predecessor, i)
        return predecessor if predecessor is not -inf else None
        '''
        def recurse(node, item, max_greater=-inf):
            if node is None:
                return max_greater
            if node.data < item:
                return max(node.data, recurse(node.right, item), max_greater)
            else:
                return max(recurse(node.left, item), max_greater)

        predecessor = recurse(self._root, item)
        predecessor = None if predecessor == -inf or\
            predecessor >= item else predecessor
        return predecessor


if __name__ == '__main__':
    tree = LinkedBST()
    print('Creating a tree like this: ')
    contents = [10, 3, 2, 5, 14, 15, 9, 11, 1, 7, 8, 4, 12, 6, 13]
    print('The tree shold be:')
    print('''       10\n      /  \\\n     /    \\\n    3      14
   / \    /  \\\n  2   5  11   15\n /   / \   \\\n1   4   9   12    
       /      \\\n      7       13\n     / \\\n    6   8\n''')
    for i in contents:
        tree.add(i)
    print('Standart representation of the LinkedBTS class:')
    print(tree)
    print("\n\ninorder traversal: ", end="")
    for item in tree.inorder():
        print(item, end=" ")

    print("\n\npreorder traversal: ", end="")
    for item in tree.preorder():
        print(item, end=" ")

    print("\n\npostorder traversal: ", end="")
    for item in tree.postorder():
        print(item, end=" ")

    print("\n\nlevelorder traversal: ", end="")
    for item in tree.levelorder():
        print(item, end=" ")

    print('\nSuccessor test')
    print('successor -5', tree.successor(-5))
    print('successor 18', tree.successor(18))
    print('successor 7', tree.successor(7))
    print('\nPredecessor test')
    print('predecessor -5', tree.predecessor(-5))
    print('predecessor 18', tree.predecessor(18))
    print('predecessor 7', tree.predecessor(7))

    print('\n\nTest finished!')
