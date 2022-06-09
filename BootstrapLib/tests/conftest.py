import pytest

from PriceSim.RandomWalk import RandomWalk


@pytest.fixture(scope="session")
def prepare_context():

    _rw = RandomWalk()
    _df = _rw.gen_random_walk(1000, 0.0001,last_date="2022-06-09 00:00", value_0=1.1300, freq="H", output_col_name="Close")
    _context = {"data": _df}

    return _context



