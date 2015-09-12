from collections import OrderedDict
from pprint import pprint


def deep_compare(a, b, pointer='/'):
    if a == b:
        return

    if type(a) != type(b):
        reason = 'Different data types'
        extra = str((type(a), type(b)))
        x(pointer, reason, extra)

    elif type(a) in (set, frozenset):
        pointer += 'set()'
        if len(a) != len(b):
            pointer += 'set()'
            reason = 'Different number of items'
            extra = str((len(a), len(b)))
            x(pointer, reason, extra)

        reason = 'Different items'
        extra = (a, b)
        x(pointer, reason, extra)

        for i in range(len(a)):
            deep_compare(a[i], b[i], pointer + 'set()'.format(i))

    elif type(a) in (list, tuple):
        if len(a) != len(b):
            pointer += '[]'
            reason = 'Different number of items'
            extra = str((len(a), len(b)))
            x(pointer, reason, extra)

        if sorted(a) == sorted(b):
            pointer += '[]'
            reason = 'Different sort order'
            extra = 'N/A'
            x(pointer, reason, extra)

        for i in range(len(a)):
            deep_compare(a[i], b[i], pointer + '[{}]'.format(i))

    elif type(a) in (dict, OrderedDict):
        if len(a) != len(b):
            pointer += '{}'
            reason = 'Different number of items'
            extra = str((len(a), len(b)))
            x(pointer, reason, extra)

        if set(a.keys()) != set(b.keys()):
            pointer += '{}'
            reason = 'Different keys'
            extra = (a.keys(), b.keys())
            x(pointer, reason, extra)

        for k in a:
            deep_compare(a[k], b[k], pointer + '[{}]'.format(k))
    else:
        reason = 'Different objects'
        extra = (a, b)
        x(pointer, reason, extra)


def x(pointer, reason, extra):
    message = 'Objects are not the same. Pointer: {}. Reason: {}. Extra: {}'
    raise RuntimeError(message.format(pointer, reason, extra))


def compare(a, b):
    try:
        deep_compare(a, b, '/')
    except RuntimeError as e:
        pprint(e.message)
