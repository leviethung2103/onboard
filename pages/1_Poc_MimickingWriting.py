import streamlit as st
import requests
from bs4 import BeautifulSoup
from colorthief import ColorThief
from io import BytesIO
import requests
from langchain_community.document_loaders import UnstructuredHTMLLoader
import re
from collections import Counter
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
import pprint

from langchain_text_splitters import RecursiveCharacterTextSplitter

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("## Welcome to the Writing Style Analyzer!")

st.write(
    "This tool helps you analyze the writing style of your website.\n\nPlease update the link on the sidebar to analyze.\n\nFinally, press the 'Analyze' button to get the analysis result."
)


st.write("### Input")
with st.sidebar:
    website_url = st.text_input("What is your website URL?", value="https://huyenchip.com/blog/")


# create the button analyze
analyze_button = st.button("Analyze")


def scrape_with_playwright(urls, schema):
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(docs, tags_to_extract=["span"])
    print("Extracting content with LLM")

    # Grab the first 1000 tokens of the site
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000, chunk_overlap=0)
    splits = splitter.split_documents(docs_transformed)

    # Process the first split
    extracted_content = extract(schema=schema, content=splits[0].page_content)
    pprint.pprint(extracted_content)
    return extracted_content


# urls = ["https://www.wsj.com"]
# extracted_content = scrape_with_playwright(urls, schema=schema)


if analyze_button:
    # analyze the website and writing style
    # add your code here to analyze the website and writing style
    # for example, use a web scraping library to extract data
    # and a machine learning model to classify the writing style

    # display the results
    st.write("### Analysis result")

    if len(website_url) <= 0:
        st.warning("Please enter a valid website URL.", icon="⚠️")

    try:
        response = requests.get(website_url, timeout=5)
        if response.status_code != 200:
            st.warning("Website is not accessible.", icon="⚠️")
        else:
            soup = BeautifulSoup(response.text, "html.parser")

            # Load HTML
            loader = AsyncChromiumLoader([website_url])
            html = loader.load()

            bs_transformer = BeautifulSoupTransformer()
            docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["span"])

            # Result
            docs_transformed[0].page_content[0:500]
            print(docs_transformed[0].page_content)
    except Exception as error:
        print("error", error)
