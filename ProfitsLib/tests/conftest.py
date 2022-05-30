import pandas as pd
import pytest 

@pytest.fixture(scope="session")
def prepare_context():
    _df = pd.read_csv("./data/trades_reduced.csv")
    _cost = 0.5
    return {"data_set": _df, "cost": _cost}

