# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and set

import apimoex
import pandas as pd
import requests
import matplotlib
from matplotlib import pyplot as plt

plt.rcParams['font.size'] = '8'
plt.switch_backend('Agg')


def check_tiker(tiker):
    with requests.Session() as session:
        data = apimoex.get_board_history(session, tiker, start='2022-08-01', end='2022-08-11',
                                         columns=('CLOSE', 'LOW', 'HIGH', 'TRADEDATE'))
        check_df = pd.DataFrame(data)
        if check_df.empty:
            return False
        else:
            return True


def get_calculation(tiker):
    if users.check_picture_of_tiker(tiker) == False:
        with requests.Session() as session:
            data = apimoex.get_board_history(session, tiker, start='2022-07-11', end='2022-09-11',
                                             columns=('CLOSE', 'LOW', 'HIGH', 'TRADEDATE'))
            df = pd.DataFrame(data)
        if df.empty:
            return 'Это не тикер!!'
    else:
        return pd.DataFrame()

    calc = pd.DataFrame()
    calc['close'] = df['CLOSE'].astype(float)
    calc['low'] = df['LOW'].astype(float)
    calc['high'] = df['HIGH'].astype(float)
    calc['date'] = df['TRADEDATE']
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
    picture_of_close_price(calc, tiker)
    picture_of_sma(calc, tiker)
    picture_of_mom(calc, tiker)
    picture_of_roc(calc, tiker)
    picture_of_rsi(calc, tiker)
    picture_of_k_and_r(calc, tiker)
    picture_of_d(calc, tiker)
    print(calc)
    return 'Расчёты готовы!'


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


def picture_of_close_price(calc: pd.DataFrame, tiker: str):
    fig, ax = plt.subplots()
    ax.set_title('График изменения цен закрытия акций')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Цена')
    ax.legend(['Цена закрытия'])
    ax.plot(calc['date'], calc['close'])
    fig.autofmt_xdate(rotation=90)
    plt.grid(True)
    fig.savefig(f'resources/Figure/{tiker}_Цена закрытия.png')


def picture_of_sma(calc: pd.DataFrame, tiker: str):
    fig, ax = plt.subplots()
    ax.set_title('График скользящих средних')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Цена')
    ax.plot(calc['7 days'])
    ax.plot(calc['14 days'])
    ax.plot(calc['21 days'])
    ax.plot(calc['date'], calc['cross1'], 'ro', color='red')
    ax.plot(calc['date'], calc['cross2'], 'ro', color='red')
    ax.plot(calc['date'], calc['cross3'], 'ro', color='red')
    ax.legend(['Цена закрытия', '7 дней', '14 дней', '21 день', 'Сигналы на покупку/продажу'])
    fig.autofmt_xdate(rotation=90)
    plt.grid(True)
    fig.savefig(f'resources/Figure/{tiker}_График скоьзящих средних.png')


def picture_of_mom(calc: pd.DataFrame, tiker: str):
    fig, ax = plt.subplots()
    ax.set_title('График MOM')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Прирост')
    ax.plot(calc['date'], calc['mom'])
    ax.plot(calc['date'], calc['line0'])
    ax.plot(calc['date'], calc['buyMom'], 'ro', color='red')
    ax.plot(calc['date'], calc['sellMom'], 'ro', color='blue')
    ax.legend(['MOM', 'Ось симметрии', 'Сигналы на покупку', 'Сигналы на продажу'])
    fig.autofmt_xdate(rotation=90)
    plt.grid(True)
    fig.savefig(f'resources/Figure/{tiker}_График MOM.png')


def picture_of_roc(calc: pd.DataFrame, tiker: str):
    fig, ax = plt.subplots()
    ax.set_title('График ROC')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Скорость изменения цены')
    ax.plot(calc['date'], calc['roc'])
    ax.plot(calc['date'], calc['line100'])
    ax.legend(['ROC', 'Уровень запаздывания сигналов'])
    fig.autofmt_xdate(rotation=90)
    plt.grid(True)
    fig.savefig(f'resources/Figure/{tiker}_График ROC.png')


def picture_of_rsi(calc: pd.DataFrame, tiker: str):
    fig, ax = plt.subplots()
    ax.set_title('График RSI')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Цена')
    ax.plot(calc['date'], calc['rsi'])
    ax.plot(calc['date'], calc['line75'])
    ax.plot(calc['date'], calc['line25'])
    ax.plot(calc['date'], calc['buyRsiS'], 'ro', color='red')
    ax.plot(calc['date'], calc['sellRsiS'], 'ro', color='blue')
    ax.plot(calc['date'], calc['buyRsiW'], 'ro', color='darkred')
    ax.plot(calc['date'], calc['sellRsiW'], 'ro', color='navy')
    ax.legend(
        ['RSI', 'Зона перекупленности', 'Зона перепроданности', 'Сильные сигналы на покупку',
         'Сильные сигналы на продажу',
         'Слабые сигналы на покупку', 'Слабые сигналы на продажу'])
    fig.autofmt_xdate(rotation=90)
    plt.grid(True)
    fig.savefig(f'resources/Figure/{tiker}_График RSI.png')


def picture_of_k_and_r(calc: pd.DataFrame, tiker: str):
    fig, ax = plt.subplots()
    ax.set_title('График стохастических линий: %K и %R')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Процент')
    ax.plot(calc['date'], calc['k'])
    ax.plot(calc['date'], calc['r'])
    ax.plot(calc['date'], calc['buyKR'], 'ro', color='red')
    ax.plot(calc['date'], calc['sellKR'], 'ro', color='blue')
    ax.legend(['%K', '%R', 'Сигналы на покупку', 'Сигналы на продажу'])
    fig.autofmt_xdate(rotation=90)
    plt.grid(True)
    fig.savefig(f'resources/Figure/{tiker}_График стохастических линий: %K и %R.png')
    print('Я сохранил! k_and_r')


def picture_of_d(calc: pd.DataFrame, tiker: str):
    fig, ax = plt.subplots()
    ax.set_title('График стохастических линий: %D')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Процент')
    ax.plot(calc['date'], calc['d'])
    ax.plot(calc['date'], calc['buyD'], 'ro', color='red')
    ax.plot(calc['date'], calc['sellD'], 'ro', color='blue')
    ax.legend(['%D', 'Сигналы на покупку', 'Сигналы на продажу'])
    fig.autofmt_xdate(rotation=90)
    plt.grid(True)
    fig.savefig(f'resources/Figure/{tiker}_График стохастических линий: %D.png')
