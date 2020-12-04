import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression, LogisticRegression
from datetime import datetime
import math

# założenie z zadania
MinDbirwt = 2700

# Punkt 2.1


# Przygotowanie pliku zawierającego dzieci, gdzie jeden z bliźniaków ma wagę poniżej <MinDbirwt> a drugi powyżej <MinDbirwt> (Warunki zadania)
# Można pominąć ten krok i wczytać przygotowany już plik o nazwie: out2.csv, ktory spełnia powyższe warunki
choice = int(input("1\t->\tpomijam tworznie pliku\n2\t->\ttworze plik\nWybor: "))

if choice == 2:
    df = pd.read_csv('twins.txt', header=0)
    #print(df)
    df['mrace'] = df['mrace'].factorize()[0]
    df['dmeduc'] = df['dmeduc'].factorize()[0]
    df['frace'] = df['frace'].factorize()[0]
    df['dfeduc'] = df['dfeduc'].factorize()[0]
    #print(df)
    df2 = df[['mort', 'dbirwt', 'infant_id', 'pair_id']]
    #print(df2)

    print("Ilosc przed: ", len(df))

    df22 = df2.groupby('pair_id')#.apply(lambda g: g[g['dbirwt'] < 2700])
    print(df22)
    print("-------------")
    i = 0

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    for pair_id, group in df22:
        if group['dbirwt'][i] < MinDbirwt and  group['dbirwt'][i+1] < MinDbirwt:
            #print("Wykrylem mniejsze")
            df = df[df['pair_id'] != pair_id]
            #print("Usuwam pair_id=",pair_id)
        elif group['dbirwt'][i] > MinDbirwt and  group['dbirwt'][i+1] > MinDbirwt:
            #print("Wykrylem wieksze")
            df = df[df['pair_id'] != pair_id]
            #print("Usuwam pair_id=",pair_id)
        i += 2

    print("Ilosc ppo: ",len(df))

    df.to_csv('./out2.csv', index_label=False, index=False)
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    print("Finish")

# PART2

df = pd.read_csv('twins.txt', header=0)
print("Ogólna śmiertelność dzieci wsrod bliznikow [%] :", df['mort'].value_counts(normalize=True)[1]*100)

df = pd.read_csv('out2.csv', header=0)
print("Śmiertelność dzieci IBV wsród blizników [%] :", df['mort'].value_counts(normalize=True)[1]*100)


df = pd.read_csv('singletons.txt', header=0)
print("Ogólna śmiertelność dzieci wsrod jedynakow [%] :",df['mort'].value_counts(normalize=True)[1]*100)

df_MinDbirwt = df[df['dbirwt'] < MinDbirwt]
print("IBW: ", len(df_MinDbirwt))
print("Śmiertelność dzieci IBV wsrod jedynakow [%] :", df_MinDbirwt['mort'].value_counts(normalize=True)[1]*100)

# End 2.1
# -------------------
# Punkt 2.2.
print("Punkt 2.2.")

# df -> singletons
print(df)
# tworze nową kolumne ientyfikująca dziecko czy jest poniżej <MinDbirwt> -> 1, a powyżej <MinDbirwt> -> 0
# Warunki zadania: dbirwt < 2700gram :lbw = 1, w przeciwnym przypadku lbw = 0
df['lbw'] = np.where(df['dbirwt'] < MinDbirwt, 1, 0)
print(df)

# tobacco = 1 -> pali

df_filtred = df[['mort', 'dbirwt', 'infant_id', 'tobacco', 'lbw']]

print(df_filtred)

X = df['dbirwt']
y = df['tobacco']
print("Minimalna waga dziecka: ", X.min())
print("Maksymalna waga dziecka: ", X.max())
X = X.values.reshape(-1, 1)
print(X)
"""
print(len(X))
X_train = X[:15000]
X_test = X[15000:]

Y_train = y[:15000]
Y_test = y[15000:]

plt.plot(X, y, '.')
plt.ylabel("ibw")
plt.xlabel("ibw")
plt.show()
"""
# Initialise and fit model
model = LinearRegression().fit(X, y)    #(X_train, Y_train)
model2 = LogisticRegression(solver='liblinear', random_state=0).fit(X, y)

print('Coefficients(a): (LinearRegression) ', model.coef_[0])
print('intercept_(b): (LinearRegression) ', model.intercept_)

print('\nCoefficients(a): (LogisticRegression)  ', model2.coef_[0][0])
print('intercept_(b): (LogisticRegression)  ', model2.intercept_[0])

# Plot outputs
plt.scatter(X, y,  color='black')
x = np.linspace(X.min(), X.max(), 100)
y_line = model.coef_[0] * x + model.intercept_
plt.plot(x, y_line, color='blue', linewidth=3)
plt.title('LinearRegression')
plt.show()

#LogicalRegresion
a_v = model2.coef_[0][0]
#print(a_v)
b_v = model2.intercept_[0]
#print(b_v)
y_line_logic = []
plt.scatter(X, y,  color='black')
x = np.linspace(X.min(), X.max(), 100)
for i in x:
    y = ((1 / (1 + math.exp(- (i * a_v)))) + b_v)   #logical
    y_line_logic.append(y)
# Plot outputs
plt.plot(x, y_line_logic, color='blue', linewidth=3)
plt.title('LogisticRegression')
plt.show()



###

