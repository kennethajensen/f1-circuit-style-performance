# https://my-first-app-app-vernumh2n2kpyeyhwgvkxg.streamlit.app/

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Set the page title
st.title("🏎️ Analyzing Formula 1 Data")
# Add a welcome message
st.write("Showing the relative performance difference on each group of circuit styles.")

# Use @st.cache_data to keep the app fast on the cloud
@st.cache_data
def load_data():
    # Because the CSV is in the same GitHub folder, 
    # we just use the filename.
    return pd.read_csv("f1_laptime_by_cluster.csv")

try:
    df = load_data()
    # st.success("Data loaded successfully from GitHub!")
    # st.dataframe(df)
except FileNotFoundError:
    st.error("CSV file not found. Check your GitHub repository structure.")


# 1. Get a unique list of teams from your CSV
# Replace 'Team_Column' with your actual column name
team_list = sorted(df['Cluster'].unique())

# 2. Create the dropdown selector
selected_team = st.selectbox("Select a circuit style to analyze:", team_list)

# 3. Filter your data based on the selection
filtered_df = df[df['Cluster'] == selected_team]

st.subheader(f"Performance for {selected_team}")

# 1. Group by your category and calculate the mean
chart_data = filtered_df.groupby('team_name')['relative_lap_duration'].mean().reset_index()

# 2. Define the Altair Chart
chart = alt.Chart(chart_data).mark_bar().encode(
    x='relative_lap_duration',
    y=alt.Y('team_name', sort='x', title=None),
    # Conditional coloring logic:
    color=alt.condition(
        alt.datum.relative_lap_duration > 0,
        alt.value('#d33232'),  # Red for positive/slower
        alt.value('#3266d3')   # Blue for negative/faster
    ),
    tooltip=['team_name', 'relative_lap_duration']
).configure_axis(
    labelLimit=300  # Ensure full category names are shown
).properties(
    height=400
)

# 3. Display the chart
st.altair_chart(chart, use_container_width=True)

# Optional: Display the raw averages in a table for clarity
if st.checkbox("Show raw average numbers"):
    st.table(chart_data)
