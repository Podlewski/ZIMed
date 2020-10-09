import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sns.set_theme()
df = pd.read_csv('us_contagious_diseases.csv', header=0, index_col=0)

# 1
df.drop(df[(df['state'] == 'Alaska') |
           (df['state'] == 'Hawaii') |
           (df['disease'] != 'Measles') |
           (df['population'] <= 100000)].index, inplace=True)

# 2
californiaDF = df.drop(df[df['state'] != 'California'].index)

plot = sns.relplot(data=californiaDF, kind='line', marker='o', x='year', y='count')
plt.axvline(1963, color='r')

plt.annotate('1963 - measles vaccine\nintroduction', xy=(1963, 60000), xytext=(1963 + 8, 70000),
             arrowprops=dict(facecolor='black', shrink=0.05, headwidth=10, width=3))
plot.fig.set_size_inches(10, 6)
plot.set_xlabels('year')
plot.set_ylabels('measles disease rate')
plt.title('Measles disease rate per year for California', fontsize=16)
plt.show()
plot.savefig('imgs/measles_disease_rate_in_California.png')

# 3
df = pd.read_csv('us_contagious_diseases.csv', header=0, index_col=0)
df = df[df['disease'] == 'Measles']

hist_1950 = df[df['year'] == 1950]
hist_1950 = hist_1950[['state', 'count']].groupby('state').sum()
hist_1950['count square transform'] = np.sqrt(hist_1950['count'])

hist_1960 = df[df['year'] == 1960]
hist_1960 = hist_1960[['state', 'count']].groupby('state').sum()
hist_1960['count square transform'] = np.sqrt(hist_1960['count'])

hist_1970 = df[df['year'] == 1970]
hist_1970 = hist_1970[['state', 'count']].groupby('state').sum()
hist_1970['count square transform'] = np.sqrt(hist_1970['count'])

# plot 1950
plot_histogram_1950 = sns.barplot(x=hist_1950['count'], y=hist_1950.index)
plt.xlim(0, 50000)
plt.tight_layout()
plt.gca().get_yticklabels()[1].set_color("red")
plt.gca().get_yticklabels()[11].set_color("red")
plt.figtext(0.05, 0.01, "* red states did not exist at that time", ha="left", fontsize=12, color='red')
fig = plot_histogram_1950.get_figure()
fig.set_size_inches(6, 12)
plt.title('Measles disease rate in 1950', fontsize=16)
fig.savefig("imgs/measles_disease_rate_in_1950.png")
plt.show()

# plot 1960
plot_histogram_1960 = sns.barplot(x=hist_1960['count'], y=hist_1960.index)
plt.xlim(0, 50000)
plt.tight_layout()
fig = plot_histogram_1960.get_figure()
fig.set_size_inches(6, 12)
plt.title('Measles disease rate in 1960', fontsize=16)
fig.savefig("imgs/measles_disease_rate_in_1960.png")
plt.show()

# plot 1970
plot_histogram_1970 = sns.barplot(x=hist_1970['count'], y=hist_1970.index)
plt.xlim(0, 50000)
plt.tight_layout()
fig = plot_histogram_1970.get_figure()
fig.set_size_inches(6, 12)
plt.title('Measles disease rate in 1970', fontsize=16)
fig.savefig("imgs/measles_disease_rate_in_1970.png")
plt.show()

# plot 1950 square root transformation
plot_histogram_1950 = sns.barplot(x=hist_1950['count square transform'], y=hist_1950.index)
plt.xlim(0, 250)
plt.tight_layout()
plt.gca().get_yticklabels()[1].set_color("red")
plt.gca().get_yticklabels()[11].set_color("red")
plt.figtext(0.01, 0.01, "* red states did not exist at that time", ha="left", fontsize=12, color='red')
fig = plot_histogram_1950.get_figure()
fig.set_size_inches(6, 12)
plot.set_xlabels('count')
plt.title('Measles disease rate in 1950', fontsize=16)
fig.savefig("imgs/measles_disease_rate_in_1950_sqrt_transform.png")
plt.show()

# plot 1960 square root transformation
plot_histogram_1960 = sns.barplot(x=hist_1960['count square transform'], y=hist_1960.index)
plt.xlim(0, 250)
plt.tight_layout()
fig = plot_histogram_1960.get_figure()
fig.set_size_inches(6, 12)
plot.set_xlabels('count')
plt.title('Measles disease rate in 1960', fontsize=16)
fig.savefig("imgs/measles_disease_rate_in_1960_sqrt_transform.png")
plt.show()

# plot 1970 square root transformation
plot_histogram_1970 = sns.barplot(x=hist_1970['count square transform'], y=hist_1970.index)
plt.xlim(0, 250)
plt.tight_layout()
fig = plot_histogram_1970.get_figure()
fig.set_size_inches(6, 12)
plot.set_xlabels('count')
plt.title('Measles disease rate in 1970', fontsize=16)
fig.savefig("imgs/measles_disease_rate_in_1970_sqrt_transform.png")
plt.show()

