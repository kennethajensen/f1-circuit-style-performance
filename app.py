import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Set the page title
st.title("🎈 My First Streamlit App")
# Add a welcome message
st.write("Welcome to my app! This is running on Streamlit Cloud.")
# Create a simple dataframe
st.subheader("Here's a sample dataframe:")

# Use @st.cache_data to keep the app fast on the cloud
@st.cache_data
def load_data():
    # Because the CSV is in the same GitHub folder, 
    # we just use the filename.
    return pd.read_csv("f1_laptime_by_cluster.csv")

try:
    df = load_data()
    st.success("Data loaded successfully from GitHub!")
    # st.dataframe(df)
except FileNotFoundError:
    st.error("CSV file not found. Check your GitHub repository structure.")

st.title("Average Metrics by Group")

# 1. Group by your category and calculate the mean
chart_data = df.groupby('Cluster')['relative_lap_duration'].mean().reset_index()

# 2. Define the Altair Chart
chart = alt.Chart(chart_data).mark_bar().encode(
    x='relative_lap_duration',
    y=alt.Y('Cluster', sort='-x'),
    # Conditional coloring logic:
    color=alt.condition(
        alt.datum.relative_lap_duration < 0,
        alt.value('#d33232'),  # Red for negative
        alt.value('#3266d3')   # Blue for positive
    ),
    tooltip=['Cluster', 'relative_lap_duration']
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

# Add an interactive widget
st.subheader("Try this slider:")
slider_value = st.slider("Select a number", 0, 100, 50)
st.write(f"You selected: {slider_value}")
# Add a button
if st.button("Click me!"):
    st.balloons()
    st.success("🎉 Congratulations! Your app is working!")
