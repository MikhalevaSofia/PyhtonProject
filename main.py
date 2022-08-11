# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import apimoex
import pandas as pd
import requests

tiker = input()
board = 'TQBR'
with requests.Session() as session:
    data = apimoex.get_board - history(session, tiker, start='2020-08-11', end='2022-08-11',
                                       columns=('CLOSE', 'LOW', 'HIGH', 'TRADEDATE'))

# df = pd.read_csv('resources/US1.AAPL_210224_220224.csv', sep=';')
# df = pd.read_csv('resources/Котировки акций Ростелекома.csv', sep=';')
calc = pd.DataFrame()
calc['close'] = df['<CLOSE>'].astype(float)
calc['low'] = df['<LOW>'].astype(float)
calc['high'] = df['<HIGH>'].astype(float)
calc['date'] = df['<DATE>']


def calc_simple_moving_average(x, days):
    sma_df = pd.DataFrame({'data': []})
    amount = 0.0

    for i in range(0, days):
        amount = amount + x.loc[i]

    for i in range(0, x.values.size + 1 - days):
        sma_df.loc[i + days - 1] = amount / days
        if i <= x.values.size - days - 1:
            amount = amount - x.loc[i] + x.loc[i + days]
    return sma_df


def calc_growth_for_rsi(x):
    growth_df = pd.DataFrame({'data': []})
    for i in range(0, x.values.size - 1):
        growth_df.loc[i + 1] = x.loc[i + 1] - x.loc[i]
    return growth_df


def calc_relative_strength_index(x, days):
    rsi_df = pd.DataFrame({'data': []})
    for i in range(1, x.values.size + 1 - days):
        l = i
        pos_sum = 0.0
        neg_sum = 0.0
        for l in range(l, l + days):
            if x.loc[l] > 0:
                pos_sum = pos_sum + x.loc[l]
            else:
                if x.loc[l] < 0:
                    neg_sum = neg_sum + x.loc[l]
        if neg_sum == 0:
            rsi_df.loc[i + days - 1] = 0
        else:
            rsi_df.loc[i + days - 1] = 100 - (100 / (1 + (pos_sum / abs(neg_sum))))
    return rsi_df


# ВЫЧИСЛЕНИЕ ПРОЦЕНТА D
def calc_min_for_d(x, days):
    min_df = pd.DataFrame({'data': []})
    for i in range(0, x.values.size - days + 1):

        minimum = x.loc[i]
        for l in range(i, i + days - 1):

            if x.loc[l + 1] < minimum:
                minimum = x.loc[l + 1]

        min_df.loc[i] = minimum
    return min_df


def calc_for_d1(x, y):
    difference1_df = pd.DataFrame({'data': []})
    for i in range(5, x.values.size):
        difference1_df.loc[i] = x.loc[i] - y.loc[i - 5]
    return difference1_df


def calc_max_for_d(x, days):
    max_df = pd.DataFrame({'data': []})
    for i in range(0, x.values.size - days + 1):

        maximum = x.loc[i]
        for l in range(i, i + days - 1):

            if x.loc[l + 1] > maximum:
                maximum = x.loc[l + 1]

        max_df.loc[i] = maximum
    return max_df


def calc_for_d2(x, y):
    difference2_df = pd.DataFrame({'data': []})
    for i in range(0, x.values.size):
        difference2_df.loc[i + 5] = x.loc[i] - y.loc[i]
    return difference2_df


def calc_d(t, e):
    d_df = pd.DataFrame({'data': []})
    for i in range(5, t.values.size - 2):
        s1 = t.loc[i] + t.loc[i + 1] + t.loc[i + 2]
        s2 = e.loc[i] + e.loc[i + 1] + e.loc[i + 2]
        d_df.loc[i + 2] = (s1 / s2) * 100
    return d_df


def calc_r_and_k(x, y, z, days):
    rk_df = pd.DataFrame({'data': []})
    for i in range(0, x.values.size - days + 1):
        min_for_r = x.iloc[i:(i + days)].min()
        max_for_r = y.iloc[i:(i + days)].max()
        rk_df.loc[i + days - 1, 'r'] = 100 * (max_for_r - z.loc[i + days - 1]) / (max_for_r - min_for_r)
        rk_df.loc[i + days - 1, 'k'] = 100 * (z.loc[i + days - 1] - min_for_r) / (max_for_r - min_for_r)
    return rk_df


