from sklearn.linear_model import LinearRegression, LogisticRegression
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from timeit import default_timer as timer
import seaborn as sns

from argument_parser import ArgumentParser


# CONSTANTS 
MIN_DBIRWT = 2700 


### PART 2.1

def add_lbw_column(df):
    df['lbw'] = df['dbirwt'].map(lambda x: x < MIN_DBIRWT)
    return df


def reduce_twins_df(df):
    groups = df.groupby('pair_id')
    only_one_twin_lbw = {}
    for id, group in groups:
        lbw = group['lbw'].values
        only_one_twin_lbw[id] = lbw[0] ^ lbw[1]
    df['one_lbw'] = df['pair_id'].map(only_one_twin_lbw)
    return df[df['one_lbw']]


def morality_rate(df):
    return df['mort'].value_counts(normalize=True)[1] * 100


def print_morality(df, type):
    print(f'{type} morality rate')
    print(f'Comprehensive:      {morality_rate(df):4.2f} %')
    print(f'Low body weight:    {morality_rate(df[df.lbw == True]):4.2f} %')
    print(f'Higher body weight: {morality_rate(df[df.lbw == False]):4.2f} %\n')


### PART 2.2

def plot_linear_reggresion(X, Y, x):
    model = LinearRegression().fit(X, Y)
    y_line = model.coef_[0] * x + model.intercept_
    plot(X, Y, x, y_line, 'Linear')


def plot_logistic_reggresion(X, Y, x):
    model = LogisticRegression(solver='liblinear', random_state=0).fit(X, Y)
    y_line = []
    a_v = model.coef_[0][0]
    b_v = model.intercept_[0]
    for i in x:
        y = ((1 / (1 + math.exp(- (i * a_v)))) + b_v)
        y_line.append(y)
    plot(X, Y, x, y_line, 'Logic')


def plot(X, Y, x, y_line, name):
    plt.scatter(X, Y, color='black', s=0.5)
    plt.plot(x, y_line, color='blue', linewidth=1.5)
    plt.title(f'{name} regression')
    plt.savefig(name, dpi=300)
    plt.clf()
    

def main(args):    
    start = timer()  

    twins = pd.read_csv('twins.txt')
    twins = add_lbw_column(twins)
    twins = reduce_twins_df(twins)
    print_morality(twins, 'Twins')

    singletons = pd.read_csv('singletons.txt')
    singletons = add_lbw_column(singletons)
    print_morality(singletons, 'Singletons')

    first_part = timer()
    if args.time is True:
        print(f'First part:  {first_part - start:4.2f} s')

    X = singletons['dbirwt'].values.reshape(-1, 1)
    x = np.linspace(X.min(), X.max(), 100)
    Y = singletons['tobacco']
    plot_linear_reggresion(X, Y, x)
    plot_logistic_reggresion(X, Y, x)

    second_part = timer()
    if args.time is True:
        print(f'Second part: {second_part - first_part:4.2f} s')


if __name__ == "__main__":
    args = ArgumentParser().get_arguments()
    sns.set_theme()
    main(args)
