# A dictionary where the keys are tuples ``(lower_bound, upper_bound)``. Items are returned if
# ``lower_bound <= item < upper_bound``.  This allows one to build a dictionary where the keys are "float ranges".
class FloatRangeDict(dict):
    def __getitem__(self, item):
        if type(item) != tuple:
            for key in self:
                if item >= key[0] and item < key[1]:
                    return self[key]
            raise KeyError(item)
        else:
            return super().__getitem__(item)
