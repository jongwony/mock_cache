import os
import pickle
from contextlib import contextmanager
from tempfile import gettempdir
from unittest.mock import patch

import pandas as pd


@contextmanager
def sql_cache(force_update: bool = False):
    """
    monkeypatch and save or mock load

    Note
    ----
    Only one `read_sql` should be written in one with statement.
    """

    def save(target, df):
        with open(target, 'wb') as wf:
            pickle.dump(df, wf)

    def load(target):
        with open(target, 'rb') as rf:
            data = pickle.load(rf)
        return data

    def read_sql_hooks():
        def wrapper(*args, **kwargs):
            cache_name = kwargs.pop('cache_name')
            target = os.path.join(gettempdir(), f'{cache_name}.pickle')
            if not os.path.exists(target) or force_update:
                df = monkeypatch(*args, **kwargs)
                df.cache_name = cache_name
                save(target, df)
            else:
                df = load(target)

            return df

        return wrapper

    monkeypatch = pd.read_sql
    pd.read_sql = read_sql_hooks()

    with patch.object(pd, 'read_sql', new=read_sql_hooks()):
        yield

    pd.read_sql = monkeypatch
