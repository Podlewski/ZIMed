import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
from scipy.stats import shapiro, stats

from argument_parser import ArgumentParser

sns.set_theme()
args = ArgumentParser().get_arguments()

vaccines_years = {'Hepatitis_A': 1995,
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
    plot.savefig(f'imgs/{disease_ns}/states/{disease_ns}_rate_in_{state_ns}.png', dpi=args.dpi)
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
    plot.savefig(f'imgs/{disease_ns}/states/{disease_ns}_sqrt_rate_in_{state_ns}.png', dpi=args.dpi)
    plt.close('all')

rate_max = 0
sqrt_rate_max = 0

for decade in args.decades:
    deacde_df = df[(df['year'] >= decade) & (df['year'] < decade + 10)]
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
    deacde_df = df[(df['year'] >= decade) & (df['year'] < decade + 10)]
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
    fig.set_size_inches(6, 13)
    plt.title(f'{disease} rate in {decade}s per 100 000 people', fontsize=16)
    plt.tight_layout()
    if (args.show_plot):
        plt.show()
    fig.savefig(f'imgs/{disease_ns}/{disease_ns}_rate_in_{decade}.png', dpi=args.dpi)
    plt.cla()

    plot = sns.barplot(x=deacde_df['sqrt_rate'], y=deacde_df.index)
    plt.xlim(0, sqrt_rate_max)
    if decade < 1960:
        plt.gca().get_yticklabels()[1].set_color("red")
        plt.gca().get_yticklabels()[11].set_color("red")
        plt.figtext(0.01, 0.01, "*red states were not states at that time",
                    ha="left", fontsize=12, color='red')
    plot.set(xlabel='square rate')
    plt.text(-3.2, -1, f'{disease} square rate {decade}s per 100 000 people', fontsize=16)
    if (args.show_plot):
        plt.show()
    fig.savefig(f'imgs/{disease_ns}/{disease_ns}_sqrt_rate_in_{decade}.png', dpi=args.dpi)
    plt.close('all')

vaccine_x = vaccine_year - min(df['year'])
rate_max = max(df['rate'])

plot = sns.boxplot(x=df['year'], y=df['rate'])
plt.axvline(vaccine_x, color='r')
plt.annotate(f'{vaccine_year} - {disease} vaccine\nintroduction',
             xy=(vaccine_x, rate_max * 3 / 4),
             xytext=(vaccine_x + 8, rate_max * 3 / 4 + rate_max / 10),
             arrowprops=dict(facecolor='black', shrink=0.05, headwidth=10, width=3))
fig = plot.get_figure()
fig.set_size_inches(12, 6)
plt.title(f'Distribution of {disease} rates', fontsize=16)
plt.xticks(rotation=75, horizontalalignment='right', fontweight='light')
plt.tight_layout()
if (args.show_plot):
    plt.show()
fig.savefig(f'imgs/{disease_ns}/Boxplot_distribution_of_{disease_ns}_rates.png', dpi=args.dpi)
plt.close()

rate_max = max(df['rate'])

plot = sns.relplot(x=df['year'], y=df['rate'], hue=df['state'], kind='line', linewidth=0.75, palette='gist_ncar')
sns.lineplot(x=df['year'], y=df['rate'], color='k', linewidth=2.25)
plt.axvline(vaccine_year, color='r')
plt.annotate(f'{vaccine_year} - {disease} vaccine\nintroduction',
             xy=(vaccine_year, rate_max * 3 / 4),
             xytext=(vaccine_year + 8, rate_max * 3 / 4 + rate_max / 10),
             arrowprops=dict(facecolor='black', shrink=0.05, headwidth=10, width=3))
plot.fig.set_size_inches(12, 9)
plt.title(f'Rates per year for each state ({disease})', fontsize=16)
plot._legend.remove()
plt.legend(bbox_to_anchor=(0.005, -0.1), loc='upper left', ncol=6, prop={'size': 9.85})
plt.tight_layout()
if (args.show_plot):
    plt.show()
plt.savefig(f'imgs/{disease_ns}/Lineplot_distribution_of_{disease_ns}_rates.png', dpi=args.dpi)
plt.cla()

df['sqrt_rate'] = df['rate'].apply(lambda x: np.sqrt(x))
new_df = df.groupby('year', as_index=False)['sqrt_rate'].mean()
before_df = new_df[new_df['year'] < vaccine_year]

stat, p = shapiro(before_df['sqrt_rate'])
print('stat={:.5f}, p={:.5f}'.format(stat, p))
alpha = 0.05
if p > alpha:
    print('Normal distribution (failed to reject H0)')
else:
    print('Not normal distribution (rejected H0)')

after_df = new_df[new_df['year'] > (vaccine_year + 6)]

stat, p = shapiro(after_df['sqrt_rate'])
print('stat={:.5f}, p={:.5f}'.format(stat, p))
if p > alpha:
    print('Normal distribution (failed to reject H0)')
else:
    print('Not normal distribution (rejected H0)')

stat, p = stats.ttest_ind(before_df['sqrt_rate'], after_df['sqrt_rate'], equal_var=False)
print('stat={:.5f}, p={}'.format(stat, p))
if p > alpha:
    print('Equal means (failed to reject H0)')
else:
    print('Unequal means (rejected H0)')

print('Mean before vaccine: {:.3f}'.format(before_df['sqrt_rate'].mean()))
print('Mean after vaccine: {:.3f}'.format(after_df['sqrt_rate'].mean()))
