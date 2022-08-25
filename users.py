import pandas as pd


def save_users(tikers_df: pd.DataFrame, id: int, tiker: str):
    user_df = tikers_df.loc[tikers_df['id'] == id]
    if user_df.empty:
        user_df.loc[0, 'id'] = id
        user_df.loc[0, 'tikers'] = tiker
        tikers_df = tikers_df.append({'id': id, 'tikers': tiker}, ignore_index=True)
    print(tikers_df)
    return tikers_df
