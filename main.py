# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import pandas as pd

df = pd.read_csv('resources/US1.AAPL_210224_220224.csv', sep=';')
df['<CLOSE>'] = df['<CLOSE>'].astype(float)
df['<DATE>'] = pd.to_datetime(arg=df['<DATE>'], infer_datetime_format=format('%d.%m.%Y'))
# plt.title('График изменения цен закрытия акций')
# plt.xlabel('Дата')
# plt.ylabel('Цена')
# plt.plot(df['<DATE>'], df['<CLOSE>'])
# plt.show()

calc = pd.DataFrame()


# TODO:
# 1. Как работать с DataFrame (создание/добавление/удаление/изменение индекса)
# 2. Как работает функйция range
# 3. Как работает .loc
# 4. как работает values.size
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

# TODO: ROC и MOM в 1 функцию
def calc_momentum(y, days):
    mom = pd.DataFrame({'data': []})
    for i in range(0, y.values.size + 1 - days):
        mom.loc[i + days - 1] = y.loc[i + days - 1] - y.loc[i]
    return mom


def calc_rate_of_change(z, days):
    roc = pd.DataFrame({'data': []})
    for i in range(0, z.values.size + 1 - days):
        roc.loc[i + days - 1] = z.loc[i + days - 1] / z.loc[i] * 100
    return roc


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


# def calc_momentum(y, days):
#     mr = pd.DataFrame({'mom': [], 'roc': []})
#     i = 0
#     for i in range(0, y.values.size + 1 - days):
#         mom.loc[i + days - 1] = y.loc[i + days - 1] - y.loc[i]
#         roc.loc[i + days - 1] = y.loc[i + days - 1] / y.loc[i] * 100
#     return [mom, roc]


calc['gr'] = calc_growth_for_rsi(df['<CLOSE>'])

calc['rsi'] = calc_relative_strength_index(calc['gr'], 6)

calc['7 days'] = calc_moving_average(df['<CLOSE>'], 7)

calc['14 days'] = calc_moving_average(df['<CLOSE>'], 14)

calc['21 days'] = calc_moving_average(df['<CLOSE>'], 21)

calc['mom'] = calc_momentum(df['<CLOSE>'], 7)

calc['roc'] = calc_rate_of_change(df['<CLOSE>'], 7)

print(calc)

# mr['mom'] = calc_momentum(df['<CLOSE>'], 7)
# mr['roc'] = calc_momentum(df['<CLOSE>'], 7)
# print(mr)
