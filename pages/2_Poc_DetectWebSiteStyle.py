import streamlit as st
import requests
from bs4 import BeautifulSoup
from io import BytesIO
import requests
import re
from collections import Counter

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("## Welcome to the Website Style Analyzer!")

st.write(
    "This tool helps you analyze the style of your website.\n\nPlease update the link on the sidebar to analyze your website.\n\nFinally, press the 'Analyze' button to get the analysis result."
)

st.write("### Input")
with st.sidebar:
    website_url = st.text_input("What is your website URL?")
    writing_pages = st.text_input("Which web pages best demonstrate your writing style?")

# create the button analyze
analyze_button = st.button("Analyze")

# file_path = "website.html"

# loader = UnstructuredHTMLLoader(file_path)
# data = loader.load()

# print(data)

if analyze_button:
    # analyze the website and writing style
    # add your code here to analyze the website and writing style
    # for example, use a web scraping library to extract data
    # and a machine learning model to classify the writing style

    # display the results
    st.write("### Analysis result")

    # Step 1: Visit the website URL
    try:
        response = requests.get(website_url, timeout=5)
        if response.status_code != 200:
            st.warning("Website is not accessible.", icon="⚠️")
        else:
            soup = BeautifulSoup(response.text, "html.parser")

            # Find all style tags
            style_tags = soup.find_all("style")

            # Find background color in CSS styles
            for tag in style_tags:
                css_styles = tag.string
                if css_styles:
                    matches = re.findall(r"background-color:\s*(.*?);", css_styles)
                    if matches:
                        color_freq = Counter(matches)
                        primary_bg_color, _ = color_freq.most_common(1)[0]
                        # Remove the primary word from the frequency dictionary
                        del color_freq[primary_bg_color]
                        # Get the second most common word (secondary word)
                        secondary_bg_color, _ = color_freq.most_common(1)[0]
                        st.write(st.color_picker(f"Primary Background Color ", primary_bg_color))
                        st.write(st.color_picker(f"Secondary Background Color ", secondary_bg_color))

            # save the website's to html file
            with open("website.html", "w") as file:
                file.write(soup.prettify())

            # Extract the title of the website
            website_title = soup.title.string
            st.write(f"Website title: {website_title}")

            def get_css_links(html_file):
                with open(html_file) as f:
                    soup = BeautifulSoup(f, "html.parser")

                css_links = []
                for link in soup.find_all("link"):
                    if link.get("href") and ".css" in link.get("href"):
                        css_links.append(link.get("href"))

                return css_links

            html_file = "website.html"  # Update this with the path to your HTML file
            css_links = get_css_links(html_file)
            # st.write(css_links)

            import re

            # pattern = r'font-family:\s*"([^"]*)"'
            # pattern = r'font-family:\s*["\']?([^"\';]*)["\']?'
            pattern = r"font-family:(.*?);"

            # read the website.html file
            with open(html_file, "r") as f:
                css_block = f.read()
            font_families = re.findall(pattern, css_block)
            # st.write(font_families)

            # pattern = r"background-color:(#(?:[0-9a-fA-F]{3}){1,2})"

            # bg_color = re.findall(pattern, css_block)

            # st.write(bg_color)

            # for idx, color in enumerate(bg_color):
            #     st.write(st.color_picker(f"Color {idx}", color))

            def find_primary_and_secondary_fonts(words_list):
                """Pick primary font and secondary font from website"""
                # Count the frequency of each word in the list
                word_freq = Counter(words_list)

                print(word_freq)

                # Get the most common word (primary word)
                primary_word, _ = word_freq.most_common(1)[0]
                # Remove the primary word from the frequency dictionary
                del word_freq[primary_word]
                # Get the second most common word (secondary word)
                secondary_word, _ = word_freq.most_common(1)[0]
                return primary_word, secondary_word

            primary_font, secondary_font = find_primary_and_secondary_fonts(font_families)
            st.write("Primary font: ", primary_font)
            st.write("Secondary font: ", secondary_font)

            # if len(css_links) > 0:
            #     st.write("Website has CSS styles.")
            #     for idx, css_link in enumerate(css_links):
            #         response = requests.get(css_link)
            #         css_code = response.text
            #         # Split the CSS code snippet into individual CSS rules
            #         css_rules = [rule.strip() for rule in css_code.split("}") if rule.strip()]
            #         # st.write(idx, css_rules)

            #         # find the font-family
            #         for css_rule in css_rules:
            #             if "font-family" in css_rule:
            #                 st.write(css_rule)

            # else:

            #     # Step 2: Understand the website's content and structure (design aspects)

            #     # Step 3: Extracting background color
            #     background_image_url = soup.find("body")["style"].split("(")[1].split(")")[0]
            #     image_response = requests.get(background_image_url)

            #     color_thief = ColorThief(BytesIO(image_response.content))
            #     background_color = color_thief.get_palette(color_count=1)[0]
            #     print(f"Background Color: {background_color}")

            #     # Step 3: DIsplay the results
            #     print(f"Writing Style Pages: {writing_pages}")
            #     print(f"Background Color: {background_color}")

            #     # Add similar print statements for other design elements like fonts, colors, etc.

            #     # Step 4: Extract the fonts

            #     # Extracting fonts
            #     font_stylesheets = [link.get("href") for link in soup.find_all("link") if "font" in link.get("href")]
            #     print("Font Stylesheets:")
            #     for stylesheet in font_stylesheets:
            #         print(stylesheet)

            #     # Extract colors

            #     # Extracting primary and secondary colors
            #     image_links = [img["src"] for img in soup.find_all("img")]
            #     colors = []
            #     for link in image_links:
            #         image_response = requests.get(link)
            #         color_thief = ColorThief(BytesIO(image_response.content))
            #         colors.extend(color_thief.get_palette(color_count=3))  # Adjust the color_count as needed
            #     primary_color = max(set(colors), key=colors.count)
            #     colors.remove(primary_color)
            #     secondary_color = max(set(colors), key=colors.count)
            #     print(f"Primary Color: {primary_color}")
            #     print(f"Secondary Color: {secondary_color}")

            #     # Extracting link color
            #     link_color = soup.find("a")["style"].split(":")[1].split(";")[0]
            #     print(f"Link Color: {link_color}")
    except requests.exceptions.RequestException as e:
        st.warning(f"Error accessing website: {e}", icon="⚠️")
