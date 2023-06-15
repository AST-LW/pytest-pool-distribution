from pool import Pooling


def test_one():
    data = Pooling.get_pool_data("user")

    assert data["name"] == "Jack"


def test_two():
    data = Pooling.get_pool_data("user")

    assert data["name"] == "Jack"
