import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt


sns.set_theme()

df = pd.read_csv('us_contagious_diseases.csv', header=0, index_col=0)

df.drop(df[(df['state'] == 'Alaska') |
           (df['state'] == 'Hawaii') |
           (df['disease'] != 'Measles') |
           (df['population'] <= 100000)].index , inplace=True)

californiaDF = df.drop(df[df['state'] != 'California'].index)

plot = sns.relplot(data=californiaDF, kind='line', x='year', y='count')
plt.axvline(1963, color='r')
plot.savefig('output.png')
