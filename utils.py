import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

from selenium import webdriver
import base64
import re
from constants import ANALYZING_PROMPT_TEMPLATE

load_dotenv(override=True)


def extract_style_from_website(user_input: str) -> dict:
    """
    This function uses OpenAI's GPT-4 model to extract primary font, secondary font, background color, primary color,
    secondary color, and link color from a given website's content. The function sends a user input to the GPT-4 model,
    which is trained to understand the context and extract the required information. The extracted information is returned
    as a JSON with the specified format.

    Parameters:
    user_input (str): The website's content from which to extract the colors. This should be a string.

    Returns:
    dict: A dictionary containing the extracted colors with keys: 'primary_font', 'secondary_font', 'background_color',
          'primary_color', 'secondary_color', and 'link_color'.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    entity_extraction_system_message = {
        "role": "system",
        "content": "Extract the primary font, secondary font, background color, primary color, secondary color and link color from this website's content, and return as a JSON with format:  {primary_font: str, secondary_font: str, background_color: str, primary_color: str, secondary_color: str, link_color: str}",
    }

    messages = [entity_extraction_system_message]
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o", messages=messages, stream=False, response_format={"type": "json_object"}
    )
    print(response.choices[0].message.content)
    return json.loads(response.choices[0].message.content)


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


def scrape_firecrawl(url: str):
    import firecrawl

    app = firecrawl.FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))
    scraped_data = app.scrape_url(url)["markdown"]
    return scraped_data


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


def read_file(file_path):
    """
    This function reads the content of a file located at the specified file path.

    Parameters:
    file_path (str): The path to the file to be read. This should be a string.

    Returns:
    str: The content of the file as a string.
    """
    with open(file_path, "r") as file:
        content = file.read()
    return content


def remove_links(text):
    """
    This function removes all URLs and web addresses (www.example.com) from a given text.
    It uses a regular expression pattern to match URLs and replaces them with an empty string.

    Parameters:
    text (str): The input text from which to remove URLs. This should be a string.

    Returns:
    str: The input text with all URLs and web addresses removed.
    """
    # Define the regex pattern to match URLs
    pattern = r"http[s]?://\S+|www\.\S+"

    # Use the sub() function to replace the links with an empty string
    cleaned_text = re.sub(pattern, "", text)

    return cleaned_text


class ExtractStyle:
    def __init__(self, url: str, output_path: str = "snapshot.png") -> None:
        self.url = url
        self.output_path = output_path

    def pipe(self):
        """
        This function orchestrates the entire process of capturing a screenshot of a website,
        encoding the screenshot into a base64-encoded string, and extracting the website's style
        (background color, primary font, secondary font, main color, secondary color, and link color)
        using OpenAI's GPT-4 model.

        Parameters:
        None

        Returns:
        dict: A dictionary containing the extracted style information with keys:
            'background_color', 'primary_font', 'secondary_font', 'main_color', 'secondary_color', and 'link_color'.
        """
        self.snapshot(self.url, self.output_path)
        encoded_image = self.encode_image(self.output_path)
        result = self.extract_style_by_vision(encoded_image)
        return result

    @staticmethod
    def encode_image(image_path: str) -> str:
        """
        This function encodes a screenshot image into a base64-encoded string.

        Parameters:
        image_path (str): The file path of the screenshot image to be encoded. This should be a string.

        Returns:
        str: The base64-encoded string representation of the screenshot image.
        """
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read())
            return encoded_image.decode("utf-8")

    @staticmethod
    def extract_style_by_vision(base64_image) -> dict:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Here is the screenshot of website. Extract the background color, primary font, secondary font, main color, secondary color and link color in the website. Response to user will be only JSON, no markdown, in the value for a JSON key response",
                        },
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                }
            ],
            max_tokens=300,
        )

        print(response.choices[0])

        content = response.choices[0].message.content

        print(content)
        return json.loads(content).get("response")

    @staticmethod
    def snapshot(url: str, output_path: str = "snapshot.png") -> None:
        """
        This function uses the Selenium WebDriver to capture a screenshot of a given website.
        It opens a Chrome browser, navigates to the specified URL, takes a screenshot, and then quits the browser.

        Parameters:
        url (str): The URL of the website to capture a screenshot of. This should be a string.

        Returns:
        None: This function does not return any value. It saves the screenshot as a file with the same name as the URL.
        """
        driver = webdriver.Chrome()

        driver.get(url)

        driver.save_screenshot(output_path)

        driver.quit()

        print("Captured screenshot")


def retrieve_style(content):
    """
    This function sends a user input to OpenAI's GPT-4o-mini model to analyze the style of the input content.
    The model is trained to understand the context and extract the style information.

    Parameters:
    content (str): The input text content for which to analyze the style. This should be a string.

    Returns:
    str: The response from the GPT-4o-mini model, which contains the analyzed style information.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": ANALYZING_PROMPT_TEMPLATE},
            {"role": "user", "content": content},
        ],
        stream=False,
    )
    return response.choices[0].message.content


def mimicking_style(input_sample, reference_style):
    """
    This function uses OpenAI's GPT-4o-mini model to re-write a given input sample text
    by imitating a specified writing style. The model is trained to understand the context
    and generate text that mimics the given style.

    Parameters:
    input_sample (str): The original text content that needs to be re-written. This should be a string.
    reference_style (str): A description of the writing style to be imitated. This should be a string.

    Returns:
    str: The re-written text that mimics the specified writing style.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"You are a helpful chatbot.",
            },
            {
                "role": "user",
                "content": f"Please re-write content of this email by imitating my writing style. My writing style is described as following: {reference_style}.\n\n{input_sample}",
            },
        ],
        stream=False,
    )

    return response.choices[0].message.content
