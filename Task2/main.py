import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from timeit import default_timer as timer

from argument_parser import ArgumentParser


# CONSTANTS 
MIN_DBIRWT = 2700 
MAX_FEATURES = 20

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

def plot_linear_reggresion(X, Y, x, show_plot):
    model = LinearRegression().fit(X, Y)
    y_line = model.coef_[0] * x + model.intercept_
    plot(X, Y, x, y_line, 'Linear', show_plot)


def plot_logistic_reggresion(X, Y, x, show_plot):
    model = LogisticRegression(solver='liblinear', random_state=0).fit(X, Y)
    y_line = []
    a_v = model.coef_[0][0]
    b_v = model.intercept_[0]
    for i in x:
        y = ((1 / (1 + math.exp(- (i * a_v)))) + b_v)
        y_line.append(y)
    plot(X, Y, x, y_line, 'Logic', show_plot)


def plot(X, Y, x, y_line, name, show_plot):
    plt.scatter(X, Y, color='black', s=0.5)
    plt.plot(x, y_line, color='blue', linewidth=1.5)
    plt.title(f'{name} regression')
    plt.tight_layout()
    plt.savefig(name, dpi=300)
    if show_plot is True:
        plt.show()
    plt.close()
    
### PART 2.3
def factorize_data (data):
    data = data.apply(lambda x: pd.factorize(x)[0])
    return data

def drop_cols(data, cols):
    for col in cols:
        data = data.drop(col,1)
    return data
    
def Forest_Classifier(X, Y):
    model = RandomForestClassifier()
    model.fit(X, Y)
    return model

def plot_feat_importances(model, col_names, name, show_plot):
    feat_importances = pd.Series(model.feature_importances_, index=col_names)
    feat_importances.nlargest(MAX_FEATURES).plot(kind='barh')
    plt.title('feature importances')
    plt.tight_layout()
    plt.savefig(name, dpi=300)    
    if show_plot is True:
        plt.show()
    plt.close()


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
        print(f'FIRST PART:  {first_part - start:4.2f} s\n')

    X = singletons['dbirwt'].values.reshape(-1, 1)
    x = np.linspace(X.min(), X.max(), 100)
    Y = singletons['tobacco']
    
    plot_linear_reggresion(X, Y, x, args.plot)
    plot_logistic_reggresion(X, Y, x, args.plot)

    second_part = timer()
    if args.time is True:
        print(f'SECOND PART: {second_part - first_part:4.2f} s\n')
    
    ### 3
    # drop unnecessery columns
    unnecessery_cols = ['infant_id', 'term', 'mort', 'dbirwt' ]
    disease_cols = ['anemia', 'cardiac', 'lung', 'diabetes', 'herpes', 'hydra',
        'hemo', 'chyper', 'eclamp', 'incervix', 'renal', 'uterine', 'othermr']  
    
    X = factorize_data(singletons)
    X = drop_cols(X, unnecessery_cols)

    corr = X.corr().stack()
    corr = corr[corr.index.get_level_values(0) != corr.index.get_level_values(1)]
    corr = corr.sort_values(ascending = False)
    corr = corr[corr.index.get_level_values(0) == 'lbw']
    print('Correlations:')
    print(f'{corr}\n')

    X = X.drop('lbw', 1)

    # Label
    Y = singletons['lbw'] 
    
    # Case1 : Only disease columns
    X1 = X[disease_cols]
    columns_names = X1.columns
    plot_feat_importances(Forest_Classifier(X1, Y), columns_names,
                          'disease_forest', args.plot)
    
    # Case2 : Non-disease columns
    X2 = drop_cols(X, disease_cols)
    columns_names = X2.columns
    plot_feat_importances(Forest_Classifier(X2, Y), columns_names,
                          'non-diesease_forest', args.plot)
    
    # Case3 : All factors/columns, expect unnecessery columns
    columns_names = X.columns
    plot_feat_importances(Forest_Classifier(X, Y), columns_names,
                          'all-forest', args.plot)

    third_part = timer()
    if args.time is True:
        print(f'THIRD PART:  {third_part - second_part:4.2f} s\n')


if __name__ == "__main__":
    args = ArgumentParser().get_arguments()
    sns.set_theme()
    main(args)
