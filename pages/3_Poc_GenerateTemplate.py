import streamlit as st
import requests
from bs4 import BeautifulSoup
from io import BytesIO
import requests
from langchain_community.document_loaders import UnstructuredHTMLLoader
import re
from collections import Counter

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("## Welcome to Generate Template!")

st.write("This tool helps you generate the template of website.\n\n")
