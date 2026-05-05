import streamlit as st
import pandas as pd
import numpy as np

# Set the page title
st.title("🎈 My First Streamlit App")
# Add a welcome message
st.write("Welcome to my app! This is running on Streamlit Cloud.")
# Create a simple dataframe
st.subheader("Here's a sample dataframe:")
df = pd.DataFrame({
    'Column A': [1, 2, 3, 4, 5],
    'Column B': ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry'],
    'Column C': np.random.randn(5)
})
st.dataframe(df)
# Add an interactive widget
st.subheader("Try this slider:")
slider_value = st.slider("Select a number", 0, 100, 50)
st.write(f"You selected: {slider_value}")
# Add a button
if st.button("Click me!"):
    st.balloons()
    st.success("🎉 Congratulations! Your app is working!")
