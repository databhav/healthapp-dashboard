import streamlit as st
import pandas as pd
import numpy as np
import re
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.header("Activity Dashboard 👣🎯")

st.divider()

df = pd.read_csv("/HealthApp_2k.log.csv")
df['Time'] = df['Time'].str[:-4]
df[['Date', 'Time']] = df['Time'].str.split('-', 1, expand=True)
df['Date'] = df['Date'].str.replace(r'(\d{4})(\d{2})(\d{2})', r'\3/\2/\1', regex=True)
#df['Time'] = pd.to_datetime(df['Time'])
#df

## Total altitude
#st.subheader('total altitude')
altitude_rows = df[df['Content'].str.contains("calculateAltitudeWithCache totalAltitude")]
altitude_rows['total_altitude'] = altitude_rows['Content']
altitude_rows['total_altitude'] = altitude_rows['total_altitude'].str.replace("calculateAltitudeWithCache totalAltitude=","")
altitude_rows['total_altitude'] = altitude_rows['total_altitude'].astype(int)
#altitude_rows

## Total cals
#st.subheader('totals cals')
cal_rows = df[df['Content'].str.contains("calculateCaloriesWithCache totalCalories")]
cal_rows['total_cals_with_cache'] = df['Content']
cal_rows['total_cals_with_cache'] = cal_rows['total_cals_with_cache'].str.replace("calculateCaloriesWithCache totalCalories=","")
cal_rows['total_cals_with_cache'] = cal_rows['total_cals_with_cache'].astype(int)
cal_rows['CalsToday'] = cal_rows['total_cals_with_cache']-126775
cal_rows['CalsToday'] = cal_rows['CalsToday'].replace(-126775,0)
#cal_rows

## Total steps
#st.subheader('total steps')
step_rows = df[df['Content'].str.contains("onStandStepChanged")]
step_rows['steps'] = step_rows['Content']
step_rows['steps'] = step_rows['steps'].str.replace("onStandStepChanged ","")
#step_rows


st.sidebar.header("Filters 🔍 ")
pid_selectbox =  st.sidebar.selectbox("Select Person ID:",df['Pid'].unique())
date_selectbox =  st.sidebar.selectbox("Select Date:",df['Date'].unique())
st.sidebar.subheader("")
st.sidebar.markdown("""
### Things to note 📝
1. Only person ID 30002312 data is available.
2. The data is available between time 10.15PM to 00.35AM.
3. Calories burned seems inaccurate in the data itself.
4. App isn't resetting the data at 00:00:00 time.
""")
st.sidebar.subheader("")
st.sidebar.subheader("About")
st.sidebar.markdown("The Dashboard shows four metrics and two interactive graphs. Step vs time graph hover represents **(time,steps)** and Calories vs Time hover represents **(time,calories burned)**.")
st.sidebar.write("SCROLL DOWN FOR CITATION")




cal_rows_filter = cal_rows[cal_rows['Date']==date_selectbox]
step_rows_filter = step_rows[step_rows['Date']==date_selectbox]

def plotting_steps(df):
  fig = go.Figure()

  # Add a line trace to the figure.
  fig.add_trace(go.Scatter(x=df["Time"], y=df["steps"], mode="lines",line_shape="spline"))

  # Set the title and axis labels for the figure.
  fig.update_layout(title="Steps vs. Time 👣", xaxis_title="Time", yaxis_title="Steps")

  # Display the Plotly figure in Streamlit.
  st.plotly_chart(fig,use_container_width=True)

def plotting_cals(df):
  fig = go.Figure()

  # Add a line trace to the figure.
  fig.add_trace(go.Scatter(x=df["Time"], y=df["CalsToday"], mode="lines"))

  # Set the title and axis labels for the figure.
  fig.update_layout(title="Calories vs. Time 🔥", xaxis_title="Time", yaxis_title="Steps")

  # Display the Plotly figure in Streamlit.
  st.plotly_chart(fig,use_container_width=True)

met1, met2, met3, met4 = st.columns(4)
met1.metric("Steps Today", max(step_rows['steps']))
met2.metric("Calories Burned", max(cal_rows['CalsToday']))
met3.metric("Calories Burned Till Date", max(cal_rows['total_cals_with_cache']))
met4.metric("Total Altitude Till Date", max(altitude_rows['total_altitude']))
st.divider()
with st.container():
  grf1, blk, grf2 = st.columns((10,1,10))
  with grf1:
    plotting_steps(step_rows_filter)
  with grf2:
    plotting_cals(cal_rows_filter)

st.subheader("Citation:")
st.markdown("""
Jieming Zhu, Shilin He, Pinjia He, Jinyang Liu, Michael R. Lyu. Loghub: A Large Collection of System Log Datasets for AI-driven Log Analytics. IEEE International Symposium on Software Reliability Engineering (ISSRE), 2023. [Online]. Available: https://github.com/logpai/loghub
""")
