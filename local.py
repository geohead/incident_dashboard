'''
This is a streamlit dashboard app for my EoC app. Data comes from a django
backend through a View/ Read api.

'''


import streamlit as st
import pandas as pd 
from datetime import datetime
from dateutil import parser
import numpy as np
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go




# read csv file locally
myurl ="files/incidents.csv"

@st.cache
def get_data (url):
    return pd.read_csv(url)

df = get_data (url=myurl)

#session state defined if it doesn't exist

if "my_data"  not in st.session_state :
    st.session_state.my_data = ''




#Sidebar content

st.sidebar.subheader ("Filter the data by:")



oldest_date = parser.isoparse (df.incident_date_time.min())
latest_date =  parser.isoparse (df.incident_date_time.max())



oldest_date = oldest_date.date()
latest_date = latest_date.date()


st.sidebar.header("Filter data according to:")

end_date = st.sidebar.date_input ("End Date:", value = latest_date, min_value= oldest_date, max_value = latest_date)
#st.sidebar.write (end_date)

start_date = st.sidebar.date_input ("Start Date:", value = oldest_date, min_value= oldest_date, max_value = latest_date)
#st.sidebar.write (start_date)



if (start_date and end_date):
    if (start_date == oldest_date) & (end_date == latest_date):
        pass

    elif end_date > start_date:
        
        start_date = start_date.strftime("%Y-%m-%dT%H:%M:%S+03:00")
        end_date = end_date.strftime("%Y-%m-%dT%H:%M:%S+03:00")


        df = df.loc[(df['incident_date_time'] >= start_date) & (df['incident_date_time'] < end_date)]
        st.write(len(df))
    else:
        st.sidebar.write("Start date cannot be greater than end date!")  



st.sidebar.subheader ("Filter by Categories:")

options = np.append((df['region'].unique()),'All')
index = (len (options))-1

region_choice = st.sidebar.selectbox("Region", options , index)




if region_choice:

    st.session_state.my_data= region_choice

    if (st.session_state.my_data) =='All':
        df = df

    else:
        df = df[df['region']==(st.session_state.my_data)]
    


options = np.append((df['purpose'].unique()),'All')

index = (len (options))-1

purpose_choice = st.sidebar.selectbox("Purpose", options, index )


if purpose_choice:
    st.session_state.my_data = purpose_choice


    if (st.session_state.my_data) =='All':
        df = df

    else:
        df = df[df['purpose']==( st.session_state.my_data)]




options = np.append((df['intervention'].unique()),'All')

index = (len (options))-1

intervention_choice = st.sidebar.selectbox("Interventions", options, index )


if intervention_choice:
    st.session_state.my_data = intervention_choice


    if (st.session_state.my_data) =='All':
        df = df

    else:
        df = df[df['intervention']==( st.session_state.my_data)]






options = np.append((df['status'].unique()),'All')
index = (len (options))-1

status_choice = st.sidebar.selectbox("status", options, index)



if status_choice:

    st.session_state.my_data = status_choice


    if (st.session_state.my_data) =='All':
        df = df

    else:
        df = df[df['status']==(st.session_state.my_data)]



krcs_logo = Image.open ('resources/KRCS_Logo.png')
st.sidebar.image(krcs_logo, width=250)


# calculations that are needed.

tot_calls = len(df.index)

calls_region = df.region.value_counts().rename_axis("region").reset_index(name='Num of calls')

calls_county = df.county.value_counts().rename_axis("county").reset_index(name='Num of calls')

calls_purpose = df.purpose.value_counts().rename_axis("purpose").reset_index(name='Num of calls')

calls_gender =  df.caller_gender.value_counts().rename_axis("gender").reset_index(name='Num of calls')

purpose_gender = df.groupby(['purpose','caller_gender']).caller_gender.count()

purpose_gender = purpose_gender.to_frame('Num of calls').reset_index()

region_gender = df.groupby(['region','caller_gender']).caller_gender.count()

region_gender = region_gender.to_frame('Num of calls').reset_index()

status_dist = df.status.value_counts().rename_axis("status").reset_index(name='Num of calls')

calls_intervention = df.intervention.value_counts().rename_axis("interventions").reset_index(name='Num of calls')



# main content of the page

st.title ("Incident Reporter Dashboard")
st.write ("This dashboard visualizes incidents reported through the EOC call centre. Data comes from an API endpoint from the KRCS EOC Incident Reporter app.")
st.write("**Created by: [Boneya Hassan]( https://github.com/geohead/Incident-Report-Dashboard-with-Streamlit)**")


st.subheader("Snapshot of the dataset")
st.write (df.head(4))
 

st.subheader("Quick Stats")

col1, col2, col3, col4, col5  = st.columns (5)


col1.metric(label="Total calls to date:", value= tot_calls)
col2.metric(label="Calls today:", value= 0, delta="2 %", delta_color= 'normal')
col3.metric(label="Calls this month:", value= 00, delta='-8 %', delta_color= 'normal')
col4.metric(label="Calls this year:", value= 000, delta='17 %', delta_color= 'normal') 
col5.metric(label="Average age:",  value=00)




# plotly graphing fuctions defined here

def bar_graph (d, x, y,t,c=None,b=None):
    fig = px.bar (d ,x= x, y = y,text_auto='.3s',color= c, title = t, barmode = b, color_discrete_sequence= ['#ed1b2e'])
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(248, 248, 248, 1)',
        })
    fig.update_traces (textfont_size=12, textangle=0, textposition="inside", cliponaxis=False)
    fig.show()
    st.plotly_chart(fig)

def group_bar_graph (d, x, y,t,c=None,b=None):
    fig = px.bar (d ,x= x, y = y,text_auto='.3s',color= c, title = t, barmode = b)
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(248, 248, 248, 1)',
        })
    fig.update_traces (textfont_size=12, textangle=0, textposition="inside", cliponaxis=False)
    fig.show()
    st.plotly_chart(fig)



def pie_chart (d, v, n,t):
    fig = px.pie (d ,values= v, names = n, title = t)
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(248, 248, 248, 1)',
        })
    fig.update_traces ( textposition="inside")
    fig.show()
    st.plotly_chart(fig)




# graph visualizations

bar_graph (calls_region , x='region', y = 'Num of calls', t ="Calls per region")

bar_graph (calls_county, x='county', y = 'Num of calls', t ="Calls per county")

bar_graph (calls_purpose, x='purpose', y = 'Num of calls', t ="Calls by purpose")

pie_chart (calls_gender, v = 'Num of calls',n ='gender', t= "Calls by gender")

group_bar_graph (purpose_gender, x='purpose', y = 'Num of calls', t ="Distribution by purpose and gender", c='caller_gender',b='group')

group_bar_graph (region_gender, x='region', y = 'Num of calls', t ="Distribution by region and gender", c='caller_gender',b='group')

pie_chart (status_dist, v = 'Num of calls',n ='status', t= "Status of calls")

bar_graph (calls_intervention, x='interventions', y = 'Num of calls', t ="Interventions applied")

pie_chart (calls_intervention, v = 'Num of calls',n ='interventions', t= "Interventions applied")
