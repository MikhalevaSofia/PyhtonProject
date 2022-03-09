# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('resources/US1.AAPL_210224_220224.csv', sep=';',
                 low_memory=False)
df['<CLOSE>'] = df['<CLOSE>'].astype(float)
df['<DATE>'] = pd.to_datetime(arg=df['<DATE>'], infer_datetime_format=format('%d.%m.%Y'))
plt.title('График изменения цен акций')
plt.xlabel('Дата')
plt.ylabel('Цена')
plt.plot(df['<DATE>'], df['<CLOSE>'])
plt.show()
