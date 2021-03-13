def contains(array, item):
    '''Type-safe approach to checking if an object contains another.
    This is intended for arrays, but falls back to equals for strings.
    For arrays, it uses the "in" operator to check for the presence of
    a specific item.
    If array or item is null, or the type of array isn't str or list,
    this returns false. Otherwise, it checks for the type, and runs an
    appropriate comparison and returns the result.
    '''

    if item is None or array is None:
        return False
    elif type(array) is list:
        return item in array
    elif type(array) is str:
        return item == array

    return False


def contains_fuzzy(array, item):
    '''Type safe contains method.
    Does the same as contains, except it uses "in" to check
    for matches instead of requiring an exact match.
    '''

    if item is None or array is None:
        return False
    elif type(array) is list:
        for a in array:
            if a in item:
                return True
        return False
    elif type(array) is str:
        return item in array

    return False
