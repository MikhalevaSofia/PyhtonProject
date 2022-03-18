# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('resources/US1.AAPL_210224_220224.csv', sep=';')
df['<CLOSE>'] = df['<CLOSE>'].astype(float)
df['<DATE>'] = pd.to_datetime(arg=df['<DATE>'], infer_datetime_format=format('%d.%m.%Y'))
plt.title('График изменения цен закрытия акций')
plt.xlabel('Дата')
plt.ylabel('Цена')
plt.plot(df['<DATE>'], df['<CLOSE>'])
plt.show()

calc = pd.DataFrame()


def calc_moving_average(x, days):
    result = pd.DataFrame({'data'})
    sum = 0.0
    i = 0
    for data in x['<CLOSE>'].values:
        if i=days:


#
#     return x


calc['7 days'] = calc_moving_average(df['<CLOSE>'], 7)
