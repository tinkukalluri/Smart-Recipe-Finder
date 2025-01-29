import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Initialize Gemini API
genai.configure(api_key="AIzaSyB5r8XQy5pHg7GWBK3qhd6nuwV5epAqZ0k")
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit app
st.title("Fruit and Vegetable Recognition")

# Upload image
uploaded_file = st.file_uploader("Upload an image of fruits and vegetables", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Use Gemini model to analyze the image
    response = model.generate_content(
        contents=[
            "Identify all the fruits and vegetables in this image. Return only the names of the fruits and vegetables, separated by commas.",
            image
        ]
    )

    # Display the results
    st.subheader("Identified Fruits and Vegetables:")
    st.write(response.text)