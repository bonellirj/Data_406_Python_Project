# %%
import sys
import os
import pandas as pd 

# sys.path.append( os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from db.engine_factory import getConnection as engine_factory


# %%
df = pd.read_sql("SELECT * FROM dw.Dim_City", engine_factory)
print( df.head() )


print('PATH:', os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


# %%
