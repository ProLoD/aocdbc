"""
Add an operation ``split`` to the linked list from Exercise 6, Problem 4.

The operation ``split`` takes in an argument ``n`` and removes all the items from the
list which are greater-equal ``n``.

The operation creates an additional list and inserts in it all the removed elements
(in the same order as in the original list). The resulting second list is finally
returned to the caller.

(The original problem statements includes an additional requirement that the caller
should be able to iterate over the original list by adding extra pointers ``old_next``
to the original nodes. We deliberately remove this part of the problem as it introduces,
in our opinion, complexity in the code with no or only marginal insights about
the nature of the code contracts).
"""
from typing import List

from correct_programs.ethz_eprog_2019.exercise_06.problem_04 import LinkedList

from icontract import require, ensure, snapshot


@require(lambda lst, old_values: len(lst) <= len(old_values))
def same_order(lst: List[int], old_values: List[int]) -> bool:
    """Check that the values in ``lst`` follow the order of the ``old_values``."""
    if len(lst) == 0:
        return True

    cur = 0
    for value in old_values:
        if value != lst[cur]:
            continue

        cur += 1
        if cur == len(lst):
            return True

    return cur == len(lst)


@snapshot(lambda lst: lst.count(), name="count")
@snapshot(lambda lst: list(lst.values()), name="values")
@ensure(lambda result, OLD: same_order(list(result.values()), OLD.values))
@ensure(lambda lst, OLD: same_order(list(lst.values()), OLD.values))
# ERROR:
# icontract.errors.ViolationError:
# all(value < n for value in lst.values()):
# all(value < n for value in lst.values()) was False
# lst was <correct_programs.ethz_eprog_2019.exercise_06.problem_04.LinkedList object at 0x000002921B159C70>
# lst.values() was <generator object LinkedList.values at 0x000002921B0DABA0>
#
# A value has not been removed properly.
@ensure(lambda lst, n: all(value < n for value in lst.values()))
@ensure(lambda result, n: all(value >= n for value in result.values()))
@ensure(
    lambda lst, result, OLD: lst.count() + result.count() == OLD.count
)
def split(lst: LinkedList, n: int) -> LinkedList:
    result = LinkedList()

    cursor = lst.cursor()

    while not cursor.done():
        value = cursor.value()
        if value >= n:
            result.add_last(value)
            cursor.remove()

        if not cursor.done():
            cursor.move()

    return result
