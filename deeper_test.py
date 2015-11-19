from collections import OrderedDict
import copy
from unittest import TestCase
from datetime import datetime

import sys

from deeper import deep_compare, deep_getsizeof


class DeeperTest(TestCase):
    def test_same_data_structures(self):
        a = dict(a=[1,2,3],
                 b={4, 5, 6, (7, 8, 9)},
                 c=['123', datetime.now()])
        b = copy.deepcopy(a)
        deep_compare(a, b)

    def _test(self, a, b, expected):
        try:
            deep_compare(a, b)
            self.fail('Should never get here')
        except RuntimeError as e:
            self.assertEqual(expected, e.message)

    def test_diff_object_types(self):
        expected = ("Objects are not the same. Pointer: /. "
                    "Reason: Different data types. "
                    "Extra: (<type 'int'>, <type 'str'>)")
        self._test(4, '5', expected)

    def test_diff_objects(self):
        expected = ('Objects are not the same. Pointer: /. '
                    'Reason: Different objects. Extra: (4, 5)')
        self._test(4, 5, expected)

    def test_diff_sets(self):
        expected = ('Objects are not the same. Pointer: /set(). '
                    'Reason: Different items. '
                    'Extra: (set([1]), set([5]))')
        self._test({1}, {5}, expected)

    def test_diff_lists(self):
        expected = ('Objects are not the same. Pointer: /[]. '
                    'Reason: Different number of items. Extra: (0, 2)')
        self._test([], [1,2], expected)

        expected = ('Objects are not the same. Pointer: /[]. '
                    'Reason: Different sort order. Extra: N/A')
        self._test([2, 1], [1,2], expected)

        expected = ('Objects are not the same. Pointer: /[1]. '
                    'Reason: Different objects. Extra: (2, 3)')
        self._test([1, 2, 4], [1, 3, 4], expected)

    def test_diff_tuples(self):
        expected = ('Objects are not the same. Pointer: /[]. '
                    'Reason: Different number of items. Extra: (0, 2)')
        self._test((), (1,2), expected)

        expected = ('Objects are not the same. Pointer: /[]. '
                    'Reason: Different Sort Order. Extra: N/A')
        self._test((2, 1), (1,2), expected)

        expected = ('Objects are not the same. Pointer: /[1]. '
                    'Reason: Different objects. Extra: (2, 3)')
        self._test((1, 2, 4), (1, 3, 4), expected)

    def test_diff_dicts(self):
        expected = ('Objects are not the same. Pointer: /{}. '
                    'Reason: Different number of items. Extra: (0, 1)')
        self._test({}, dict(a=1), expected)

        expected = ("Objects are not the same. Pointer: /{}. "
                    "Reason: Different keys. Extra: (['a'], ['b'])")
        self._test(dict(a=1), dict(b=1), expected)

        expected = ('Objects are not the same. Pointer: /[a]. '
                    'Reason: Different objects. Extra: (1, 2)')
        self._test(dict(a=1), dict(a=2), expected)

    def test_diff_nested_sets(self):
        expected = ('Objects are not the same. Pointer: /[2]set(). '
                    'Reason: Different items. '
                    'Extra: (set([1]), set([5]))')
        self._test([4, 6, {1}, 7], [4, 6, {5}, 7], expected)

    def test_diff_nested_lists(self):
        expected = ('Objects are not the same. Pointer: /[x][]. '
                    'Reason: Different number of items. Extra: (0, 2)')
        self._test(dict(x=[]), dict(x=[1,2]), expected)

        expected = ('Objects are not the same. Pointer: /[x][]. '
                    'Reason: Different sort order. Extra: N/A')
        self._test(dict(x=[2, 1]), dict(x=[1,2]), expected)

        expected = ('Objects are not the same. Pointer: /[x][1]. '
                    'Reason: Different objects. Extra: (2, 3)')
        self._test(dict(x=[1, 2, 4]), dict(x=[1, 3, 4]), expected)

    def test_diff_nested_tuples(self):
        expected = ('Objects are not the same. Pointer: /[x][]. '
                    'Reason: Different number of items. Extra: (0, 2)')
        self._test(dict(x=()), dict(x=(1,2)), expected)

        expected = ('Objects are not the same. Pointer: /[x][]. '
                    'Reason: Different sort order. Extra: N/A')
        self._test(dict(x=(2, 1)), dict(x=(1,2)), expected)

        expected = ('Objects are not the same. Pointer: /[x][1]. '
                    'Reason: Different objects. Extra: (2, 3)')
        self._test(dict(x=(1, 2, 4)), dict(x=(1, 3, 4)), expected)

    def test_diff_nested_dicts(self):
        expected = ('Objects are not the same. Pointer: /[x]{}. '
                    'Reason: Different number of items. Extra: (0, 1)')
        self._test(dict(x={}), dict(x=dict(a=1)), expected)

        expected = ("Objects are not the same. Pointer: /[x]{}. "
                    "Reason: Different keys. Extra: (['a'], ['b'])")
        self._test(dict(x=dict(a=1)), dict(x=dict(b=1)), expected)

        expected = ('Objects are not the same. Pointer: /[x][a]. '
                    'Reason: Different objects. Extra: (1, 2)')
        self._test(dict(x=dict(a=1)), dict(x=dict(a=2)), expected)

    def test_diff_complex(self):
        a = [frozenset([1, 2, 3, (4, 5, 6)]),
             dict(a=1, b=2, c=OrderedDict([('first', 1), ('second', 2)])),
             ('a', 'b', 8, 9)]

        # Case 1
        b = copy.deepcopy(a)
        b[0] = frozenset([1, 2, 3, (4,5,6, 7)])
        expected = ('Objects are not the same. Pointer: /[0]set(). '
                    'Reason: Different items. Extra: ('
                    'frozenset([1, 2, 3, (4, 5, 6)]), '
                    'frozenset([1, 2, 3, (4, 5, 6, 7)]))')
        self._test(a, b, expected)

        # Case 2
        b = copy.deepcopy(a)
        b[1]['c']['first'] = 3

        expected = ('Objects are not the same. Pointer: /[1][c][first]. '
                    'Reason: Different objects. Extra: (1, 3)')
        self._test(a, b, expected)

    def test_deep_getsizeof(self):
        g = sys.getsizeof
        d = deep_getsizeof

        data = 5
        s1 = g(data)
        s2 = d(data, set())
        self.assertEqual(s1, s2)

        data = 8.9945
        s1 = g(data)
        s2 = d(data, set())
        self.assertEqual(s1, s2)

        data = ''
        s1 = g(data)
        s2 = d(data, set())
        self.assertEqual(s1, s2)

        data = 'abcd'
        s1 = g(data)
        s2 = d(data, set())
        self.assertEqual(s1, s2)

        data = ()
        s1 = g(data)
        s2 = d(data, set())
        self.assertEqual(s1, s2)

        data = []
        s1 = g(data)
        s2 = d(data, set())
        self.assertEqual(s1, s2)

        data = set()
        s1 = g(data)
        s2 = d(data, set())
        self.assertEqual(s1, s2)

        data = {}
        s1 = g(data)
        s2 = d(data, set())
        self.assertEqual(s1, s2)

        data = [1, 2, 3, 4]
        s1 = g(data) + 4 * g(1)
        s2 = d(data, set())
        self.assertEqual(s1, s2)

        # Object counted once when repeated (the integer 1)
        data = [1, 1, 1, 1]
        s1 = g(data) + g(1)
        s2 = d(data, set())
        self.assertEqual(s1, s2)

        data = dict(a=dict(b=1, c=[2,3]))
        self.assertEqual(834, d(data, set()))







