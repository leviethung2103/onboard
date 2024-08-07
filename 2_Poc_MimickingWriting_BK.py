# %%
import streamlit as st
import requests
from bs4 import BeautifulSoup
import requests
import re
from collections import Counter
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
import platform
from langchain_community.document_transformers import Html2TextTransformer
from langchain_openai import ChatOpenAI
from pprint import pprint
from dotenv import load_dotenv
import os
import pandas as pd


os.system("playwright install")

load_dotenv(override=True)

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", api_key=os.getenv("OPENAPI_API_KEY", default=None))


# if platform.system() == "Windows":
#     loop = asyncio.ProactorEventLoop()
#     asyncio.set_event_loop(loop)
# else:
#     loop = asyncio.get_event_loop()
# bar = loop.run_until_complete(foo())


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
# website_url = st.text_input("What is your website URL?", value="https://www.wsj.com")
# website_url = st.text_input("What is your website URL?", value="https://vnexpress.net")
website_url = st.text_input("What is your website URL?", value="https://huyenchip.com/blog/")


# create the button analyze
analyze_button = st.button("Analyze")

print(website_url)

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

# Load HTML
# # Resolve async issues by applying nest_asyncio
import nest_asyncio

nest_asyncio.apply()
loader = AsyncChromiumLoader([website_url], headless=True, user_agent="MyAppUserAgent")
html = loader.load()

# bs_transformer = BeautifulSoupTransformer()
# docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["span"])

# # Result
# docs_transformed[0].page_content[0:500]
# print(docs_transformed[0].page_content)

# docs = loader.load()
# docs[0].page_content[0:100]


# from langchain_community.document_transformers import Html2TextTransformer

# html2text = Html2TextTransformer()
# docs_transformed = html2text.transform_documents(docs)
# docs_transformed[0].page_content[0:500]

# Transform
bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["a"])

from langchain.chains import create_extraction_chain

# schema = {
#     "properties": {
#         "news_article_title": {"type": "string"},
#         "news_article_summary": {"type": "string"},
#         "news_article_link": {"type": "string"},
#     },
#     "required": ["news_article_title", "news_article_summary", "news_article_link"],
# }
schema = {
    "properties": {
        "news_article_title": {"type": "string"},
        "news_article_link": {"type": "string"},
    },
    "required": ["news_article_summary", "news_article_link"],
}


def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).run(content)


def scrape_with_playwright(urls, schema):
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    #
    bs_transformer = BeautifulSoupTransformer()
    # docs_transformed = bs_transformer.transform_documents(docs, tags_to_extract=["span"])
    # extract the links from the website
    docs_transformed = bs_transformer.transform_documents(docs, tags_to_extract=["a"])
    print("Extracting content with LLM")

    # Grab the first 1000 tokens of the site
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000, chunk_overlap=0)
    splits = splitter.split_documents(docs_transformed)

    print(splits)

    # Process the first split
    extracted_content = extract(schema=schema, content=splits[0].page_content)
    pprint(extracted_content)
    return extracted_content


urls = [website_url]
extracted_content = scrape_with_playwright(urls, schema=schema)

# %%
# %%
import streamlit as st
import requests
from bs4 import BeautifulSoup
import requests
import re
from collections import Counter
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
import platform
from langchain_community.document_transformers import Html2TextTransformer
from langchain_openai import ChatOpenAI
from pprint import pprint
from dotenv import load_dotenv
import os

os.system("playwright install")

load_dotenv(override=True)

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", api_key=os.getenv("OPENAPI_API_KEY", default=None))


# if platform.system() == "Windows":
#     loop = asyncio.ProactorEventLoop()
#     asyncio.set_event_loop(loop)
# else:
#     loop = asyncio.get_event_loop()
# bar = loop.run_until_complete(foo())


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

    # website_url = st.text_input("What is your website URL?", value="https://www.wsj.com")
    # website_url = st.text_input("What is your website URL?", value="https://vnexpress.net")
    website_url = st.text_input("What is your website URL?", value="https://huyenchip.com/blog/")


# create the button analyze
analyze_button = st.button("Analyze")

print(website_url)

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

# Load HTML
# # Resolve async issues by applying nest_asyncio
import nest_asyncio

nest_asyncio.apply()
loader = AsyncChromiumLoader([website_url], headless=True, user_agent="MyAppUserAgent")
html = loader.load()

# bs_transformer = BeautifulSoupTransformer()
# docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["span"])

# # Result
# docs_transformed[0].page_content[0:500]
# print(docs_transformed[0].page_content)

# docs = loader.load()
# docs[0].page_content[0:100]


# from langchain_community.document_transformers import Html2TextTransformer

# html2text = Html2TextTransformer()
# docs_transformed = html2text.transform_documents(docs)
# docs_transformed[0].page_content[0:500]

