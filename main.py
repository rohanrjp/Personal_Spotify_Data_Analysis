import pandas as pd
import streamlit as st
from data_processing import calculate_avg_session_duration, calculate_day_hour_heatmap, calculate_listening_streak, calculate_monthly_trends, calculate_top_10_songs, calculate_top_artists_by_month, calculate_weekday_trends, load_data,calculate_top_10_artists,calculate_hourly_listening,calculate_most_played_songs,calculate_weekly_top_tracks,calculate_hours_by_day_and_time
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.graph_objects as go

# Folder path where all JSON files are located
folder_path = 'https://raw.githubusercontent.com/rohanrjp/Personal_Spotify_Data_Analysis/refs/heads/main/data/merged_spotify_data.csv'

raw_data=load_data(folder_path)

st.title("Spotify Rewrapped")
st.subheader("Heres a preview")
st.write(raw_data.head())

monthly_trends = calculate_monthly_trends(raw_data)
weekday_trends = calculate_weekday_trends(raw_data)
avg_session_duration = calculate_avg_session_duration(raw_data)

st.header("Top 10 Artists")
st.write(calculate_top_10_artists(raw_data))
st.bar_chart(calculate_top_10_artists(raw_data))

top_songs = calculate_top_10_songs(raw_data)

st.header("Top 10 Most Played Songs")
st.bar_chart(calculate_top_10_songs(raw_data))


st.header("Listening Time by Day of Week")
st.bar_chart(weekday_trends)

st.metric("Average Session Duration (min)", avg_session_duration / 60)
st.header("Another visualization")
hourly_listening = calculate_hourly_listening(raw_data)

st.subheader("Listening Time by Hour of the Day")

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
hours = np.linspace(0, 2 * np.pi, 24, endpoint=False)
ax.bar(hours, hourly_listening, width=0.25, color='skyblue', edgecolor='black')
ax.set_theta_direction(-1)
ax.set_theta_offset(np.pi / 2.0)
ax.set_xticks(hours)
ax.set_xticklabels([f"{int(hr)}:00" for hr in hourly_listening.index])
ax.set_title("Average Listening Time by Hour (minutes)", va='bottom')

st.pyplot(fig)

top_songs = calculate_most_played_songs(raw_data)

st.header("Top 10 Most Played Songs")

fig, ax = plt.subplots()
ax.pie(top_songs["Total Hours Played"], labels=top_songs["Song"], autopct='%1.1f%%', startangle=90)
ax.set_title("Top 10 Most Played Songs (Total Hours Played)")
st.pyplot(fig) 

st.header("Weekly Popularity of Top 5 Tracks")
weekly_trends = calculate_weekly_top_tracks(raw_data)
fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(weekly_trends.T, cmap="Blues", ax=ax)
ax.set_xlabel("Week")
ax.set_ylabel("Track Name")
ax.set_title("Weekly Popularity of Top 5 Tracks")
st.pyplot(fig)

hours_by_day_and_time = calculate_hours_by_day_and_time(raw_data)


st.header("Hours Played by Day of Week and Time of Day")

fig, ax = plt.subplots(figsize=(14, 10))

colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]  

hours_by_day_and_time.plot(kind='bar', stacked=True, color=colors, ax=ax)

ax.set_xlabel("Day of the Week")
ax.set_ylabel("Hours Played")
ax.set_title("Listening Hours by Day of Week and Time of Day")

ax.legend(title="Time of Day", labels=hours_by_day_and_time.columns)

st.pyplot(fig)

monthly_artist_counts = calculate_top_artists_by_month(raw_data)

st.header("Top 15 Artists Played Over the Year")

fig, ax = plt.subplots(figsize=(14, 8))

for artist in monthly_artist_counts.columns:
    ax.plot(monthly_artist_counts.index, monthly_artist_counts[artist], label=artist)

ax.set_xlabel("Month")
ax.set_ylabel("Times Played")
ax.set_title("Monthly Plays of Top 15 Artists")
ax.legend(title="Artists", bbox_to_anchor=(1.05, 1), loc="upper left")

st.pyplot(fig)

st.header("Listening Time Heatmap by Day and Hour")

day_hour_data = calculate_day_hour_heatmap(raw_data)
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(day_hour_data, cmap="Blues", ax=ax, cbar_kws={'label': 'Total Listening Time (seconds)'})
ax.set_title("Listening Time Intensity by Day and Hour")
st.pyplot(fig)

st.header("Longest Listening Streak")
longest_streak = calculate_listening_streak(raw_data)
st.metric("Longest Streak (days)", longest_streak)

monthly_trends = calculate_monthly_trends(raw_data)

fig = go.Figure()
fig.add_trace(go.Scatter(x=monthly_trends['month'].astype(str), y=monthly_trends['seconds_played'], mode='lines+markers'))

if st.checkbox("Show Peak Annotations"):
    peak_month = monthly_trends['seconds_played'].idxmax()
    fig.add_annotation(x=monthly_trends.iloc[peak_month]['month'].strftime('%Y-%m'),
                       y=monthly_trends.iloc[peak_month]['seconds_played'],
                       text="Peak Listening Month",
                       showarrow=True,
                       arrowhead=2)

fig.update_layout(title="Monthly Listening Trends", xaxis_title="Month", yaxis_title="Total Listening Time (seconds)")
st.plotly_chart(fig)