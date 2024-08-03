import os
from dotenv import load_dotenv
from PIL import Image
import streamlit as st
import google.generativeai as genai
from typing_extensions import Final

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

def fetch_gemini_response(prompt, image_data, user_query):
    """Fetch response from Gemini model given a prompt, image data, and user query."""
    response = model.generate_content([prompt, image_data[0], user_query])
    return response.text

def process_uploaded_image(uploaded_file):
    """Process the uploaded image file and return its details."""
    if uploaded_file:
        image_bytes = uploaded_file.getvalue()
        image_info = [
            {
                "mime_type": uploaded_file.type,
                "data": image_bytes
            }
        ]
        return image_info
    else:
        raise FileNotFoundError("No file was uploaded.")

#streamlit set up
st.set_page_config(page_title="Multi-Language Invoice Reader")
st.header("Multi-Language Invoice Reader")

user_input = st.text_input("Input Prompt:", key="user_input")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

if st.button("submit"):
    predefined_prompt = """
    You are an expert in understanding invoices. We will upload an image as an invoice
    and you will have to answer any questions based on the uploaded invoice image.
    """
    try:
        image_details = process_uploaded_image(uploaded_file)
        gemini_response = fetch_gemini_response(predefined_prompt, image_details, user_input)
        st.subheader("The Response is")
        st.write(gemini_response)
    except FileNotFoundError as e:
        st.error(str(e))