# Transform
bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["a"])

from langchain.chains import create_extraction_chain

# schema = {
#     "properties": {
#         "news_article_title": {"type": "string"},
#         "news_article_summary": {"type": "string"},
#         "news_article_link": {"type": "string"},
#     },
#     "required": ["news_article_title", "news_article_summary", "news_article_link"],
# }
schema = {
    "properties": {
        "article_title": {"type": "string"},
        "article_link": {"type": "string"},
    },
    "required": ["article_title", "article_link"],
}


def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).run(content)


from langchain_core.pydantic_v1 import BaseModel, Field


class Blog(BaseModel):
    title: str = Field(description="The title of post")
    link: str = Field(
        description="The link of the post. If the link does not contains https, combine it with main link"
    )


structured_llm = llm.with_structured_output(schema=Blog)


def scrape_with_playwright(urls, schema):
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    #
    bs_transformer = BeautifulSoupTransformer()
    # docs_transformed = bs_transformer.transform_documents(docs, tags_to_extract=["span"])
    # extract the links from the website
    docs_transformed = bs_transformer.transform_documents(docs, tags_to_extract=["a"])
    print("Extracting content with LLM")

    # Grab the first 1000 tokens of the site
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000, chunk_overlap=0)
    splits = splitter.split_documents(docs_transformed)

    print(splits)

    # Process the first split
    extracted_content = extract(schema=schema, content=splits[0].page_content)
    pprint(extracted_content)
    return extracted_content


urls = [website_url]
extracted_content = scrape_with_playwright(urls, schema=schema)


# %%

# from langchain_community.document_loaders import FireCrawlLoader

# loader = FireCrawlLoader(api_key="fc-44f4486703c14fbca94aa4a7f5b31c2f", url="https://huyenchip.com/blog/", mode="crawl")

# docs = loader.load()


import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable, ALL


cost_table_headers = ["Site Name"] + [f"Beautiful Soup"]
content_table_headers = ["Site Name"] + [f"Beautiful Soup"]


content_table = PrettyTable()
content_table.field_names = content_table_headers

cost_table = PrettyTable()
cost_table.field_names = cost_table_headers


content_row = ["7taps"]

import requests


def scrape_jina_ai(url: str) -> str:
    response = requests.get("https://r.jina.ai/" + url)
    return response.text


def beautiful_soup_scrape_url(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return str(soup)


content = scrape_jina_ai("https://huyenchip.com/blog/")
# content = beautiful_soup_scrape_url("https://www.7taps.com/pricing")
content_snippet = content[:1000]

content_row.append(content_snippet)
content_table.add_row(content_row)

content_table.max_width = 100

print(content_table)

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_link(user_input: str):
    entity_extraction_system_message = {
        "role": "system",
        "content": "Get me all the links related to blog from this website's content, and return as a JSON with format: link:[{title: str, link: str]",
    }

    messages = [entity_extraction_system_message]
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o", messages=messages, stream=False, response_format={"type": "json_object"}
    )

    return response.choices[0].message.content


table = PrettyTable()
table.field_names = ["Site", "Provider Name", "Extracted Content"]
extracted_content = extract_link(content)
table.add_row(["7taps", "Jina AI", extracted_content])


def extract_content_from_url(url: str):
    blog_content = scrape_jina_ai(url)
    lines = blog_content.split("\n\n")

    title = None
    link = None
    published_date = None
    content = None

    for line in lines:
        if "title" in line.lower():
            title = line.split(":")[1].strip()
        if "url" in line.lower():
            link = line.split(":")[1].strip()
        if "published" in line.lower():
            published_date = line.split(":")[1].strip()
        if "markdown content" in line.lower():
            # content = line.split(":")[1].strip()
            content = "\n".join(lines[lines.index(line) + 1 :])

    return {"title": title, "link": link, "published_date": published_date, "content": content}


# blog_content = extract_content_from_url("https://huyenchip.com/2024/04/17/personal-growth.html")


# chỗ này nội dung hơi nhiều -> dùng tốn tiền

# %%
from linkedin_api import Linkedin
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv(override=True)


# Authenticate using any Linkedin account credentials
api = Linkedin(os.getenv("LINKEDIN_EMAIL"), os.getenv("LINKEDIN_PASSWORD"))

# GET a profile
# profile = api.get_profile('chiphuyen')


# GET a profiles contact info
# contact_info = api.get_profile_contact_info('chiphuyen')


posts = api.get_profile_posts("chiphuyen")
data = []
for post in posts:
    url = post["socialContent"]["shareUrl"]
    content = post["commentary"]["text"]["text"]
    data.append({"url": url, "content": content})

df = pd.DataFrame(data)
df.to_csv("post.csv", index=False)

# %%
