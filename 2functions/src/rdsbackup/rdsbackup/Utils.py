from collections.abc import Iterable


def multimap(func, it):
    for x in it:
        return (y for y in func(x))


def merge_hash(x, y):
    return {**x, **y}


def foreach(func, it):
    for x in it:
        yield func(x)


def flatten(it):
    for x in it:
        if isinstance(x, Iterable):
            for y in x:
                yield y
        else:
            yield x
