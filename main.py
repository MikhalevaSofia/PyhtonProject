# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('resources/US1.AAPL_210224_220224.csv', sep=';')
calc = pd.DataFrame()
# TODO: Уже работаем с calc
# TODO: Поправить замечания по стилю
# TODO: Дать переменным осознанные нименования
calc['close'] = df['<CLOSE>'].astype(float)
calc['low'] = df['<LOW>'].astype(float)
calc['high'] = df['<HIGH>'].astype(float)
calc['date'] = df['<DATE>']


def calc_simple_moving_average(x, days):
    sma = pd.DataFrame({'data': []})
    sum = 0.0

    for i in range(0, days):
        sum = sum + x.loc[i]

    for i in range(0, x.values.size + 1 - days):
        sma.loc[i + days - 1] = sum / days
        if i <= x.values.size - days - 1:
            sum = sum - x.loc[i] + x.loc[i + days]
    return sma


def calc_growth_for_rsi(x):
    growth = pd.DataFrame({'data': []})
    for i in range(0, x.values.size - 1):
        growth.loc[i + 1] = x.loc[i + 1] - x.loc[i]
    return growth


def calc_relative_strength_index(x, days):
    rsi = pd.DataFrame({'data': []})
    for i in range(1, x.values.size + 1 - days):
        l = i
        PosSum = 0.0
        NegSum = 0.0
        for l in range(l, l + days):
            if x.loc[l] > 0:
                PosSum = PosSum + x.loc[l]
            else:
                if x.loc[l] < 0:
                    NegSum = NegSum + x.loc[l]
        if NegSum == 0:
            rsi.loc[i + days - 1] = 0
        else:
            rsi.loc[i + days - 1] = 100 - (100 / (1 + (PosSum / abs(NegSum))))
    return rsi


# ВЫЧИСЛЕНИЕ ПРОЦЕНТА D
def calc_min_for_d(x, days):
    min = pd.DataFrame({'data': []})
    for i in range(0, x.values.size - days + 1):

        minimum = x.loc[i]
        for l in range(i, i + days - 1):

            if x.loc[l + 1] < minimum:
                minimum = x.loc[l + 1]

        min.loc[i] = minimum
    return min


def calc_for_d1(x, y):
    difference1 = pd.DataFrame({'data': []})
    for i in range(5, x.values.size):
        difference1.loc[i] = x.loc[i] - y.loc[i - 5]
    return difference1


def calc_max_for_d(x, days):
    max = pd.DataFrame({'data': []})
    for i in range(0, x.values.size - days + 1):

        maximum = x.loc[i]
        for l in range(i, i + days - 1):

            if x.loc[l + 1] > maximum:
                maximum = x.loc[l + 1]

        max.loc[i] = maximum
    return max


def calc_for_d2(x, y):
    difference2 = pd.DataFrame({'data': []})
    for i in range(0, x.values.size):
        difference2.loc[i + 5] = x.loc[i] - y.loc[i]
    return difference2


def calc_d(t, e):
    d = pd.DataFrame({'data': []})
    for i in range(5, t.values.size - 2):
        s1 = t.loc[i] + t.loc[i + 1] + t.loc[i + 2]
        s2 = e.loc[i] + e.loc[i + 1] + e.loc[i + 2]
        d.loc[i + 2] = (s1 / s2) * 100
    return d


# TODO: Объединить calc_r и calc_k
def calc_r_and_k(x, y, z, days):
    rk = pd.DataFrame({'data': []})
    for i in range(0, x.values.size - days + 1):
        minForR = x.iloc[i:(i + days)].min()
        maxForR = y.iloc[i:(i + days)].max()
        rk.loc[i + days - 1, 'r'] = 100 * (maxForR - z.loc[i + days - 1]) / (maxForR - minForR)
        rk.loc[i + days - 1, 'k'] = 100 * (z.loc[i + days - 1] - minForR) / (maxForR - minForR)
    return rk


# def calc_k(t, e, u, days):
#     k = pd.DataFrame({'data': []})
#     for i in range(0, t.values.size - days + 1):
#         minForR = t.iloc[i:(i + days)].min()
#         maxForR = e.iloc[i:(i + days)].max()
#         k.loc[i + days - 1] = 100 * (u.loc[i + days - 1] - minForR) / (maxForR - minForR)
#     return k


def calc_mom_and_roc(y, days):
    mr = pd.DataFrame()
    for i in range(0, y.values.size + 1 - days):
        mr.loc[i + days - 1, 'mom'] = y.loc[i + days - 1] - y.loc[i]
        mr.loc[i + days - 1, 'roc'] = y.loc[i + days - 1] / y.loc[i] * 100
    return mr


def line_for_momentum(y, days):
    line0 = pd.DataFrame({'data': []})
    for i in range(0, y.values.size + 1 - days):
        line0.loc[i + days - 1] = 0
    return line0


def line75_for_rsi(y, days):
    line75 = pd.DataFrame({'data': []})
    for i in range(0, y.values.size + 1 - days):
        line75.loc[i + days - 1] = 75
    return line75


def line25_for_rsi(y, days):
    line25 = pd.DataFrame({'data': []})
    for i in range(0, y.values.size + 1 - days):
        line25.loc[i + days - 1] = 25
    return line25


