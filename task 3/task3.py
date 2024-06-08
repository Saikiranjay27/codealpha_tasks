# -*- coding: utf-8 -*-
"""task3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zxIAQsO6kZkmSuKm3rBY4qLaBKTgmEIc
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
# %matplotlib inline
#We are setting the seed to assure you get the same answers on quizzes as we set up
random.seed(42)

df_ab = pd.read_csv('ab_data.csv')
df_ab.head(5)

df_ab.shape[0]

len(df_ab.user_id.unique())

converted = df_ab.converted.value_counts()
print(f"Proportion of converted: {converted[1] / (converted[0] + converted[1])}")

first = df_ab.query('group=="treatment" & landing_page!="new_page"')
second = df_ab.query('landing_page=="new_page" & group!="treatment"')
len(first) + len(second)

pd.isna(first).count()

pd.isna(second).count()

import pandas as pd

# Assuming first and second are the two DataFrames you want to concatenate

# Create a copy of the first DataFrame
df2 = first.copy()

# Append the second DataFrame to the first DataFrame
df2 = pd.concat([df2, second], ignore_index=True)

# Display the first 5 rows of the resulting Data
df2.head(5)

len(df2)

df_mess = df2.copy()

df_mess.head(5)

df2 = pd.concat([df_ab, df_mess, df_mess]).drop_duplicates(keep=False)
df2.head(2)

len(df2)

len(df2.user_id.unique())

df2_dup = df2[df2.user_id.duplicated()]
df2_dup

df2[df2.user_id == 773192]

df2.drop(1899, inplace=True)
df2[df2.user_id == 773192]

df2_conv = df2[df2.converted == 1]

all_convert = len(df2_conv)
all_convert

all_peeps = len(df2)
all_peeps

all_convert / all_peeps

df2_all_control = df2[df2.group == 'control']
all_control = len(df2_all_control)
all_control

df2_control_conv = df2_all_control[df2_all_control.converted == 1]
len(df2_control_conv)

df2.query('group == "control"')['converted'].mean()

df2.query('group == "treatment"')['converted'].mean()

len(df2[df2.landing_page == 'new_page']) / all_peeps

# a/b test
p_new = df2.converted.mean()
p_new

p_old = df2.converted.mean()
p_old

p_new - p_old

n_new = len(df2[df2.group == 'treatment'])
n_new

n_old = len(df2[df2.group == 'control'])
n_old

new_page_converted = []
new_page_converted = np.random.choice([0,1],n_new,[1-p_new,p_new])

old_page_converted = []
old_page_converted = np.random.choice([0,1],n_old,[1-p_old,p_old])

obs_diff = np.mean(new_page_converted) - np.mean(old_page_converted)
obs_diff

# Commented out IPython magic to ensure Python compatibility.
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

#mpl.style.use('ggplot')
# %matplotlib inline

plt.figure(figsize=(10,10))
sns.distplot(p_diffs, bins=10, kde=False, rug=True);

plt.xlabel('Mean Distribution', fontsize=20)
plt.title('Distributions of 10,000 samples at size of 145,300', fontsize=24)
plt.ylabel('Number of Samples', fontsize=20)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12);

p_diffs = np.array(p_diffs)
null_vals = np.random.normal(0, p_diffs.std(), p_diffs.size)

(null_vals > obs_diff).mean()

actual_new_conv = df2[df2.landing_page == 'new_page']['converted'].mean()
actual_old_conv = df2[df2.landing_page == 'old_page']['converted'].mean()

actual_diff = actual_new_conv - actual_old_conv

print(f"Actual difference in new & old conversion means: {actual_diff}")

diff_prop = np.greater(p_diffs,actual_diff)

diff_prop.mean()

import statsmodels.api as sm

old_data = df2[df2.landing_page == 'old_page']['converted']
mu_convert_old = df2[df2.landing_page == 'old_page']['converted'].mean()
std_convert_old = df2[df2.landing_page == 'old_page']['converted'].std()

new_data = df2[df2.landing_page == 'new_page']['converted']
mu_convert_new = df2[df2.landing_page == 'new_page']['converted'].mean()
std_convert_new = df2[df2.landing_page == 'new_page']['converted'].std()

n_old = len(df2[df2.group == 'control'])
n_new = len(df2[df2.group == 'treatment'])

print(n_old,mu_convert_old,std_convert_old)
print(n_new,mu_convert_new,std_convert_new)

sm.stats.ztest(old_data,new_data,alternative='two-sided')

mu_convert_old

mu_convert_new

sm.stats.proportions_ztest(mu_convert_new * n_new, n_new, mu_convert_old, alternative='larger')