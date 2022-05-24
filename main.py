# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import matplotlib.pyplot as plt
import pandas as pd

# df = pd.read_csv('resources/US1.AAPL_210224_220224.csv', sep=';')
df = pd.read_csv('resources/Котировки акций Ростелекома.csv', sep=';')
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


def line100_for_roc(y, days):
    line100 = pd.DataFrame({'data': []})
    for i in range(0, y.values.size + 1 - days):
        line100.loc[i + days - 1] = 100
    return line100


def cross_sma(x, y, days):
    cross = pd.DataFrame({'data': []})
    for i in range(0, y.values.size - days):
        if ((x.loc[i + days - 1] > y.loc[i + days - 1]) and (x.loc[i + days] < y.loc[i + days])) or (
                abs(x.loc[i + days - 1] - y.loc[i + days - 1]) == 0.5) or (
                (x.loc[i + days - 1] < y.loc[i + days - 1]) and (x.loc[i + days] > y.loc[i + days])):
            cross.loc[i + days - 1] = x.loc[i + days - 1]
    return cross


def cross_mom(x, y, days):
    sb = pd.DataFrame()
    for i in range(0, x.values.size - days - 1):
        if x.loc[i + days] == y.loc[i + days]:
            if x.loc[i + days - 1] < y.loc[i + days + 1]:
                sb.loc[i + days, 'buy'] = y.loc[i + days]
            elif x.loc[i + days - 1] > y.loc[i + days + 1]:
                sb.loc[i + days, 'sell'] = y.loc[i + days]
        if x.loc[i + days - 1] < 0 and x.loc[i + days] > 0:
            sb.loc[i + days - 1, 'buy'] = y.loc[i + days]
        elif x.loc[i + days - 1] > 0 and x.loc[i + days] < 0:
            sb.loc[i + days - 1, 'sell'] = y.loc[i + days]
        if x.loc[i + days] > x.loc[i + days - 1] and x.loc[i + days] > x.loc[i + days + 1] and x.loc[i + days] > 0:
            sb.loc[i + days, 'buy'] = x.loc[i + days]
        if x.loc[i + days] < x.loc[i + days - 1] and x.loc[i + days] < x.loc[i + days + 1] and x.loc[i + days] < 0:
            sb.loc[i + days, 'sell'] = x.loc[i + days]
    return sb


# TODO: Разделить слабые и сильные сигналы
def cross_rsi_strong(x, y, z, days):
    cs = pd.DataFrame()
    for i in range(0, x.values.size - days - 1):
        if x.loc[i + days] == y.loc[i + days] and x.loc[i + days - 1] < y.loc[i + days + 1]:
            cs.loc[i + days, 'buyRsiS'] = y.loc[i + days]
        if x.loc[i + days - 1] < 25 and x.loc[i + days] > 25:
            cs.loc[i + days - 1, 'buyRsiS'] = y.loc[i + days]
        if x.loc[i + days] == z.loc[i + days] and x.loc[i + days - 1] > z.loc[i + days + 1]:
            cs.loc[i + days, 'sellRsiS'] = y.loc[i + days]
        if x.loc[i + days - 1] > 75 and x.loc[i + days] < 75:
            cs.loc[i + days - 1, 'sellRsiS'] = z.loc[i + days]

    return cs


def cross_rsi_weak(x, days):
    cr = pd.DataFrame()
    for i in range(0, x.values.size - days - 1):
        if x.loc[i + days] > x.loc[i + days - 1] and x.loc[i + days] >= x.loc[i + days + 1] and x.loc[i + days] > 75:
            cr.loc[i + days, 'sellRsiW'] = x.loc[i + days]
        if x.loc[i + days] < x.loc[i + days - 1] and x.loc[i + days] <= x.loc[i + days + 1] and x.loc[i + days] < 25:
            cr.loc[i + days, 'buyRsiW'] = x.loc[i + days]
    return cr


# TODO: Делать поиск пиков отдельно для %K и %D и убрать 50%
def cross_k_and_r(x, y, days):
    kr = pd.DataFrame()
    for i in range(0, x.values.size - days - 1):
        if x.loc[i + days] > x.loc[i + days - 1] and x.loc[i + days] > x.loc[i + days + 1] and x.loc[i + days] > 50:
            kr.loc[i + days, 'sell'] = x.loc[i + days]
            kr.loc[i + days, 'buy'] = y.loc[i + days]
    return kr


