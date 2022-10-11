import pandas as pd


def add_user_tiker(users_df: pd.DataFrame, id: int, tiker: str):
    user_df = users_df.loc[users_df['id'] == id]
    if user_df.empty:
        users_df = users_df.append({'id': id, 'tikers': tiker}, ignore_index=True)
    else:
        users_df.loc[users_df['id'] == id, 'tikers'] = \
            check_include_tiker(users_df.loc[users_df['id'] == id, 'tikers'][0], tiker)
    print(users_df)
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
