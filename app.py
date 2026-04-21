import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

import preprocess,helper


st.set_page_config(
    page_title="Olympics Analytics",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: white;
    }
    h1, h2, h3 {
        color: #f5c542;
    }
    .stDataFrame {
        background-color: #1c1f26;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)


with st.spinner("⏳ Loading data... Please wait"):
    df = pd.read_csv('athlete_ipl.csv')
    region_df = pd.read_csv('noc_regions.csv')
    df = preprocess.preprocess(df,region_df)
    

st.sidebar.header("Summer Olympics Analysis: ")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis','Country-wise Analysis', 'Athelete-wise Analysis')  
)


st.header("Summer Olympics Analysis: ")
# st.dataframe(df)
# Medal tally for teams yearwise

if user_menu == 'Medal Tally':
    # st.sidebar.header('Medal Tally')
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year: ', years)
    selected_country = st.sidebar.selectbox('Select Country: ', country)
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Medal Tally: ')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally ' + str(selected_year) + ' Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Medal Tally: ')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + "'s performance in "+ str(selected_year) + ' Olympics')
        
    
    st.dataframe(medal_tally)
    
    
# Statstics of each atributes 
if user_menu == 'Overall Analysis':
    editions = df['Year'].nunique()
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    atheletes = df['Name'].nunique()
    nations = df['region'].nunique()
    
    st.title('Top Statistics: ')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Editions: ")
        st.title(editions)
    with col2:
        st.subheader("Hosts: ")
        st.title(cities)
    with col3:
        st.subheader("Sports: ")
        st.title(sports)
        
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Events: ")
        st.title(events)
    with col2:
        st.subheader("Atheletes: ")
        st.title(atheletes)
    with col3:
        st.subheader("Nations: ")
        st.title(nations)
        
    nations_over_time = helper.data_over_time(df, 'region')
    fig1 = px.line(nations_over_time, x = 'Year', y = 'count')
    st.header('Participating Nations over time: ')
    st.plotly_chart(fig1, key="chart_1")

    events_over_time = helper.data_over_time(df, 'Event')
    fig2 = px.line(events_over_time, x = 'Year', y = 'count')
    st.header('Events over time: ')
    st.plotly_chart(fig2, key="chart_2")

    atheletes_over_time = helper.data_over_time(df, 'Name')
    fig3 = px.line(atheletes_over_time, x = 'Year', y = 'count')
    st.header('Atheletes over time: ')
    # st.dataframe(atheletes_over_time)
    st.plotly_chart(fig3, key="chart_3")

    st.subheader("No. of Events over time(Every Sport): ")
    fig,ax = plt.subplots(figsize = (15,15))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index= 'Sport', columns='Year', values="Event", aggfunc='count').fillna(0).astype('int'), annot=True)

    st.pyplot(fig)
    
    # Participation trend based on sex over year
    st.subheader("Participation trend based on sex over year: ")
    x = df.groupby("Year")["Sex"].value_counts().reset_index()
    fig = sns.relplot(x, x = 'Year', y = 'count', hue= 'Sex', kind= 'line')
    st.pyplot(fig)





if user_menu == 'Athelete-wise Analysis':
    st.header("Most successful athelete of all time: ")
    st.subheader("Filters: ")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    col1, col2 = st.columns([1, 3])
    with col1:
        selected_sport = st.selectbox("Select a sport: ", sport_list, key="Select_1")
    x = helper.most_successful_athelete(df, selected_sport)
    st.dataframe(x)
    
    st.header("Yearwise most successful athelete: ")
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')
    region = df[~df['region'].isna()]['region'].unique().tolist()
    region.sort()
    region.insert(0,'Overall')
    st.subheader("Filters: ")
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_year = st.selectbox('Select Year:', years, key="Select_2")
    with col2:
        selected_sport = st.selectbox('Select a sport:', sport_list, key="Select_3")
    with col3:
        selected_region = st.selectbox('Select a region:', region, key="Select_4")
    x = helper.most_successful_athelete_of_the_year(df, selected_sport, selected_year, selected_region)
    st.dataframe(x)
    
    # plot age vs medalist
    st.header("Medal tally vs age distribution:")
    age_df = df[df['Age'].notna()]

    fig = px.histogram(
        age_df,
        x="Age",
        color="Medal",  # optional
        barmode="overlay",
        opacity=0.6
    )

    st.plotly_chart(fig, key="age_distribution")
    
    st.header("Medal tally vs Sex distribution:")
    st.subheader("Filters: ")
    col1, col2 = st.columns([1, 3])
    with col1:
        selected_sport = st.selectbox("Select a sport: ", sport_list)
    # scatterplot 
    if(selected_sport == 'Overall'):
        st.subheader("Select a sport for further analysis view: ")
    if(selected_sport != 'Overall'):
        temp_df = df[df['Sport']  ==  selected_sport]
        temp_df['Medal'] = temp_df['Medal'].fillna("no medal")
        fig, ax = plt.subplots(figsize=(10,10))
        sns.scatterplot(
            data=temp_df,
            x='Weight',
            y='Height',
            hue='Medal',
            style='Sex',
            ax = ax)
        st.pyplot(fig)
    
    
    

if user_menu == 'Country-wise Analysis':
    st.header("Countrywise medal tally: ")
    st.subheader("Filters: ")
    region = df[~df['region'].isna()]['region'].unique().tolist()
    region.sort()
    region.insert(0,'Overall')
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,"Overall")
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        inner_col1, inner_col2 = st.columns(2)
        with inner_col1:
            selected_country = st.selectbox("Select Country: ", region)
        with inner_col2:
            selected_year = st.selectbox("Select year: ", years)
            
    x = helper.countrywise_medal(df, selected_country, selected_year)
    st.dataframe(x)
    
    y = helper.countrywise_medal_plot(df, selected_country)
    # st.dataframe(x)
    fig1 = px.line(y, x = 'Year', y = 'Medal')
    st.header('Medal tally of ' + selected_country +' over time : ')
    st.plotly_chart(fig1, key="chart_1")
    
    
    if selected_country != "Overall":
        st.header("Sportwise medal tally of " + selected_country + ":")

        fig, ax = plt.subplots(figsize=(15, 15))

        x = df[df['Medal'].notna()]

        x = x.drop_duplicates(subset=['NOC','Year','Sport','Event','Medal'])

        x = x[x['region'] == selected_country]

        pivot = x.pivot_table(
            index='Sport',
            columns='Year',
            values='Event',
            aggfunc='count'
        ).fillna(0).astype(int)

        sns.heatmap(pivot, annot=True, ax=ax)

        st.pyplot(fig)
    
        st.header("Top 10 atheletes of "+ selected_country + " : ")
        x = helper.successful_athelete(df, selected_country)
        st.dataframe(x)