def cross_sma(x, y, days):
    cs = pd.DataFrame({'data': []})
    for i in range(0, y.values.size - days):
        if ((x.loc[i + days - 1] > y.loc[i + days - 1]) and (x.loc[i + days] < y.loc[i + days])) or (
                abs(x.loc[i + days - 1] - y.loc[i + days - 1]) == 0.5) or (
                (x.loc[i + days - 1] < y.loc[i + days - 1]) and (x.loc[i + days] > y.loc[i + days])):
            cs.loc[i + days - 1] = x.loc[i + days - 1]
    return cs


def cross_sma2(x, y, days):
    cs2 = pd.DataFrame({'data': []})
    for i in range(0, x.values.size - days):
        if abs(x.loc[i + days - 1] - y.loc[i + days - 1]) == 0.5:
            cs2.loc[i + days - 1] = x.loc[i + days - 1]
    return cs2


calc['growth'] = calc_growth_for_rsi(calc['close'])

calc['rsi'] = calc_relative_strength_index(calc['growth'], 6)

calc['7 days'] = calc_simple_moving_average(calc['close'], 7)

calc['14 days'] = calc_simple_moving_average(calc['close'], 14)

calc['21 days'] = calc_simple_moving_average(calc['close'], 21)

calc['min'] = calc_min_for_d(calc['low'], 6)
calc['max'] = calc_max_for_d(calc['high'], 6)
calc['difference1'] = calc_for_d1(calc['close'], calc['min'])
calc['difference2'] = calc_for_d2(calc['max'], calc['min'])
calc['d'] = calc_d(calc['difference1'], calc['difference2'])
# calc['r'] = calc_r(calc['low'], calc['high'], calc['close'], 7)
# calc['k'] = calc_k(calc['low'], calc['high'], calc['close'], 7)
RandK = calc_r_and_k(calc['low'], calc['high'], calc['close'], 7)
calc['r'] = RandK['r']
calc['k'] = RandK['k']
momAndRoc = calc_mom_and_roc(calc['close'], 7)
calc['mom'] = momAndRoc['mom']
calc['roc'] = momAndRoc['roc']
calc['line0'] = line_for_momentum(calc['close'], 7)
calc['line75'] = line75_for_rsi(calc['close'], 7)
calc['line25'] = line25_for_rsi(calc['close'], 7)
calc['cs'] = cross_sma(calc['7 days'], calc['14 days'], 7)
calc['cs2'] = cross_sma2(calc['21 days'], calc['cs'], 7)

print(calc)
fig1 = plt.figure()
# plt.subplot(3, 1, 1)
plt.title('График скользящих средних')
plt.xlabel('Дата')
plt.ylabel('Цена')

plt.plot(calc['date'], calc['close'])

plt.plot(calc['7 days'])
plt.plot(calc['14 days'])
plt.plot(calc['21 days'])
plt.plot(calc['date'], calc['cs'], 'ro')
plt.grid()
fig1.autofmt_xdate()
fig1.show()

fig2 = plt.figure()
# plt.subplot(3, 1, 2)
plt.title('График MOM')
plt.xlabel('Дата')
plt.ylabel('Цена')
plt.plot(calc['date'], calc['mom'])
plt.plot(calc['date'], calc['close'])
plt.plot(calc['date'], calc['line0'])
plt.grid()
fig2.autofmt_xdate()
fig2.show()

fig3 = plt.figure()
# plt.subplot(3, 1, 3)
plt.title('График ROC')
plt.xlabel('Дата')
plt.ylabel('Цена')
plt.plot(calc['date'], calc['roc'])
plt.plot(calc['date'], calc['close'])
plt.grid()
fig3.autofmt_xdate()
fig3.show()

fig4 = plt.figure()
# plt.subplot(3, 2, 1)
plt.title('График RSI')
plt.xlabel('Дата')
plt.ylabel('Цена')
plt.plot(calc['date'], calc['rsi'])
plt.plot(calc['date'], calc['line75'])
plt.plot(calc['date'], calc['line25'])
plt.grid()
fig4.autofmt_xdate()
fig4.show()

fig5 = plt.figure()
# plt.subplot(3, 2, 2)
plt.title('График стохастических линий: процент K и процент R')
plt.xlabel('Дата')
plt.ylabel('Цена')
plt.plot(calc['date'], calc['k'])
plt.plot(calc['date'], calc['r'])
plt.grid()
fig5.autofmt_xdate()
fig5.show()

fig6 = plt.figure()
# plt.subplot(3, 2, 3)
plt.title('График стохастических линий: процент D')
plt.xlabel('Дата')
plt.ylabel('Цена')
plt.plot(calc['date'], calc['d'])
plt.grid()
fig6.autofmt_xdate()
fig6.show()

fig7 = plt.figure()
# plt.subplot(3, 2, 1)
plt.title('График пересечений средних')
plt.xlabel('Дата')
plt.ylabel('Цена')
plt.plot(calc['date'], calc['cs'], 'ro')
# plt.grid()
fig7.autofmt_xdate()
fig7.show()
plt.show()
