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
calc['close'] = df['<LOW>'].astype(float)
calc['high'] = df['<HIGH>'].astype(float)
calc['date'] = df['<DATE>']


def calc_moving_average(x, days):
    sma = pd.DataFrame({'data': []})
    sum = 0.0

    for i in range(0, days):
        sum = sum + x.loc[i]

    for i in range(0, x.values.size + 1 - days):
        sma.loc[i + days - 1] = sum / days
        if i <= x.values.size - days - 1:
            sum = sum - x.loc[i] + x.loc[i + days]
    return sma





def calc_growth_for_rsi(w):
    gr = pd.DataFrame({'data': []})
    for i in range(0, w.values.size - 1):
        gr.loc[i + 1] = w.loc[i + 1] - w.loc[i]
    return gr


def calc_relative_strength_index(m, days):
    rsi = pd.DataFrame({'data': []})
    PosSum = 0.0
    NegSum = 0.0
    for i in range(1, m.values.size + 2 - days):
        l = i
        for l in range(l, l + days):

            if m.loc[i] > 0:
                PosSum = PosSum + m.loc[i]
            else:
                if m.loc[i] < 0:
                    NegSum = NegSum + m.loc[i]
        grow = PosSum / abs(NegSum)
        rsi.loc[i + days - 1] = 100 - (100 / (1 + grow))
    return rsi


# ВЫЧИСЛЕНИЕ ПРОЦЕНТА D
def calc_min(s, days):
    mi = pd.DataFrame({'data': []})
    for i in range(0, s.values.size - days + 1):

        minimum = s.loc[i]
        for l in range(i, i + days - 1):

            if s.loc[l + 1] < minimum:
                minimum = s.loc[l + 1]

        mi.loc[i] = minimum
    return mi


def calc_cl(k, b):
    cl = pd.DataFrame({'data': []})
    for i in range(5, k.values.size):
        cl.loc[i] = k.loc[i] - b.loc[i - 5]
    return cl


def calc_max(j, days):
    ma = pd.DataFrame({'data': []})
    for i in range(0, j.values.size - days + 1):

        maximum = j.loc[i]
        for l in range(i, i + days - 1):

            if j.loc[l + 1] > maximum:
                maximum = j.loc[l + 1]

        ma.loc[i] = maximum
    return ma


def calc_hl(h, q):
    hl = pd.DataFrame({'data': []})
    for i in range(0, h.values.size):
        hl.loc[i + 5] = h.loc[i] - q.loc[i]
    return hl


def calc_d(t, e):
    d = pd.DataFrame({'data': []})
    for i in range(5, t.values.size - 2):
        s1 = t.loc[i] + t.loc[i + 1] + t.loc[i + 2]
        s2 = e.loc[i] + e.loc[i + 1] + e.loc[i + 2]
        d.loc[i + 2] = (s1 / s2) * 100
    return d


# TODO: Объединить calc_r и calc_k
def calc_r(t, e, k, days):
    r = pd.DataFrame({'data': []})
    for i in range(0, t.values.size - days + 1):
        minForR = t.iloc[i:(i + days)].min()
        maxForR = e.iloc[i:(i + days)].max()
        r.loc[i + days - 1] = 100 * (maxForR - k.loc[i + days - 1]) / (maxForR - minForR)
    return r


def calc_k(t, e, u, days):
    k = pd.DataFrame({'data': []})
    for i in range(0, t.values.size - days + 1):
        minForR = t.iloc[i:(i + days)].min()
        maxForR = e.iloc[i:(i + days)].max()
        k.loc[i + days - 1] = 100 * (u.loc[i + days - 1] - minForR) / (maxForR - minForR)
    return k


def calc_momentum(y, days):
    mr = pd.DataFrame()
    for i in range(0, y.values.size + 1 - days):
        mr.loc[i + days - 1, 'mom'] = y.loc[i + days - 1] - y.loc[i]
        mr.loc[i + days - 1, 'roc'] = y.loc[i + days - 1] / y.loc[i] * 100
    return mr


def calc_for_momentum(y, days):
    l = pd.DataFrame({'data': []})
    for i in range(0, y.values.size + 1 - days):
        l.loc[i + days - 1] = 0
    return l


def calc_for_rsi_one(y, days):
    lineSF = pd.DataFrame({'data': []})
    for i in range(0, y.values.size + 1 - days):
        lineSF.loc[i + days - 1] = 75
    return lineSF


def calc_for_rsi_two(y, days):
    lineTF = pd.DataFrame({'data': []})
    for i in range(0, y.values.size + 1 - days):
        lineTF.loc[i + days - 1] = 25
    return lineTF


def cross_sma(x, y, days):
    cs = pd.DataFrame({'data': []})
    for i in range(0, y.values.size - days):
        if ((x.loc[i + days - 1] > y.loc[i + days - 1]) and (x.loc[i + days] < y.loc[i + days])) or (
                abs(x.loc[i + days - 1] - y.loc[i + days - 1]) == 0.5):
            cs.loc[i + days - 1] = x.loc[i + days - 1]
    return cs


def cross_sma2(x, y, days):
    cs2 = pd.DataFrame({'data': []})
    for i in range(0, x.values.size - days):
        if abs(x.loc[i + days - 1] - y.loc[i + days - 1]) == 0.5:
            cs2.loc[i + days - 1] = x.loc[i + days - 1]
    return cs2


calc['gr'] = calc_growth_for_rsi(calc['close'])

calc['rsi'] = calc_relative_strength_index(calc['gr'], 6)

calc['7 days'] = calc_moving_average(calc['close'], 7)

calc['14 days'] = calc_moving_average(calc['close'], 14)

calc['21 days'] = calc_moving_average(calc['close'], 21)

calc['mi'] = calc_min(calc['low'], 6)
calc['ma'] = calc_max(calc['high'], 6)
calc['cl'] = calc_cl(calc['close'], calc['mi'])
calc['hl'] = calc_hl(calc['ma'], calc['mi'])
calc['d'] = calc_d(calc['cl'], calc['hl'])
calc['r'] = calc_r(calc['low'], calc['high'], calc['close'], 7)
calc['k'] = calc_k(calc['low'], calc['high'], calc['close'], 7)
momAndRoc = calc_momentum(calc['close'], 7)
calc['mom'] = momAndRoc['mom']
calc['roc'] = momAndRoc['roc']
calc['l'] = calc_for_momentum(calc['close'], 7)
calc['lineSF'] = calc_for_rsi_one(calc['close'], 7)
calc['lineTF'] = calc_for_rsi_two(calc['close'], 7)
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
plt.plot(calc['date'], calc['l'])
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
plt.plot(calc['date'], calc['lineSF'])
plt.plot(calc['date'], calc['lineTF'])
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
plt.show()

fig7 = plt.figure()
# plt.subplot(3, 2, 1)
plt.title('График пересечений средних')
plt.xlabel('Дата')
plt.ylabel('Цена')
plt.plot(calc['date'], calc['cs'])
plt.grid()
fig7.autofmt_xdate()
fig7.show()
