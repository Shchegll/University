# test_pdb.py
def integers_counter(data):
    integers_found = 0
    for item in data:
        if not isinstance(item, bool) and isinstance(item, int):
            integers_found += 1
    return integers_found


def test_counter():
    data = [False, 1.0, "some_string", 3, True, 1, [], False]
    integers = integers_counter(data)
    assert integers == 2
