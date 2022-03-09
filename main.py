# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import.matplotlib.pyplot as plt
import csv


def get_data_plot():
    with open('US1.AAPL_210224_2202224.csv') as file:
        data = csv.load(file)
        return data


plt.title('График изменения цен акций')
plt.xlable('Дата')
plt.ylable('Цена')
plt.plot(*data_plot(), lable='Цена')
plt.legend()
plt.show()
