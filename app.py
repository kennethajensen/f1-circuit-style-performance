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
    st.success("CSV file loaded successfully.")

try:
    df = load_data()
    # st.success("Data loaded successfully from GitHub!")
    # st.dataframe(df)
except FileNotFoundError:
    st.error("CSV file not found. Check your GitHub repository structure.")
    st.stop()  # Stop execution here

# 1. Get a unique list of teams from your CSV
cluster_list = sorted(df['Cluster Name'].unique())

# 2. Create the dropdown selector
selected_circuit_cluster = st.selectbox("Select a circuit style to analyze:", cluster_list)

# 3. Filter your data based on the selection
filtered_df = df[df['Cluster Name'] == selected_circuit_cluster]

st.subheader(f"Performance on {selected_circuit_cluster}")

# 1. Group by your category and calculate the mean
chart_data = filtered_df.groupby('Team Name')['Lap Time Difference (ms)'].mean().reset_index()

# 2. Define the Altair Chart
chart = alt.Chart(chart_data).mark_bar().encode(
    x='Lap Time Difference (ms)',
    y=alt.Y('Team Name', sort='x', title=None),
    # Conditional coloring logic:
    color=alt.condition(
        alt.datum['Lap Time Difference (ms)'] > 0,
        alt.value('#d33232'),  # Red for positive/slower
        alt.value('#3266d3')   # Blue for negative/faster
    ),
    tooltip=['Team Name', 'Lap Time Difference (ms)']
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

# Heatmap: Team Name vs Cluster Name
st.subheader("Heatmap: Mean Lap Time Difference by Team and Cluster")

# Group by Team Name and Cluster Name, calculate mean lap time difference
heatmap_data = df.groupby(['Team Name', 'Cluster Name'])['Lap Time Difference (ms)'].mean().reset_index()

# Get the number of unique clusters
num_clusters = heatmap_data['Cluster Name'].nunique()

# Create the heatmap with tickCount set to exact number of clusters
heatmap = alt.Chart(heatmap_data).mark_rect().encode(
    x=alt.X('Cluster Name:N', title=None, axis=alt.Axis(labelAngle=-45, labelPadding=10, labelLimit=500, tickCount=num_clusters, tickMinStep=1)),
    y=alt.Y('Team Name:N', title=None),
    color=alt.Color('Lap Time Difference (ms):Q', scale=alt.Scale(scheme='redblue'), legend=None),
    tooltip=['Team Name', 'Cluster Name', alt.Tooltip('Lap Time Difference (ms)', format='.2f')]
).properties(
    width=1600,
    height=600
)

st.altair_chart(heatmap, use_container_width=True)

# Optional: Display the heatmap data in a pivot table for clarity
if st.checkbox("Show heatmap data as pivot table"):
    try:
        pivot_data = heatmap_data.pivot_table(index='Team Name', columns='Cluster Name', values='Lap Time Difference (ms)', aggfunc='mean')
        st.dataframe(pivot_data)
    except Exception as e:
        st.error(f"Error creating pivot table: {e}")
