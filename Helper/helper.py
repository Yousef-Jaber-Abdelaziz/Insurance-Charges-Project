import pandas as pd


# ----------------------------------------------------------------------------
# Data functions
# ----------------------------------------------------------------------------
def load_data(path):
    """Read a csv file into a DataFrame."""
    return pd.read_csv(path)
