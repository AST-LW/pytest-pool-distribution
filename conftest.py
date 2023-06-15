import pytest

from pool import Pooling


@pytest.fixture(scope="session", autouse=True)
def session_fixture(request):
    Pooling.create_pool_template(request)


@pytest.fixture(scope="function", autouse=True)
def function_fixture(request):
    return Pooling.create_instance_reference(request)
