import streamlit as st
import requests
import requests
from utils import ExtractStyle
from constants import OUTPUT_DIR

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("## Welcome to the Website Analyzer!")

st.write(
    "This tool helps you analyze the style of your website.\n\nPlease update the link on the sidebar to analyze your website.\n\nFinally, press the 'Analyze' button to get the analysis result."
)

st.write("### Input")
website_url = st.text_input("What is your website URL?", value="https://24h.com.vn/")

# create the button analyze
analyze_button = st.button("Analyze")

if analyze_button:
    st.write("### Analysis result")

    if len(website_url) <= 0 or not website_url.startswith("http"):
        st.warning("Please enter a valid website URL.", icon="⚠️")
        st.stop()

    st.write("**Analyzing website style...**")

    response = requests.get(website_url, timeout=5)
    if response.status_code != 200:
        st.warning("Website is not accessible.", icon="⚠️")
        st.stop()
    else:
        output_image = f"{OUTPUT_DIR}/snapshot.png"
        extractor = ExtractStyle(url=website_url, output_path=output_image)
        result = extractor.pipe()

        st.success("Analyzed website successfully!")

        st.write(result)

        st.image(image=output_image, caption="Snapshot of the website")

        st.write("**Font**")
        st.write(f"- Primary Font: {result['primary_font']}")
        st.write(f"- Secondary Font: {result['secondary_font']}")

        st.write("**Hexa Colors**")
        st.write(f"- Background color: {result['background_color']}")
        st.write(f"- Main color: {result['main_color']}")
        st.write(f"- Secondary color:{result['secondary_color']}")

        st.write("**Human Colors**")
        st.color_picker(f"Background color", result["background_color"])
        st.color_picker(f"Main color", result["main_color"])
        st.color_picker(f"Secondary color", result["secondary_color"])
