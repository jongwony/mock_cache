# mock_cache
Mock objects not only for testing but caching that save your time!

## Usage

- pandas `read_sql` monkeypatch

```python
import sqlite3
import pandas as pd
from common.io import sql_cache

engine = sqlite3.connect(':memory:')
with sql_cache(force_update=False):
    data = pd.read_sql('select * from user limit 1', engine, cache_name='test')
    data2 = pd.read_sql('select * from user limit 2', engine, cache_name='test2')
    ...
```
