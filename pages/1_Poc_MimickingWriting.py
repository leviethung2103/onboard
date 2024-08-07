import requests
import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
from linkedin_api import Linkedin

# sys.path.append("/Users/hunglv/Downloads/flodesk-onboard")
from utils import scrape_jina_ai, extract_links_from_blog, extract_blog_content_from_url, get_netloc

load_dotenv(override=True)

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("## Welcome to the Writing Style Analyzer!")

st.write(
    "This tool helps you analyze the writing style of your website.\n\nPlease update the link on the sidebar to analyze.\n\nFinally, press the 'Analyze' button to get the analysis result."
)

st.write("### Input")
website_url = st.text_input("What is your website URL?", value="https://huyenchip.com/blog/", key="url")
number_of_posts = st.number_input("How many posts to analyze?", value=2, key="number_of_posts")
linkedin = st.text_input(
    "What is your linkedin account url or account name?", value="https://www.linkedin.com/in/chiphuyen/", key="linkedin"
)

analyze_button = st.button("Analyze")

if analyze_button:
    st.write("### Analysis result")

    if len(website_url) <= 0:
        st.warning("Please enter a valid website URL.", icon="⚠️")
        st.stop()

    if linkedin.startswith("https://www.linkedin.com/in/"):
        account_name = linkedin.split("/in/")[-1].replace("/", "")
    else:
        account_name = linkedin

    st.write("**Processing website url...**")
    response = requests.get(website_url, timeout=10)
    if response.status_code != 200:
        st.warning("Website is not accessible.", icon="⚠️")
    else:
        # Step 1: get content of blog
        content = scrape_jina_ai(website_url)

        print(content[:500])

        # Step 2: extract links from blog
        raw_links, links = extract_links_from_blog(content)

        data = []

        # Step 3: extract content from each link
        for link in links[0:number_of_posts]:
            blog_content = extract_blog_content_from_url(link.get("link"))
            data.append(blog_content)

        # Step 4: Save extracted content to CSV file
        df = pd.DataFrame(data)

        website_name = get_netloc(website_url)
        df.to_csv(f"{website_name}.csv", index=False)

        st.success("Scraped website content successfully!")

        st.dataframe(df)

    st.write("**Processing linkedin account...**")
    api = Linkedin(os.getenv("LINKEDIN_EMAIL"), os.getenv("LINKEDIN_PASSWORD"))

    print(account_name)

    posts = api.get_profile_posts(account_name)
    data = []
    for post in posts:
        url = post["socialContent"]["shareUrl"]
        content = post["commentary"]["text"]["text"]
        data.append({"url": url, "content": content})

    df_linkedin = pd.DataFrame(data)
    df_linkedin.to_csv(f"{account_name}_posts.csv", index=False)

    st.success("Scraped website content successfully!")

    st.dataframe(df_linkedin)
