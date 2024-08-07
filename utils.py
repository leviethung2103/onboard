import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv(override=True)


def extract_blog_content_from_url(url: str) -> dict:
    """
    This function extracts the title, link, published date, and content of a blog post from a given URL.
    The blog content is scraped from the Jina AI website using the `scrape_jina_ai` function.
    The extracted information is returned as a dictionary with keys: 'title', 'link', 'published_date', and 'content'.

    Parameters:
    url (str): The URL path to be appended to the base URL "https://r.jina.ai/". This URL should not include the base URL.

    Returns:
    dict: A dictionary containing the extracted blog information with keys: 'title', 'link', 'published_date', and 'content'.
    """
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
            content = "\n".join(lines[lines.index(line) + 1 :])

    return {"title": title, "link": link, "published_date": published_date, "content": content}


def extract_links_from_blog(user_input: str) -> dict:
    """
    This function uses OpenAI's GPT-4 model to extract relevant links from a given user input.
    The user input is sent to the GPT-4 model, which is trained to understand the context and extract links related to blogs.
    The extracted links are returned as a JSON string with the format: {links:[{title: str, link: str}]}.

    Parameters:
    user_input (str): The input text from which to extract links. This could be a website's content, a blog post, etc.

    Returns:
    dict: A dictionary containing the extracted links with their respective titles.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    entity_extraction_system_message = {
        "role": "system",
        "content": "Get me all the links related to blog from this website's content, and return as a JSON with format:  {links:[{title: str, link: str}]}",
    }

    messages = [entity_extraction_system_message]
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o", messages=messages, stream=False, response_format={"type": "json_object"}
    )

    return response.choices[0].message.content, json.loads(response.choices[0].message.content).get("links")


def scrape_jina_ai(url: str) -> str:
    """
    This function sends a GET request to the specified URL on the Jina AI website and returns the response text.

    Parameters:
    url (str): The URL path to be appended to the base URL "https://r.jina.ai/". This URL should not include the base URL.

    Returns:
    str: The response text from the GET request.
    """
    response = requests.get("https://r.jina.ai/" + url)
    return response.text


def beautiful_soup_scrape_url(url: str):
    """
    This function sends a GET request to the specified URL and parses the response content using BeautifulSoup.
    It returns the parsed HTML content as a string.

    Parameters:
    url (str): The URL to be scraped.

    Returns:
    str: The parsed HTML content of the specified URL as a string.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return str(soup)


def get_netloc(url: str) -> str:
    """
    This function extracts the network location (netloc) from a given URL.
    The netloc is the network location part of the URL, which includes the domain name and any port number.

    Parameters:
    url (str): The URL from which to extract the netloc. This should be a string.

    Returns:
    str: The network location (netloc) extracted from the given URL.
    """
    from urllib.parse import urlparse

    parsed_url = urlparse(url)
    return parsed_url.netloc
