from py_treaps.treap_map import TreapMap

import pytest
from typing import Any

# This file includes some starter test cases that you can use
# as a template to test your code and write your own test cases.
# You should write more tests; passing the following tests is
# NOT sufficient to guarantee that your code works.
# For example, there is no test for join(). You should write some.
# Be sure to read the test cases carefully.

def test_empty_lookup() -> None:
    """Test `lookup` on an empty Treap."""

    treap: TreapMap[Any, Any] = TreapMap()

    assert not treap.lookup(6)
    assert not treap.lookup(0)
    assert not treap.lookup("hi")


def test_single_insert() -> None:
    """Test minimal insert/lookup functionality."""

    treap: TreapMap[int, str] = TreapMap()
    treap.insert(1, "one")

    assert treap.lookup(1) == "one"


def test_multiple_insert() -> None:
    """Test the insertion and lookup of multiple elements."""

    treap: TreapMap[int, str] = TreapMap()
    N = 21

    for i in range(N):
        treap.insert(i, str(i))
        assert treap.lookup(i) == str(i)

    # make sure all nodes are still there
    for i in range(N):
        assert treap.lookup(i) == str(i)


def test_insert_overwrite() -> None:
    """Test whether multiple insertions to the same key overwrites
    the value.
    """

    treap: TreapMap[int, str] = TreapMap()
    for i in range(10):
        treap.insert(i, str(i))

    for value in ("hi", "foo", "bar"):
        treap.insert(2, value)
        assert treap.lookup(2) == value


def test_empty_remove() -> None:
    """Test `remove` on an empty Treap."""

    treap: TreapMap[str, int] = TreapMap()
    assert treap.remove("hi") is None


def test_iterator_exception() -> None:
    """Test that the TreapMap iterator raises a StopIteration
    when exhausted.
    """
    treap: TreapMap[int, str] = TreapMap()

    it = iter(treap)
    with pytest.raises(StopIteration):
        next(it)


def test_split_by_median() -> None:
    """Test `split` with the median key."""

    original_treap = TreapMap()
    for i in range(11):
        original_treap.insert(i, str(i))
    new_treaps = original_treap.split(5)
    left = new_treaps[0]
    right = new_treaps[1]
    a1 = [0,1,2,3,4]
    a2 = [5,6,7,8,9,10]
    count = 0
    for key in left:
        assert a1[count] == key
        count += 1
        assert 0 <= key < 5
    count = 0
    for key in right:
        assert a2[count] == key
        count += 1
        assert 5 <= key < 11
    for i in range(5, 11):
        assert right.lookup(i) == str(i)
    new_treaps = left.join(right)
    #new_treaps = right.join(left)


def test_get_root_node() -> None:
    """Test that the root node works as expected"""

    t = TreapMap()
    for i in range(10):
        t.insert(i, i)
    root_node = t.get_root_node()
    assert root_node.key in list(range(10))
    assert root_node.value in list(range(10))
    assert root_node.parent is None
    assert root_node.left_child is not None or root_node.right_child is not None


def test_heap_property_simple() -> None:
    """Test heap property in a basic way"""

    for _ in range(50):  # Run this test a bunch to account for randomness
        t = TreapMap()
        for i in range(10):
            t.insert(str(i), str(i))
        root_node = t.get_root_node()

        # Is this sufficient to test the heap property?

        if (
            root_node.key != "0"
        ):  # why does this if statement exist? What if you remove it?
            assert root_node.priority >= root_node.left_child.priority
        if root_node.key != "9":
            assert root_node.priority >= root_node.right_child.priority


def test_bst_property_simple() -> None:
    """Test BST property in a basic way"""

    for _ in range(50):  # Run this test a bunch to account for randomness
        t = TreapMap()
        for i in range(10):
            t.insert(str(i), str(i))
        root_node = t.get_root_node()

        # Is this sufficient to test the BST property?

        if root_node.key != "0":
            assert root_node.value >= root_node.left_child.value
        if root_node.key != "9":
            assert root_node.value <= root_node.right_child.value