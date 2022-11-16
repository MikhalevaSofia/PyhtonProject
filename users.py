import os

import pandas as pd


def add_user_tiker(id: int, tiker: str):
    global users_df
    user_df = users_df.loc[users_df['id'] == id]
    if user_df.empty:
        users_df = users_df.append({'id': id, 'tikers': tiker}, ignore_index=True)
    else:
        users_df.loc[users_df['id'] == id, 'tikers'] = \
            add_tiker_to_str(get_user_tikers(id), tiker)
    print(users_df)
    save_csv()
    return users_df


def check_include_tiker(user_tikers: str, tiker: str):
    flag = True
    for old_tiker in user_tikers.split(','):
        if tiker == old_tiker:
            flag = False
            break
    return flag


def add_tiker_to_str(user_tikers: str, tiker: str):
    if check_include_tiker(user_tikers, tiker):
        user_tikers += ',' + tiker
    return user_tikers


def delete_tiker_from_str(id: int, tiker: str, user_tikers: str):
    if check_include_tiker(get_user_tikers(id), tiker):
        return 'Такого тикера нет!'
    else:
        for need_tiker in user_tikers.split(','):
            if tiker != need_tiker:
                user_tikers += tiker


def build_menu(buttons, n_cols, user_tikers: str):
    count_tikers = 0
    for tiker in user_tikers.split(','):
        count_tikers += 1

    menu = [buttons[i:i + n_cols] for i in range(0, count_tikers, n_cols)]


#     тут мы должны получить от пользователя значение переменной tiker, чтобы направить его в функцию
# delete_tiker_from_str, в которой он удалится


def save_csv():
    global users_df, name_file
    users_df.to_csv(name_file, index=False)


def load_from_csv():
    global name_file
    for file in os.listdir('./'):
        if file.endswith(name_file):
            return pd.read_csv(name_file)
    return pd.DataFrame(columns=['id', 'tikers'])


def check_picture_of_tiker(tiker):
    for file in os.path.isfile(f'resources/Figure'):
        if file.startswitch(tiker):
            return True
        else:
            return False


def get_user_tikers(id: int):
    global users_df
    if users_df.empty or users_df.loc[users_df['id'] == id].empty:
        return ''
    else:
        return users_df.loc[users_df['id'] == id, 'tikers'].iat[0]


name_file = 'users.csv'
users_df = load_from_csv()
