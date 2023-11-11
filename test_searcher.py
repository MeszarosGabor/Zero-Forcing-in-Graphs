import searcher


def test_is_connected_connected():
    G = {
        0: [1,],
        1: [0,],
    }
    assert searcher.is_connected(G) is True


def test_is_connected_disconnected():
    G = {
        0: [1,],
        1: [0,],
        2: [3,],
        3: [2,],
    }
    assert searcher.is_connected(G) is False
