import collections

from collections import UserDict


class PrefixDict(UserDict):
    # noinspection PyMissingConstructor
    def __init__(self):
        self.data = collections.OrderedDict()

    def keys(self):
        return self.data.keys()

    def items(self):
        return self.data.items()

    def values(self):
        return self.data.values()

    def clear(self):
        self.data.clear()

    def __getitem__(self, key):
        longest_prefix = None
        for stored_key in self.data:
            if key.startswith(stored_key):
                if longest_prefix is None or len(stored_key) > len(longest_prefix):
                    longest_prefix = stored_key

        if longest_prefix is not None:
            return self.data[longest_prefix]
        else:
            raise KeyError(f"No matching prefix found for key: {key}")

    def __contains__(self, key):
        return any(key.startswith(stored_key) for stored_key in self.data)

    def __repr__(self):
        return f"PrefixDict({self.data})"
