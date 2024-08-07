from dotenv import load_dotenv
import pandas as pd
import streamlit as st
from utils import read_file, remove_links, retrieve_style, mimicking_style
import pandas as pd

load_dotenv(override=True)

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("## Welcome to the Writing Style Analyzer!")

st.write(
    "This tool helps you analyze the writing style of your website.\n\nPlease update the link below to analyze.\n\nFinally, press the 'Analyze' button to get the analysis result."
)


reference_content = pd.read_csv("data/chiphuyen/huyenchip.com.csv")["content"].iloc[0]
sample_content = read_file("sample_welcome_message.txt")

c1, c2 = st.columns(2)
with c1:
    sample_text = st.text_area("Sample text", value=sample_content, key="sample_text", height=500)

with c2:
    reference_text = st.text_area("Reference text", value=reference_content, key="reference_text", height=500)

# * Preprocessing reference content
cleaned_reference_content = remove_links(reference_text)

analyze_button = st.button("Analyze")

if analyze_button:
    with st.spinner("Analyzing style..."):
        writing_style = retrieve_style(cleaned_reference_content)
        writing_style = writing_style.replace("###", "####")
    st.write(f"### Analyzed style")
    st.write(f"{writing_style}")
    with st.spinner("Mimicking style..."):
        new_email = mimicking_style(input_sample=sample_text, reference_style=writing_style)
    st.write(f"### Final result...")
    st.text_area("Final result", value=new_email, key="new_email", height=500)
