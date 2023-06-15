from pool import Pooling


def test_three():
    data = Pooling.get_pool_data("user")
    assert data["name"] == "James"


def test_four():
    data = Pooling.get_pool_data("user")
    assert data["name"] == "Lindy"
