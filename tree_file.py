"""
tree classes
"""

from __future__ import annotations

import csv
# import random
from typing import Any, Optional  # , List


class Tree:
    """A recursive tree data structure.

    Note the relationship between this class and RecursiveList; the only major
    difference is that _rest has been replaced by _subtrees to handle multiple
    recursive sub-parts.

    Representation Invariants:
        - self._root is not None or self._subtrees == []
        - all(not subtree.is_empty() for subtree in self._subtrees)
    """
    # Private Instance Attributes:
    # - _match: The item stored as a tuple with the root as the name and the list of similar clothing types, or None
    #           if the tree is empty.
    # - _subtrees: The list of subtrees of this tree. This attribute is empty when self._root is None
    #           (representing an empty tree). However, this attribute may be empty when self._root is not None,
    #           which represents a tree consisting of just one item.

    '''_root: Optional[Any]
    _clothing: list[str]'''

    _match: tuple[Optional[Any], list[str]] | None
    _subtrees: list[Tree]

    def __init__(self, match: tuple[Optional[Any], list[str]] | None, subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
            - root is not none or subtrees == []
        """
        # self._root = root
        # self.clothing = clothing
        self._match = match
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return whether this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(("PUFFER JACKET", ["tan"]), [])
        >>> t2.is_empty()
        False
        """
        return self._match is None

    def __len__(self) -> int:
        """Return the number of items contained in this tree.

        >>> t1 = Tree(None, [])
        >>> len(t1)
        0
        >>> t2 = Tree(("PUFFER JACKET", ["tan"]), [Tree(("TUXEDO", ["black", "silk"]), []), Tree(("COAT", ["grey"]), [])])
        >>> len(t2)
        3
        """
        if self.is_empty():
            return 0
        else:
            size = 1  # count the root
            for subtree in self._subtrees:
                size += subtree.__len__()  # could also write len(subtree)
            return size

    def __contains__(self, item: Any) -> bool:
        """Return whether the given is in this tree.

        >>> t = Tree(("PUFFER JACKET", ["tan"]), [Tree(("TUXEDO", ["black", "silk"]), [])])
        >>> t.__contains__(("PUFFER JACKET", ["tan"]))
        True
        >>> t.__contains__(("TUXEDO", ["black", "cotten"]))
        False
        >>> t.__contains__(("TUXEDO", ["black"]))
        True
        """
        # if self.is_empty():
        #     return False
        # elif self._root == item:
        #     return True
        # else:
        #     for subtree in self._subtrees:
        #         if subtree.__contains__(item):
        #             return True
        #     return False

    # def __str__(self) -> str:
    #     """Return a string representation of this tree.
    #
    #     For each node, its item is printed before any of its
    #     descendants' items. The output is nicely indented.
    #
    #     You may find this method helpful for debugging.
    #     """
    #     return self._str_indented(0).rstrip()

    # def _str_indented(self, depth: int) -> str:
    #     """Return an indented string representation of this tree.
    #
    #     The indentation level is specified by the <depth> parameter.
    #     """
    #     if self.is_empty():
    #         return ''
    #     else:
    #         str_so_far = '  ' * depth + f'{self._root}\n'
    #         for subtree in self._subtrees:
    #             # Note that the 'depth' argument to the recursive call is
    #             # modified.
    #             str_so_far += subtree._str_indented(depth + 1)
    #         return str_so_far

    def matching_clothing(self, ) -> bool:
        """
        It will compare the clothing style to show similarity.
        """

    def remove(self, item: Any) -> bool:
        """Delete *one* occurrence of the given item from this tree.

        Do nothing if the item is not in this tree.
        Return whether the given item was deleted.
        """
        if self.is_empty():
            return False
        elif self._root == item:
            self._delete_root()  # delete the root
            return True
        else:
            for subtree in self._subtrees:
                deleted = subtree.remove(item)
                if deleted and subtree.is_empty():
                    # The item was deleted and the subtree is now empty.
                    # We should remove the subtree from the list of subtrees.
                    # Note that mutate a list while looping through it is
                    # EXTREMELY DANGEROUS!
                    # We are only doing it because we return immediately
                    # afterward, and so no more loop iterations occur.
                    self._subtrees.remove(subtree)
                    return True
                elif deleted:
                    # The item was deleted, and the subtree is not empty.
                    return True

            # If the loop doesn't return early, the item was not deleted from
            # any of the subtrees. In this case, the item does not appear
            # in this tree.
            return False

    def _delete_root(self) -> None:
        """Remove the root item of this tree.

        Preconditions:
            - not self.is_empty()
        """
        if not self._subtrees:
            self._root = None
        else:
            # Strategy: Promote a subtree (the rightmost one is chosen here).
            # Get the last subtree in this tree.
            last_subtree = self._subtrees.pop()

            self._root = last_subtree._root
            self._subtrees.extend(last_subtree._subtrees)
