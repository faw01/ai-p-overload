# %%
# import
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import IsolationForest

# %%
# load the data
df = pd.read_csv('datasets/data.csv')

# EXPLORATION

# %%
# first few rows
df.head()

# %%
# last few rows
df.tail()

# %%
# shape
df.shape

# %%
# columns list
df.columns

# %%
# basic info
df.info()

# %%
# count non-null entries in each column
df.count()

# %%
# display summary statistics for numerical columns
df.describe()

# WRANGLING

# %% 
# remove redundant columns (cardio related / all NaN)
df = df.drop(['Distance', 'Seconds', 'Notes', 'Workout Notes', 'RPE'], axis=1)

# %% 
# format is day-month-year hours-minutes
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y %H:%M').dt.date

# %%
# only get date component
df['Date'] = pd.to_datetime(df['Date'])

# %%
# function to convert duration into hh-mm-ss
def convert_duration(duration):
    return np.nan if pd.isnull(duration) else pd.to_timedelta(duration)

# %%
# apply the function to the duration column
df['Duration'] = df['Duration'].apply(convert_duration)

# IMPUTATION
# %%
# identify missing values
df.isnull().sum()

# %%
# identify duration = 0 
df[df['Duration'] == '0 days 00:00:00']

# %%
# fill in the difference for joe
pass

# %%
# print missing values
df[df.isnull().any(axis=1)]

# DUPLICATION

# %%
# identify duplicate entries
duplicate_entries = df.duplicated()

# %%
# remove duplicates
df = df[~duplicate_entries]

# OUTLIER DETECTION

# %% 
# identify outliers in the dataset using isolation forest
iso = IsolationForest(contamination=0.1)
yhat = iso.fit_predict(df[['Set Order', 'Weight', 'Reps', 'Volume']])

# select all rows that are not outliers
mask = yhat != -1
df = df[mask]

# %%
# display summary statistics for numerical columns
df.describe()

# FEATURE ENGINEERING

# %% 
# sort the dataframe by participant and date
df = df.sort_values(['Participant', 'Date'])

# %% 
# group the data by participant and workout name
grouped = df.groupby(['Participant', 'Workout Name'])

# %% 
# calculate workout_volume_change, average_weight, change_in_rep_count, and change_in_set_count
df['Workout_Volume_Change'] = grouped['Volume'].diff()
df['Average_Weight'] = grouped['Weight'].transform('mean')
df['Change_in_Rep_Count'] = grouped['Reps'].diff()
df['Change_in_Set_Count'] = grouped['Set Order'].diff()

# %% 
# calculate workout_intensity
df['Workout_Intensity'] = df['Weight'] / df['Reps']

# %% 
# calculate workout_frequency and exercise_frequency
df['Week'] = df['Date'].dt.week
workout_frequency = df.groupby(['Participant', 'Week'])['Workout Name'].nunique()
exercise_frequency = df.groupby(['Participant', 'Week', 'Exercise Name']).size()

# %% 
# merge workout_frequency and exercise_frequency back into the main dataframe
df = df.merge(workout_frequency, how='left', on=['Participant', 'Week'])
df = df.merge(exercise_frequency, how='left', on=['Participant', 'Week', 'Exercise Name'])

# %% 
# rename the new columns
df.rename(columns={'Workout Name_x': 'Workout Name', 'Workout Name_y': 'Workout_Frequency', 0: 'Exercise_Frequency'}, inplace=True)

