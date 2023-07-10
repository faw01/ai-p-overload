#%%
import pandas as pd

#%%
df = pd.read_csv('datasets/data.csv')

#%%
df.head()

# %% 
# remove redundant columns
df = df.drop(['Distance', 'Seconds', 'Notes', 'Workout Notes', 'RPE'], axis=1)


# %%
df.shape

# %%
df.index

# %%
df.columns

# %%
df.info()

# %%
df.count()

# %%
df.head()

# %%
df.tail()

# %% 
# cleaning (formatting, reduction)

# %%
# imputation