# TODO: Отметить все сигналы
def cross_d(x, days):
    d = pd.DataFrame()
    for i in range(0, x.values.size - days - 1):
        if x.loc[i + days] > x.loc[i + days - 1] and x.loc[i + days] > x.loc[i + days + 1] and x.loc[i + days] > 75:
            d.loc[i + days, 'sell'] = x.loc[i + days]
        if x.loc[i + days] < x.loc[i + days - 1] and x.loc[i + days] < x.loc[i + days + 1] and x.loc[i + days] < 25:
            d.loc[i + days, 'buy'] = x.loc[i + days]
    return d


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
RandK = calc_r_and_k(calc['low'], calc['high'], calc['close'], 7)
calc['r'] = RandK['r']
calc['k'] = RandK['k']
momAndRoc = calc_mom_and_roc(calc['close'], 7)
calc['mom'] = momAndRoc['mom']
calc['roc'] = momAndRoc['roc']
calc['line0'] = line_for_momentum(calc['close'], 7)
calc['line75'] = line75_for_rsi(calc['close'], 7)
calc['line25'] = line25_for_rsi(calc['close'], 7)
calc['line100'] = line100_for_roc(calc['close'], 7)
calc['cross1'] = cross_sma(calc['7 days'], calc['14 days'], 7)
calc['cross2'] = cross_sma(calc['7 days'], calc['21 days'], 7)
calc['cross3'] = cross_sma(calc['14 days'], calc['21 days'], 7)
sb = cross_mom(calc['mom'], calc['line0'], 7)
calc['buyMom'] = sb['buy']
calc['sellMom'] = sb['sell']
sellAndBuyRsiStrong = cross_rsi_strong(calc['rsi'], calc['line25'], calc['line75'], 7)
calc['buyRsiS'] = sellAndBuyRsiStrong['buyRsiS']
calc['sellRsiS'] = sellAndBuyRsiStrong['sellRsiS']
sellAndBuyRsiWeak = cross_rsi_weak(calc['rsi'], 7)
calc['buyRsiW'] = sellAndBuyRsiWeak['buyRsiW']
calc['sellRsiW'] = sellAndBuyRsiWeak['sellRsiW']
kr = cross_k_and_r(calc['k'], calc['r'], 7)
calc['buyKR'] = kr['buy']
calc['sellKR'] = kr['sell']
kr = cross_d(calc['d'], 7)
calc['buyD'] = kr['buy']
calc['sellD'] = kr['sell']

print(calc)
# TODO: Сделать легенду
fig1 = plt.figure()
# plt.subplot(3, 1, 1)
plt.title('График скользящих средних')
plt.xlabel('Дата')
plt.ylabel('Цена')

plt.plot(calc['date'], calc['close'])

plt.plot(calc['7 days'], label='7 дней')
plt.plot(calc['14 days'], label='14 дней')
plt.plot(calc['21 days'], label='21 день')
plt.plot(calc['date'], calc['cross1'], 'ro')
plt.plot(calc['date'], calc['cross2'], 'ro')
plt.plot(calc['date'], calc['cross3'], 'ro')
fig1.legend(['Цена закрытия', '7 дней', '14 дней', '21 дней', 'Сигналы на покупку/продажу'])
plt.grid()
fig1.autofmt_xdate()
fig1.show()

fig2 = plt.figure()
# plt.subplot(3, 1, 2)
plt.title('График MOM')
plt.xlabel('Дата')  # TODO: Это скорость изменения цены
plt.ylabel('Прирост')
plt.plot(calc['date'], calc['mom'])
plt.plot(calc['date'], calc['line0'])
plt.plot(calc['date'], calc['buyMom'], 'ro', color='red')
plt.plot(calc['date'], calc['sellMom'], 'ro', color='blue')
plt.grid()
fig2.autofmt_xdate()
fig2.show()

fig3 = plt.figure()
# plt.subplot(3, 1, 3)
plt.title('График ROC')
plt.xlabel('Дата')  # TODO: Это прирост
plt.ylabel('Скорость изменения цены')
plt.plot(calc['date'], calc['roc'])
# plt.plot(calc['date'], calc['close'])
plt.plot(calc['date'], calc['line100'])
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
plt.plot(calc['date'], calc['buyRsiS'], 'ro', color='red')
plt.plot(calc['date'], calc['sellRsiS'], 'ro', color='blue')
plt.plot(calc['date'], calc['buyRsiW'], 'ro', color='red')
plt.plot(calc['date'], calc['sellRsiW'], 'ro', color='blue')
plt.grid()
fig4.autofmt_xdate()
fig4.show()

fig5 = plt.figure()
# plt.subplot(3, 2, 2)
plt.title('График стохастических линий: процент K и процент R')
plt.xlabel('Дата')  # TODO: Не цена, а процент
plt.ylabel('Процент')
plt.plot(calc['date'], calc['k'])
plt.plot(calc['date'], calc['r'])
plt.plot(calc['date'], calc['buyKR'], 'ro', color='red')
plt.plot(calc['date'], calc['sellKR'], 'ro', color='blue')
plt.grid()
fig5.autofmt_xdate()
fig5.show()

fig6 = plt.figure()
# plt.subplot(3, 2, 3)
plt.title('График стохастических линий: процент D')
plt.xlabel('Дата')  # TODO: Не цена, а процент
plt.ylabel('Процент')
plt.plot(calc['date'], calc['d'])
plt.plot(calc['date'], calc['buyD'], 'ro', color='red')
plt.plot(calc['date'], calc['sellD'], 'ro', color='blue')
plt.grid()
fig6.autofmt_xdate()
fig6.show()

plt.show()
