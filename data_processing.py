import pandas as pd

def load_data(folder_path:str):
    raw_data=pd.read_csv(folder_path)
    raw_data["endTime"]=pd.to_datetime(raw_data["endTime"])
    raw_data['year'] = raw_data['endTime'].dt.year
    raw_data['month'] = raw_data['endTime'].dt.month
    raw_data['date'] = raw_data['endTime'].dt.day
    raw_data['hour'] = raw_data['endTime'].dt.hour
    raw_data['day_of_week'] = raw_data['endTime'].dt.day_name()
    raw_data["seconds_played"]=raw_data["msPlayed"]/1000
    raw_data["min_played"]=raw_data["seconds_played"]/60
    raw_data["hours_played"]=raw_data["min_played"]/60
    return raw_data

def calculate_top_10_artists(data):
    data = data["artistName"].value_counts().head(10).reset_index()
    data.columns = ['Artist', 'Number of times played']
    return data

def calculate_hourly_listening(data):
    data['hour'] = data['endTime'].dt.hour
    hourly_data = data.groupby('hour')['seconds_played'].sum() / 3600  
    return hourly_data

def calculate_monthly_trends(data):
    monthly_data = data.groupby(data['endTime'].dt.to_period("M"))['hours_played'].sum()
    return monthly_data

def calculate_weekday_trends(data):
    weekday_data = data.groupby('day_of_week')['seconds_played'].sum().sort_index() / 3600  
    return weekday_data

def calculate_avg_session_duration(data):
    return data['seconds_played'].mean() 

def calculate_most_played_songs(data, top_n=10):
    most_played_songs = (
        data.groupby("trackName")["seconds_played"].sum().sort_values(ascending=False) / 3600
    )
    most_played_songs = most_played_songs.head(top_n).reset_index()
    most_played_songs.columns = ["Song", "Total Hours Played"]  
    return most_played_songs

def calculate_weekly_top_tracks(data, top_n=5):
    top_tracks = data['trackName'].value_counts().head(top_n).index
    track_data = data[data['trackName'].isin(top_tracks)]
    
    weekly_trends = track_data.groupby([pd.Grouper(key='endTime', freq='W'), 'trackName'])['seconds_played'].sum().unstack()
    return weekly_trends

def calculate_hours_by_day_and_time(data):
    bins = [0, 6, 12, 18, 24]
    labels = ["Night", "Morning", "Afternoon", "Evening"]

    data['hours_played'] = data['seconds_played'] / 3600

    data['day_of_week'] = data['endTime'].dt.day_name()
    data['hour'] = data['endTime'].dt.hour

    data['time_of_day'] = pd.cut(data['hour'], bins=bins, labels=labels, right=False)

    hours_by_day_and_time = data.groupby(['day_of_week', 'time_of_day'])['hours_played'].sum().unstack().reindex(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )
    return hours_by_day_and_time

def calculate_top_artists_by_month(data, top_n=10):
    data['endTime'] = pd.to_datetime(data['endTime'])

    top_artists = data['artistName'].value_counts().head(top_n).index

    filtered_data = data[data['artistName'].isin(top_artists)]

    filtered_data['month'] = filtered_data['endTime'].dt.month_name()

    monthly_artist_counts = (
        filtered_data.groupby(['month', 'artistName']).size().unstack(fill_value=0)
    )

    month_order = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    monthly_artist_counts = monthly_artist_counts.reindex(month_order)

    return monthly_artist_counts

def calculate_top_10_songs(data):
    top_songs = data['trackName'].value_counts().head(10)
    
    top_songs.index.name = 'Song'
    top_songs.name = 'Play Count'
    
    return top_songs


def calculate_day_hour_heatmap(data):
    data['day_of_week'] = data['endTime'].dt.day_name()
    data['hour'] = data['endTime'].dt.hour

    day_hour_data = data.groupby(['day_of_week', 'hour'])['seconds_played'].sum().unstack().fillna(0)

    return day_hour_data

def calculate_listening_streak(data):
    listening_days = data['endTime'].dt.date.unique()
    streaks = []
    current_streak = 1
    
    for i in range(1, len(listening_days)):
        if (listening_days[i] - listening_days[i - 1]).days == 1:
            current_streak += 1
        else:
            streaks.append(current_streak)
            current_streak = 1
    streaks.append(current_streak)
    
    longest_streak = max(streaks)
    return longest_streak

def calculate_monthly_trends(data):
    data['month'] = data['endTime'].dt.to_period("M")
    monthly_trends = data.groupby(data['month'])['seconds_played'].sum().reset_index()
    return monthly_trends