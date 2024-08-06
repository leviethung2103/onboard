import streamlit as st
import requests
from bs4 import BeautifulSoup
from colorthief import ColorThief
from io import BytesIO
import requests
from langchain_community.document_loaders import UnstructuredHTMLLoader
import re
from collections import Counter

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("## Welcome to the Writing Style Analyzer!")

st.write(
    "This tool helps you analyze the writing style of your website.\n\nPlease update the link on the sidebar to analyze your website.\n\nFinally, press the 'Analyze' button to get the analysis result."
)
