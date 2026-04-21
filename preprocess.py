import pandas as pd



def preprocess(df, region_df):
    df = df[df['Season'] == 'Summer']
    df = df.merge(region_df, on='NOC' ,how='left')
    df.drop_duplicates(inplace=True)
    valid_years = [1896, 1900, 1904, 1908, 1912, 1920, 1924, 1928, 1932, 1936, 1948, 1952, 1956, 1960, 1964, 1968, 1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004,2008, 2012, 2016]
    df = df.drop_duplicates(subset=['NOC','Sport','Event','Year','Team','Medal','Games','region'])
    df = df[df['Year'].isin(valid_years)]
    df = pd.concat([df, pd.get_dummies(df['Medal'])],axis=1)
    return df
