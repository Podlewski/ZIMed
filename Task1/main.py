import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
from argument_parser import ArgumentParser


sns.set_theme()
args = ArgumentParser().get_arguments()

vaccines_years = {'Hepatitis A': 1950,
                   'Measles': 1963,
                   'Mumps': 1950,
                   'Pertussis': 1950,
                   'Polio': 1950,
                   'Rubella': 1950,
                   'Smallpox': 1950}

disease = args.disease
disease_ns = disease.replace(' ', '-')
vaccine_year = vaccines_years[disease]

if not os.path.exists(f'imgs/{disease_ns}'):
    os.makedirs(f'imgs/{disease_ns}')

### 1
df = pd.read_csv('us_contagious_diseases.csv', header=0, index_col=0)
# df.drop(df[(df['state'] == 'Alaska') |
#            (df['state'] == 'Hawaii') |
#            (df['disease'] != 'Measles') |
#            (df['population'] <= 100000)].index, inplace=True)
df = df[df['disease'] == disease]

for state in args.states:
    state_ns = state.replace(' ', '_')
    if not os.path.exists(f'imgs/{disease_ns}/{state_ns}'):
        os.makedirs(f'imgs/{disease_ns}/{state_ns}')

    state_df = df.drop(df[df['state'] != state].index)
    state_df['count square transform'] = np.sqrt(state_df['count'])

    plot = sns.relplot(x=state_df['year'], y=state_df['count'], kind='line', marker='o')
    plt.axvline(vaccine_year, color='r')
    plt.annotate(f'{vaccine_year} - {disease} vaccine\nintroduction',
                xy=(vaccine_year, 60000), xytext=(vaccine_year + 8, 70000),
                arrowprops=dict(facecolor='black', shrink=0.05, headwidth=10, width=3))
    plot.fig.set_size_inches(10, 6)
    plot.set_ylabels(f'{disease} disease rate')
    plt.title(f'{disease} disease rate per year for {state}', fontsize=16)
    plt.tight_layout()
    if (args.show_plot):
        plt.show()
    plot.savefig(f'imgs/{disease_ns}/{state_ns}/{disease_ns}_disease_rate_in_{state_ns}.png')
    plt.cla()

    plot = sns.relplot(x=state_df['year'], y=state_df['count square transform'],
                       kind='line', marker='o')
    plt.axvline(vaccine_year, color='r')
    plt.annotate(f'{vaccine_year} - {disease} vaccine\nintroduction',
                xy=(vaccine_year, 200), xytext=(vaccine_year + 8, 250),
                arrowprops=dict(facecolor='black', shrink=0.05, headwidth=10, width=3))
    plot.fig.set_size_inches(10, 6)
    plot.set_ylabels(f'{disease} disease square rate')
    plt.title(f'{disease} disease square rate per year for {state}', fontsize=16)
    plt.tight_layout()
    if (args.show_plot):
        plt.show()
    plot.savefig(f'imgs/{disease_ns}/{state_ns}/{disease_ns}_disease_rate_in_{state_ns}_sqrt_transform.png')
    plt.cla()

plt.close()

for decade in args.decades:
    deacde_df = df[df['year'] == decade]
    deacde_df = deacde_df[['state', 'count']].groupby('state').sum()
    deacde_df['count square transform'] = np.sqrt(deacde_df['count'])

    plot = sns.barplot(x=deacde_df['count'], y=deacde_df.index)
    plt.xlim(0, 50000)
    if decade < 1960:
        plt.gca().get_yticklabels()[1].set_color("red")
        #plt.gca().get_yticklabels()[11].set_color("red")
        plt.figtext(0.01, 0.01, "*red states did not exist at that time",
                    ha="left", fontsize=12, color='red')
    fig = plot.get_figure()
    fig.set_size_inches(6, 12)
    plt.title(f'{disease} disease rate in {decade}', fontsize=16)
    plt.tight_layout()
    if (args.show_plot):
        plt.show()
    fig.savefig(f'imgs/{disease_ns}/{disease_ns}_disease_rate_in_{decade}.png')
    plt.cla()

    plot = sns.barplot(x=deacde_df['count square transform'], y=deacde_df.index)
    plt.xlim(0, 250)
    if decade < 1960:
        plt.gca().get_yticklabels()[1].set_color("red")
        #plt.gca().get_yticklabels()[11].set_color("red")
        plt.figtext(0.01, 0.01, "*red states did not exist at that time",
                    ha="left", fontsize=12, color='red')
    plot.set(xlabel='square count')
    plt.title(f'{disease} disease rate in {decade}', fontsize=16)
    if (args.show_plot):
        plt.show()
    fig.savefig(f'imgs/{disease_ns}/{disease_ns}_disease_rate_in_{decade}_sqrt_transform.png')
    plt.cla()

plt.close()


# box 
plot = sns.boxplot(x=df['year'], y=df['state'], data=df['count'])
fig = plot.get_figure()
fig.set_size_inches(6, 12)
plt.title(f'Distribution of {disease} rates', fontsize=16)
plt.tight_layout()
if (args.show_plot):
    plt.show()
fig.savefig(f'imgs/{disease_ns}/Distribution_of_{disease_ns}_rates.png')
plt.close()