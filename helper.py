# def medal_tally(df):
#     valid_years = [1896, 1900, 1904, 1908, 1912, 1920, 1924, 1928, 1932, 1936, 1948, 1952, 1956, 1960, 1964, 1968, 1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004,2008, 2012, 2016]
#     medal_tally = df.drop_duplicates(subset=['NOC','Sport','Event','Year','Team','Medal','Games'])
#     medal_tally = medal_tally[medal_tally['Year'].isin(valid_years)]
#     medal_tally =  medal_tally[medal_tally['Season']=='Summer'].groupby('region')[['Gold','Silver','Bronze']].sum().sort_values('Gold',ascending=False).reset_index()
#     medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']  
    
#     return medal_tally

def country_year_list(df):
    years = df[~df['Year'].isna()]['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')
    country = df[~df['region'].isna()]['region'].unique().tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years, country
    
    
def fetch_medal_tally(df,years,country):
    flag = 0 
    if years == 'Overall' and country == 'Overall':
        temp_df = df
    if years == 'Overall' and country != 'Overall':
        # pass
        flag = 1
        temp_df = df[df['region'] == country]
    if years != 'Overall' and country == 'Overall':
        # pass
        temp_df = df[df['Year'] == int(years)]
    if years != 'Overall' and country != 'Overall':
        # pass
        temp_df = df[(df['region'] == country) & (df['Year'] == int(years))]
    
    if(flag == 1):
        x = temp_df.groupby('Year')[['Gold','Silver','Bronze']].sum().sort_values('Year',ascending=True).reset_index()
    else:
        x = temp_df.groupby('NOC')[['Gold','Silver','Bronze']].sum().sort_values('Gold',ascending=False).reset_index()
        
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    
    return x


# Nations over time
def data_over_time(df, y):
    nations_overtime = df.drop_duplicates(subset=[y,'Year'])['Year'].value_counts().sort_index(ascending=True).reset_index()
    return nations_overtime


# Sport wise medal tally
def most_successful_athelete(df, sport):
    temp_df = df[~df['Medal'].isna()]
    if(sport == 'Overall'):
        temp_df
    else:
        temp_df = temp_df[temp_df['Sport'] == sport]
    return temp_df[['Name','Sport','region']].value_counts().reset_index()


# Year and sport and region wise medal tally
def most_successful_athelete_of_the_year(df, sport, year, region):
    temp_df = df[~df['Medal'].isna()]
    if(sport != 'Overall'):
        temp_df = temp_df[temp_df['Sport'] == sport]
    if(year != 'Overall'):
        temp_df = temp_df[temp_df['Year'] == year]
    if(region != 'Overall'):
        temp_df = temp_df[temp_df['region'] == region]
    return temp_df[['Name','Sport','region']].value_counts().reset_index()

# 
def countrywise_medal(df, region, year):
    temp_df = df[~df['Medal'].isna()]
    if(region == 'Overall' and year == 'Overall'):
        temp_df = df
        return temp_df[['region','Year','Sport']].value_counts().reset_index()
    elif(region != 'Overall' and year == 'Overall'):
        temp_df = temp_df[temp_df['region'] == region]
        return temp_df[['region','Year','Sport']].value_counts().reset_index()
    elif(region == 'Overall' and year != 'Overall'):
        temp_df = temp_df[temp_df['Year'] == year]
        return temp_df[['region','Year','Sport']].value_counts().reset_index()
    else:
        temp_df = temp_df[(temp_df['region'] == region) & (temp_df['Year'] == year)]
        return temp_df[['region','Year','Sport']].value_counts().reset_index()
    
def countrywise_medal_plot(df, region):
    temp_df = df[~df['Medal'].isna()]
    if(region != 'Overall'):
        temp_df = df[df['region'] == region]
    return temp_df.groupby('Year').count()['Medal'].reset_index()
    
    
def successful_athelete(df, region):
    temp_df = df[~df['Medal'].isna()] 
    temp_df = temp_df[temp_df['region'] == region]
    temp_df = temp_df[['Name','Medal']]['Name'].value_counts().sort_values(ascending=False).head(10)
    return temp_df