def calc_mom_and_roc(y, days):
    mr_df = pd.DataFrame()
    for i in range(0, y.values.size + 1 - days):
        mr_df.loc[i + days - 1, 'mom'] = y.loc[i + days - 1] - y.loc[i]
        mr_df.loc[i + days - 1, 'roc'] = y.loc[i + days - 1] / y.loc[i] * 100
    return mr_df


def line_for_momentum(y, days):
    line0_df = pd.DataFrame({'data': []})
    for i in range(0, y.values.size + 1 - days):
        line0_df.loc[i + days - 1] = 0
    return line0_df


def line75_for_rsi(y, days):
    line75_df = pd.DataFrame({'data': []})
    for i in range(0, y.values.size + 1 - days):
        line75_df.loc[i + days - 1] = 75
    return line75_df


def line25_for_rsi(y, days):
    line25_df = pd.DataFrame({'data': []})
    for i in range(0, y.values.size + 1 - days):
        line25_df.loc[i + days - 1] = 25
    return line25_df


def line100_for_roc(y, days):
    line100_df = pd.DataFrame({'data': []})
    for i in range(0, y.values.size + 1 - days):
        line100_df.loc[i + days - 1] = 100
    return line100_df


def cross_sma(x, y, days):
    cross_df = pd.DataFrame({'data': []})
    for i in range(0, y.values.size - days):
        if ((x.loc[i + days - 1] > y.loc[i + days - 1]) and (x.loc[i + days] < y.loc[i + days])) or (
                abs(x.loc[i + days - 1] - y.loc[i + days - 1]) == 0.5) or (
                (x.loc[i + days - 1] < y.loc[i + days - 1]) and (x.loc[i + days] > y.loc[i + days])):
            cross_df.loc[i + days - 1] = x.loc[i + days - 1]
    return cross_df


def cross_mom(x, y, days):
    sb_df = pd.DataFrame()
    for i in range(0, x.values.size - days - 1):
        if x.loc[i + days] == y.loc[i + days]:
            if x.loc[i + days - 1] < y.loc[i + days + 1]:
                sb_df.loc[i + days, 'buy'] = y.loc[i + days]
            elif x.loc[i + days - 1] > y.loc[i + days + 1]:
                sb_df.loc[i + days, 'sell'] = y.loc[i + days]
        if x.loc[i + days - 1] < 0 and x.loc[i + days] > 0:
            sb_df.loc[i + days - 1, 'buy'] = y.loc[i + days]
        elif x.loc[i + days - 1] > 0 and x.loc[i + days] < 0:
            sb_df.loc[i + days - 1, 'sell'] = y.loc[i + days]
        if x.loc[i + days] > x.loc[i + days - 1] and x.loc[i + days] >= x.loc[i + days + 1] and x.loc[i + days] > 0:
            sb_df.loc[i + days, 'buy'] = x.loc[i + days]
        if x.loc[i + days] < x.loc[i + days - 1] and x.loc[i + days] <= x.loc[i + days + 1] and x.loc[i + days] < 0:
            sb_df.loc[i + days, 'sell'] = x.loc[i + days]
    return sb_df


def cross_rsi_strong(x, y, z, days):
    cs_df = pd.DataFrame()
    for i in range(0, x.values.size - days - 1):
        if x.loc[i + days] == y.loc[i + days] and x.loc[i + days - 1] < y.loc[i + days + 1]:
            cs_df.loc[i + days, 'buyRsiS'] = y.loc[i + days]
        if x.loc[i + days - 1] < 25 and x.loc[i + days] > 25:
            cs_df.loc[i + days - 1, 'buyRsiS'] = y.loc[i + days]
        if x.loc[i + days] == z.loc[i + days] and x.loc[i + days - 1] > z.loc[i + days + 1]:
            cs_df.loc[i + days, 'sellRsiS'] = y.loc[i + days]
        if x.loc[i + days - 1] > 75 and x.loc[i + days] < 75:
            cs_df.loc[i + days - 1, 'sellRsiS'] = z.loc[i + days]

    return cs_df


