import streamlit as st
import pandas as pd
import numpy as np

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
    st.dataframe(df)
except FileNotFoundError:
    st.error("CSV file not found. Check your GitHub repository structure.")

# Add an interactive widget
st.subheader("Try this slider:")
slider_value = st.slider("Select a number", 0, 100, 50)
st.write(f"You selected: {slider_value}")
# Add a button
if st.button("Click me!"):
    st.balloons()
    st.success("🎉 Congratulations! Your app is working!")
