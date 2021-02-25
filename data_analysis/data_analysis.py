import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from pathlib import Path
from scipy import stats
import seaborn as sns

sns.set_theme(style="whitegrid")

BASE_DIR = Path(__file__).resolve().parent

df = pd.read_csv(os.path.join('data_analysis', 'questionnaires.csv'))

# %% groups

df1 = df[df['What group were you in?'] == 'Group number 1']
df2 = df[df['What group were you in?'] == 'Group number 2']
df3 = df[df['What group were you in?'] == 'Group number 3']

# %% hypotheses 1
question1 = 'How much did you enjoy the experiment?'
question2 = 'How much did you enjoy the interaction with the robot?'
enj1 = df1.loc[:, question1].tolist()
enj2 = df2.loc[:, question1].tolist()

enj12 = df1.loc[:, question2].tolist()
enj22 = df2.loc[:, question2].tolist()

t1, p1 = stats.ttest_ind(enj1, enj2, alternative='greater')
t2, p2 = stats.ttest_ind(enj12, enj22, alternative='greater')

# print(f"t value: {t:.3f}; p value: {p:.3f}")
res = pd.DataFrame([[t1,p1], [t2,p2]],columns=['t value', 'p value'], index=[question1, question2])
res.to_csv('p_values.csv')
# %%


# %% anova

# enj1 = df1.loc[:, 'How much did you enjoy the experiment?'].tolist()
# enj2 = df2.loc[:, 'How much did you enjoy the experiment?'].tolist()
# enj3 = df3.loc[:, 'How much did you enjoy the experiment?'].tolist()

enj1 = df1.loc[:, 'How much did you enjoy the interaction with the robot?'].tolist()
enj2 = df2.loc[:, 'How much did you enjoy the interaction with the robot?'].tolist()
enj3 = df3.loc[:, 'How much did you enjoy the interaction with the robot?'].tolist()

statistics, p = stats.f_oneway(enj1, enj2, enj3)

print(f"statistics value: {statistics:.3f}; p value: {p:.3f}")

# %% anova for age groups
question = 'How much did you enjoy the experiment?'
# question = 'How much did you enjoy the interaction with the robot?'
age_groups = []

for age_group in ['15 - 24 years old', '35 - 44 years old', '25 - 34 years old', '45 - 54 years old',
                  '55 - 64 years old', '65+ years old']:
    age_groups.append(df[df['How old are you ?'] == age_group].loc[:, question].tolist())

statistics, p = stats.f_oneway(*age_groups)

print(f"statistics value: {statistics:.3f}; p value: {p:.3f}")

# %% anova
question = 'Would you suggest using this kind of language learning app to people over 60?'
enj1 = df1.loc[:, question].tolist()
enj2 = df2.loc[:, question].tolist()
enj3 = df3.loc[:, question].tolist()

statistics, p = stats.f_oneway(enj1, enj2, enj3)

print(f"statistics value: {statistics:.3f}; p value: {p:.3f}")

# %%
question = 'How much did you enjoy the experiment?'
# question = 'How much did you enjoy the interaction with the robot?'
print("All", np.mean(df.loc[:, question].tolist()))
print("Group1", np.mean(df1.loc[:, question].tolist()))
print("Group2", np.mean(df2.loc[:, question].tolist()))
print("Group3", np.mean(df3.loc[:, question].tolist()))
ax = sns.boxplot(x='What group were you in?', y=question, order=['Group number 1', 'Group number 2', 'Group number 3'],
                 data=df)

plt.savefig(os.path.join(BASE_DIR, 'figures', question + '.png'), transparent=True)
plt.show()

# %%
plt.figure(figsize=(16, 12))
question = 'If you were in group 3, what was your preferred input method?'
ax = sns.catplot(x=question, kind="count", data=df3)
plt.savefig(os.path.join(BASE_DIR, 'figures', question + '.png'), transparent=True)
plt.show()

# %%
plt.figure(figsize=(8, 6))
question = 'Hearing the robot speak to me and ask me questions was more interesting than if I would have just read the questions.'
sns.histplot(x=question, data=df, binrange=(1, 7))
plt.xlabel(
    'Hearing the robot speak to me and ask me questions was more\n interesting than if I would have just read the questions.')
plt.savefig(os.path.join(BASE_DIR, 'figures', question + '.png'), transparent=True)
plt.show()

# %%
plt.figure(figsize=(16, 12))
question = 'If you were in group 3, what was your preferred input method?'