def cross_rsi_weak(x, days):
    cr_df = pd.DataFrame()
    for i in range(0, x.values.size - days - 1):
        if x.loc[i + days] > x.loc[i + days - 1] \
                and x.loc[i + days] >= x.loc[i + days + 1] and x.loc[i + days] > 75:
            cr_df.loc[i + days, 'sellRsiW'] = x.loc[i + days]
        if x.loc[i + days] < x.loc[i + days - 1] \
                and x.loc[i + days] <= x.loc[i + days + 1] and x.loc[i + days] < 25:
            cr_df.loc[i + days, 'buyRsiW'] = x.loc[i + days]
    return cr_df


def cross_k_and_r(x, y, days):
    kr_df = pd.DataFrame()
    for i in range(0, x.values.size - days - 1):
        if x.loc[i + days] > x.loc[i + days - 1] and x.loc[i + days] >= x.loc[i + days + 1]:
            kr_df.loc[i + days, 'sell'] = x.loc[i + days]
        if y.loc[i + days] > y.loc[i + days - 1] and y.loc[i + days] >= y.loc[i + days + 1]:
            kr_df.loc[i + days, 'buy'] = y.loc[i + days]
    return kr_df


def cross_d(x, days):
    d_df = pd.DataFrame()
    for i in range(0, x.values.size - days - 1):
        if x.loc[i + days] > x.loc[i + days - 1] and x.loc[i + days] >= x.loc[i + days + 1]:
            d_df.loc[i + days, 'sell'] = x.loc[i + days]
        if x.loc[i + days] < x.loc[i + days - 1] and x.loc[i + days] <= x.loc[i + days + 1]:
            d_df.loc[i + days, 'buy'] = x.loc[i + days]
    return d_df


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
r_and_k_df = calc_r_and_k(calc['low'], calc['high'], calc['close'], 7)
calc['r'] = r_and_k_df['r']
calc['k'] = r_and_k_df['k']
mom_and_roc_df = calc_mom_and_roc(calc['close'], 7)
calc['mom'] = mom_and_roc_df['mom']
calc['roc'] = mom_and_roc_df['roc']
calc['line0'] = line_for_momentum(calc['close'], 7)
calc['line75'] = line75_for_rsi(calc['close'], 7)
calc['line25'] = line25_for_rsi(calc['close'], 7)
calc['line100'] = line100_for_roc(calc['close'], 7)
calc['cross1'] = cross_sma(calc['7 days'], calc['14 days'], 7)
calc['cross2'] = cross_sma(calc['7 days'], calc['21 days'], 7)
calc['cross3'] = cross_sma(calc['14 days'], calc['21 days'], 7)
sell_and_buy_df = cross_mom(calc['mom'], calc['line0'], 7)
calc['buyMom'] = sell_and_buy_df['buy']
calc['sellMom'] = sell_and_buy_df['sell']
sell_and_buy_rsi_strong_df = cross_rsi_strong(calc['rsi'], calc['line25'], calc['line75'], 7)
calc['buyRsiS'] = sell_and_buy_rsi_strong_df['buyRsiS']
calc['sellRsiS'] = sell_and_buy_rsi_strong_df['sellRsiS']
sell_and_buy_rsi_weak_df = cross_rsi_weak(calc['rsi'], 7)
calc['buyRsiW'] = sell_and_buy_rsi_weak_df['buyRsiW']
calc['sellRsiW'] = sell_and_buy_rsi_weak_df['sellRsiW']
cross_k_and_r_df = cross_k_and_r(calc['k'], calc['r'], 7)
calc['buyKR'] = cross_k_and_r_df['buy']
calc['sellKR'] = cross_k_and_r_df['sell']
cross_d_df = cross_d(calc['d'], 7)
calc['buyD'] = cross_d_df['buy']
calc['sellD'] = cross_d_df['sell']

print(calc)

