import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
from argument_parser import ArgumentParser


sns.set_theme()
args = ArgumentParser().get_arguments()

vaccines_years = {'Hepatitis A': 1995,
                   'Measles': 1963,
                   'Mumps': 1948,
                   'Pertussis': 1926,
                   'Polio': 1955,
                   'Rubella': 1969,
                   'Smallpox': 1796}

disease = args.disease
disease_ns = disease.replace(' ', '-')
vaccine_year = vaccines_years[disease]

if not os.path.exists(f'imgs/{disease_ns}/states'):
    os.makedirs(f'imgs/{disease_ns}/states')

### 1
df = pd.read_csv('us_contagious_diseases.csv', header=0, index_col=0)
df = df[df['disease'] == disease]
df['rate'] = (df['count'] / df['weeks_reporting']) * (100000 / df['population'])

for state in args.states:
    state_ns = state.replace(' ', '_')
    state_df = df.drop(df[df['state'] != state].index)
    state_df['sqrt_rate'] = np.sqrt(state_df['rate'])

    rate_max = max(state_df['rate']) 
    sqrt_rate_max = max(state_df['sqrt_rate'])

    plot = sns.relplot(x=state_df['year'], y=state_df['rate'], kind='line', marker='o')
    plt.axvline(vaccine_year, color='r')
    plt.annotate(f'{vaccine_year} - {disease} vaccine\nintroduction',
                xy=(vaccine_year, rate_max * 3 / 4),
                xytext=(vaccine_year + 8, rate_max * 3 / 4 + rate_max / 10),
                arrowprops=dict(facecolor='black', shrink=0.05, headwidth=10, width=3))
    plot.fig.set_size_inches(10, 6)
    plot.set_ylabels(f'Average {disease} rate per week')
    plt.title(f'{disease} rate for {state} per 100 000 people', fontsize=16)
    plt.tight_layout()
    if (args.show_plot):
        plt.show()
    plot.savefig(f'imgs/{disease_ns}/states/{disease_ns}_rate_in_{state_ns}.png')
    plt.cla()

    plot = sns.relplot(x=state_df['year'], y=state_df['sqrt_rate'],
                       kind='line', marker='o')
    plt.axvline(vaccine_year, color='r')
    plt.annotate(f'{vaccine_year} - {disease} vaccine\nintroduction',
                xy=(vaccine_year, sqrt_rate_max * 3 / 4),
                xytext=(vaccine_year + 8, sqrt_rate_max * 3 / 4 + sqrt_rate_max / 10),
                arrowprops=dict(facecolor='black', shrink=0.05, headwidth=10, width=3))
    plot.fig.set_size_inches(10, 6)
    plot.set_ylabels(f'Average {disease} square rate per week')
    plt.title(f'{disease} square rate for {state} per 100 000 people', fontsize=16)
    plt.tight_layout()
    if (args.show_plot):
        plt.show()
    plot.savefig(f'imgs/{disease_ns}/states/{disease_ns}_sqrt_rate_in_{state_ns}.png')
    plt.close('all')

rate_max = 0
sqrt_rate_max = 0

for decade in args.decades:
    deacde_df = df[(df['year'] >= decade) & (df['year'] < decade+10)]
    deacde_df = deacde_df[['state', 'rate']].groupby('state').sum()
    deacde_df['sqrt_rate'] = np.sqrt(deacde_df['rate'])

    decade_max = max(deacde_df['rate'])
    if (decade_max > rate_max):
        rate_max = decade_max

    decade_sqrt_max = max(deacde_df['sqrt_rate'])
    if (decade_sqrt_max > sqrt_rate_max):
        sqrt_rate_max = decade_sqrt_max      

rate_max = (int(rate_max / 25) + 1) * 25 
sqrt_rate_max = (int(sqrt_rate_max / 5) + 1) * 5 

for decade in args.decades:
    deacde_df = df[(df['year'] >= decade) & (df['year'] < decade+10)]
    deacde_df = deacde_df[['state', 'rate']].groupby('state').sum()
    deacde_df['sqrt_rate'] = np.sqrt(deacde_df['rate'])

    plot = sns.barplot(x=deacde_df['rate'], y=deacde_df.index)
    plt.xlim(0, rate_max)
    if decade < 1960:
        plt.gca().get_yticklabels()[1].set_color("red")
        plt.gca().get_yticklabels()[11].set_color("red")
        plt.figtext(0.01, 0.01, "*red states were not states at that time",
                    ha="left", fontsize=12, color='red')
    fig = plot.get_figure()
    fig.set_size_inches(6, 12)
    plt.title(f'{disease} rate in {decade} per 100 000 people', fontsize=16)
    plt.tight_layout()
    if (args.show_plot):
        plt.show()
    fig.savefig(f'imgs/{disease_ns}/{disease_ns}_rate_in_{decade}.png')
    plt.cla()

    plot = sns.barplot(x=deacde_df['sqrt_rate'], y=deacde_df.index)
    plt.xlim(0, sqrt_rate_max)
    if decade < 1960:
        plt.gca().get_yticklabels()[1].set_color("red")
        plt.gca().get_yticklabels()[11].set_color("red")
        plt.figtext(0.01, 0.01, "*red states were not states at that time",
                    ha="left", fontsize=12, color='red')
    plot.set(xlabel='square rate')
    plt.title(f'{disease} square rate in {decade} per 100 000 people', fontsize=16)
    if (args.show_plot):
        plt.show()
    fig.savefig(f'imgs/{disease_ns}/{disease_ns}_sqrt_rate_in_{decade}.png')
    plt.close('all')

# box 
plot = sns.boxplot(x=df['year'], y=df['state'], data=df['rate'])
fig = plot.get_figure()
fig.set_size_inches(6, 12)
plt.title(f'Distribution of {disease} rates', fontsize=16)
plt.tight_layout()
if (args.show_plot):
    plt.show()
fig.savefig(f'imgs/{disease_ns}/Distribution_of_{disease_ns}_rates.png')
plt.close()