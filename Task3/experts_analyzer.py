import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

path = './dcm_files/reads.csv'
R1_cols = [
    'R1:ICH', 'R1:IPH', 'R1:IVH', 'R1:SDH', 'R1:EDH', 'R1:SAH', 'R1:BleedLocation-Left',
    'R1:BleedLocation-Right', 'R1:ChronicBleed', 'R1:Fracture', 'R1:CalvarialFracture', 'R1:OtherFracture',
    'R1:MassEffect', 'R1:MidlineShift'
]

R2_cols = [
    'R2:ICH', 'R2:IPH', 'R2:IVH', 'R2:SDH', 'R2:EDH', 'R2:SAH', 'R2:BleedLocation-Left',
    'R2:BleedLocation-Right', 'R2:ChronicBleed', 'R2:Fracture', 'R2:CalvarialFracture', 'R2:OtherFracture',
    'R2:MassEffect', 'R2:MidlineShift'
]

R3_cols = [
    'R3:ICH', 'R3:IPH', 'R3:IVH', 'R3:SDH', 'R3:EDH', 'R3:SAH', 'R3:BleedLocation-Left',
    'R3:BleedLocation-Right', 'R3:ChronicBleed', 'R3:Fracture', 'R3:CalvarialFracture', 'R3:OtherFracture',
    'R3:MassEffect', 'R3:MidlineShift'
]


df_R1 = pd.read_csv(path, usecols=R1_cols)
df_R2 = pd.read_csv(path, usecols=R2_cols)
df_R3 = pd.read_csv(path, usecols=R3_cols)

# Badanie sprawdzające, czy opinie lekarzy radiologów są spójne
R1_sum = df_R1.sum()
R2_sum = df_R2.sum()
R3_sum = df_R3.sum()

values_1 = []
values_2 = []
values_3 = []
for col in R1_cols:
    col = 'R1:' + col[3:]
    values_1.append(R1_sum[col])
    col = 'R2:' + col[3:]
    values_2.append(R2_sum[col])
    col = 'R3:' + col[3:]
    values_3.append(R3_sum[col])

labels = [
            'ICH', 'IPH', 'IVH', 'SDH', 'EDH', 'SAH', 'BleedLocation-Left',
            'BleedLocation-Right', 'ChronicBleed', 'Fracture', 'CalvarialFracture', 'OtherFracture',
            'MassEffect', 'MidlineShift'
          ]


barWidth = 0.25

r1 = np.arange(len(R1_cols))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]

plt.grid(alpha=0.2)
plt.bar(r1, values_1, width=barWidth, edgecolor='white', label='R1')
plt.bar(r2, values_2, width=barWidth, edgecolor='white', label='R2')
plt.bar(r3, values_3, width=barWidth, edgecolor='white', label='R3')

plt.xticks([r + barWidth for r in range(len(R1_cols))], labels, rotation=90)

plt.ylabel('liczba stwierdzonych przypadków')
plt.legend()
plt.show()

# Badanie sprawdzające, czy są jakieś zależności w położeniu i rozmiarze krwiaków
path2 = './dcm_files/1_Initial_Manual_Labeling.csv'
df_IML = pd.read_csv(path2, index_col=None)

sns.jointplot(data=df_IML, x="x", y="y", hue="labelName")
plt.show()

sns.jointplot(data=df_IML, x="width", y="height", hue="labelName")
plt.show()

haematoma_types = ['Intraventricular', 'Intraparenchymal', 'Subarachnoid', 'Chronic', 'Subdural', 'Epidural']

df_IML['size'] = df_IML['width'] * df_IML['height']

sns.displot(df_IML, x="size", hue="labelName", kind="kde", fill=True)
plt.show()

sns.displot(df_IML, x="size", hue="labelName", fill=True)
plt.show()

sns.boxplot(x=df_IML['labelName'], y=df_IML['size'])
plt.xticks(rotation=90)
plt.show()