# fig0 = plt.figure()
#
# plt.title('График изменения цен закрытия акций')
# plt.xlabel('Дата')
# plt.ylabel('Цена')
# plt.plot(calc['date'], calc['close'])
# fig0.legend(['Цена закрытия'])
# fig0.autofmt_xdate()
# fig0.show()
#
# fig1 = plt.figure()
# plt.title('График скользящих средних')
# plt.xlabel('Дата')
# plt.ylabel('Цена')
#
# plt.plot(calc['date'], calc['close'])
#
# plt.plot(calc['7 days'])
# plt.plot(calc['14 days'])
# plt.plot(calc['21 days'])
# plt.plot(calc['date'], calc['cross1'], 'ro', color='red')
# plt.plot(calc['date'], calc['cross2'], 'ro', color='red')
# plt.plot(calc['date'], calc['cross3'], 'ro', color='red')
# fig1.legend(['Цена закрытия', '7 дней', '14 дней', '21 день', 'Сигналы на покупку/продажу'])
# fig1.autofmt_xdate()
# fig1.show()
#
# fig2 = plt.figure()
# plt.title('График MOM')
# plt.xlabel('Дата')
# plt.ylabel('Прирост')
# plt.plot(calc['date'], calc['mom'])
# plt.plot(calc['date'], calc['line0'])
# plt.plot(calc['date'], calc['buyMom'], 'ro', color='red')
# plt.plot(calc['date'], calc['sellMom'], 'ro', color='blue')
# fig2.legend(['MOM', 'Ось симметрии', 'Сигналы на покупку', 'Сигналы на продажу'])
# fig2.autofmt_xdate()
# fig2.show()
#
# fig3 = plt.figure()
# plt.title('График ROC')
# plt.xlabel('Дата')
# plt.ylabel('Скорость изменения цены')
# plt.plot(calc['date'], calc['roc'])
# plt.plot(calc['date'], calc['line100'])
# fig3.legend(['ROC', 'Уровень запаздывания сигналов'])
# fig3.autofmt_xdate()
# fig3.show()
#
# fig4 = plt.figure()
# plt.title('График RSI')
# plt.xlabel('Дата')
# plt.ylabel('Цена')
# plt.plot(calc['date'], calc['rsi'])
# plt.plot(calc['date'], calc['line75'])
# plt.plot(calc['date'], calc['line25'])
# plt.plot(calc['date'], calc['buyRsiS'], 'ro', color='red')
# plt.plot(calc['date'], calc['sellRsiS'], 'ro', color='blue')
# plt.plot(calc['date'], calc['buyRsiW'], 'ro', color='darkred')
# plt.plot(calc['date'], calc['sellRsiW'], 'ro', color='navy')
# fig4.legend(
#     ['RSI', 'Зона перекупленности', 'Зона перепроданности', 'Сильные сигналы на покупку', 'Сильные сигналы на продажу',
#      'Слабые сигналы на покупку', 'Слабые сигналы на продажу'])
# fig4.autofmt_xdate()
# fig4.show()
#
# fig5 = plt.figure()
# plt.title('График стохастических линий: %K и %R')
# plt.xlabel('Дата')
# plt.ylabel('Процент')
# plt.plot(calc['date'], calc['k'])
# plt.plot(calc['date'], calc['r'])
# plt.plot(calc['date'], calc['buyKR'], 'ro', color='red')
# plt.plot(calc['date'], calc['sellKR'], 'ro', color='blue')
# fig5.legend(['%K', '%R', 'Сигналы на покупку', 'Сигналы на продажу'])
# fig5.autofmt_xdate()
# fig5.show()
#
# fig6 = plt.figure()
# plt.title('График стохастических линий: %D')
# plt.xlabel('Дата')
# plt.ylabel('Процент')
# plt.plot(calc['date'], calc['d'])
# plt.plot(calc['date'], calc['buyD'], 'ro', color='red')
# plt.plot(calc['date'], calc['sellD'], 'ro', color='blue')
# fig6.legend(['%D', 'Сигналы на покупку', 'Сигналы на продажу'])
# fig6.autofmt_xdate()
# fig6.show()
#
# plt.show()
