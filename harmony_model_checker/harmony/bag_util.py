def bag_add(bag, item):
    cnt = bag.get(item)
    if cnt is None:
        bag[item] = 1
    else:
        bag[item] = cnt + 1

def bag_remove(bag, item):
    cnt = bag[item]
    assert cnt > 0
    if cnt == 1:
        del bag[item]
    else:
        bag[item] = cnt - 1