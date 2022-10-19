import os

import pandas as pd


def add_user_tiker(id: int, tiker: str):
    global users_df
    user_df = users_df.loc[users_df['id'] == id]
    if user_df.empty:
        users_df = users_df.append({'id': id, 'tikers': tiker}, ignore_index=True)
    else:
        users_df.loc[users_df['id'] == id, 'tikers'] = \
            check_include_tiker(get_user_tikers(id), tiker)
    print(users_df)
    save_csv()
    return users_df


def check_include_tiker(user_tikers: str, tiker: str):
    flag = True
    for old_tiker in user_tikers.split(','):
        if tiker == old_tiker:
            flag = False
            break
    if flag:
        user_tikers += ',' + tiker
    return user_tikers


def save_csv():
    global users_df, name_file
    users_df.to_csv(name_file, index=False)


def load_from_csv():
    global name_file
    for file in os.listdir('./'):
        if file.endswith(name_file):
            return pd.read_csv(name_file)
    return pd.DataFrame(columns=['id', 'tikers'])


def get_user_tikers(id: int):
    global users_df
    return users_df.loc[users_df['id'] == id, 'tikers'].iat[0]


users_df = load_from_csv()
name_file = 'users.csv'
