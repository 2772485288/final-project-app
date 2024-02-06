# import packages
from asyncore import write
from cgitb import text
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('seaborn-v0_8')

# show the title
st.title('Values of Soccer Players(2021) Analyzing App \n   by Zhiqi Zhu and Shiwen Zhang')

# read csv and show the dataframe
df = pd.read_csv('players.csv')
df = df[0:500]  #sample 500 rows


# create a multi select
nationality_filter = st.sidebar.multiselect(
     'Choose the Nationality',
     df.country_of_citizenship.unique(),  # options
     df.country_of_citizenship.unique()
)  


value_filter = st.sidebar.radio(
     "Choose a value level",
     ('ALL','Low(<=40,000,000)','Medium(40,000,000<<80,000,000)','High(>=80,000,000)')
)

position_filter = st.sidebar.radio(
     "Choose a posotion",
     ('ALL','Attack','Midfield','Defender','Goalkeeper')
)

club_filter = st.sidebar.multiselect(
     'Choose the club',
     df.club_pretty_name.unique(),  # options
     df.club_pretty_name.unique()
)  

#filter by nationality
df = df[df.country_of_citizenship.isin(nationality_filter)]

#filter by value
if value_filter == 'Low(<=40,000,000)':
    df = df[df.market_value_in_gbp<=40000000]
         
if value_filter == 'Medium(40,000,000<<80,000,000)':   
    df = df[(df.market_value_in_gbp >40000000) & (df.market_value_in_gbp < 80000000 )]

if value_filter == 'High(>=80,000,000)':
    df = df[df.market_value_in_gbp>80000000]

if value_filter == 'All':
    df = df

#filter by position
if position_filter == 'ALL':
    df = df

if position_filter == 'Attack':   
    df = df[df.position=='Attack']

if position_filter == 'Midfield':
    df = df[df.position=='Midfield']

if position_filter == 'Defender':
    df = df[df.position=='Defender']

if position_filter == 'Goalkeeper':
    df = df[df.position=='Goalkeeper']

#filter by club
df = df[df.club_pretty_name.isin(club_filter)]


st.subheader('This is the Dataset of 500 top value soccer players in 2021:')
st.write(df)


# q1
st.subheader('Question 1: Are there any relations between the positions of the player and thier values? ')

df_att=df[df['position']=='Attack']
df_mid=df[df['position']=='Midfield']
df_def=df[df['position']=='Defender']
df_goal=df[df['position']=='Goalkeeper']

att_value=df_att['market_value_in_gbp'].mean()
mid_value=df_mid['market_value_in_gbp'].mean()
def_value=df_def['market_value_in_gbp'].mean()
goal_value=df_goal['market_value_in_gbp'].mean()

max=att_value
name='Attcker'
if mid_value>max:
    max=mid_value
    name='Midfielder'
if def_value>max:
    max=def_value
    name='Defender'
if goal_value>max:
    max=goal_value
    name='Goalkeeper'

fig, ax = plt.subplots()
x = ['Attcker','Midfielder','Defender','Goalkeeper']
y = [att_value,mid_value,def_value,goal_value]

plt.xlabel('Position')
plt.ylabel('average value')
plt.bar(x,y)
'Plot1:'
st.pyplot(fig)

'RESULT:'
st.text(f'Among the top 500 players, the average value of the Attacker is {att_value:.2f};')
st.text(f'the average value of the Midfielder is {mid_value:.2f};')
st.text(f'the average value of the Defender is {def_value:.2f};')
st.text(f'the average value of the Goalkeeper is {goal_value:.2f}.')
st.text(f'So among these four positions, {name}\'s value is the highest,which is {max:.2f}.')
'Concludsion:'
st.write('In different positions, there is a slight difference in the price of a player: the highest is the Attack, the lowest is goalkeeper.')
st.write('However,the result differs for specific different nationalities and clubs')


#q2
st.subheader('Question 2: If the preferred foot of soccer players have something to do with thier values? ')

fig2, ax = plt.subplots(1, 3,figsize=(15, 5))

df_right=df[df['foot']=='Right']

df_left=df[df['foot']=='Left']

df_both=df[df['foot']=='Both']

df_right.market_value_in_gbp.plot.box(ax=ax[0])  

df_left.market_value_in_gbp.plot.box(ax=ax[1]) 

df_both.market_value_in_gbp.plot.box(ax=ax[2]) 

ax[0].set_ylabel('Value')

ax[0].set_xlabel('Right foot')

ax[1].set_xlabel('Left foot')

ax[2].set_xlabel('Both foot')

'Plot2:'
st.pyplot(fig2)

'Conclusion:'
st.write('Between right foot and left foot,the outliers with right foot as thier preferred foot have higher value.')
st.write('But,except the outliers,the value of right foot players is relatively lower than that of left foot players.(BOTH foot players are not considered for too little data)')



st.subheader('Plot3:')

fig3, ax = plt.subplots()

df.market_value_in_gbp.plot()

st.pyplot(fig3)

'Analysis:'
'From this line chart,we can clearly see that there is a dramatical drop in value for the first few players.'
'That is because the values for Kylian Mbappe and Erling Haaland are outliers.Thier values reach about 140,000,000.After these two,the data of value levels off.'



st.subheader('Plot4:')

fig4, ax = plt.subplots(figsize=(10, 10))

df_nation=df[['country_of_citizenship', 'market_value_in_gbp']]

df_nation=df_nation.groupby('country_of_citizenship').mean()

df_nation=df_nation.sort_values(by='market_value_in_gbp', ascending=False)

plt.barh(df_nation.index,df_nation.market_value_in_gbp)

plt.xlabel('Average Value')
plt.ylabel('Nationality')

st.pyplot(fig4)

'Analysis:'
'From this bar chart,we can see the average value sorted by nationality.However,we can\'t conclude that Egypt players are better than Brazil players.'
'Because this data is influenced by number of players and outliers to a high degree.'

