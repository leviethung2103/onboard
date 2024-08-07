import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Streamlit! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.\n
    👈 Select a demo **Website Website** from the sidebar to play with Challenge #1\n
    👈 Select a demo **Mimicking Writing** from the sidebar to play with Challenge #2 
"""
)
