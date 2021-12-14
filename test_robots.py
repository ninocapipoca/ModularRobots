from reduce import reduce
from checks import check_connected

def test_reduce():
    M = [[0,0,0,0],
        [0,1,0,0],
        [0,0,1,0]]
    print(reduce(M))
    M = [[0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]]
    print(reduce(M))


def test_connected():
    M = [[0,0,0,0],
        [0,1,0,0],
        [0,0,1,0]]
    assert not check_connected(M)
    M = [[0,0,0,0],
        [0,1,1,0],
        [0,0,1,0]]
    assert check_connected(M)