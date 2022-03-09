# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import csv

import matplotlib.pyplot as plt


def get_data_plot_from_file():
    with open('resources/US1.AAPL_210224_220224.csv') as file:
        data = csv.load(file)
        return data
adsasd
plt.title('График изменения цен акций')
plt.xlable('Дата')
plt.ylable('Цена')
plt.plot(*data_plot(), lable='Цена')
plt.legend()
plt.show()
