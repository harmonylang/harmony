class HDict:

    def __init__(self, dict):
        self._dict = dict

    def __contains__(self, item):
        return self._dict.__contains__(item)

    def __getitem__(self, item):
        return self._dict.__getitem__(item)

    def __setitem__(self, key, value):
        self._dict.__setitem__(key, value)

    def __iter__(self):
        return self._dict.__iter__()

    def __len__(self):
        return self._dict.__len__()

    def __call__(self, item):
        return self._dict.__getitem__(item)

class Ref:

    def __init__(self, pointee):
        self.pointee = pointee
