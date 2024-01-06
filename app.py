import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

st.title('Image Captioning and Tagging')

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
API_KEY = st.text_input("Enter your API Key", type="password")
if uploaded_file is not None:
    if st.button('Upload'):
        if API_KEY.strip() == '':
            st.error('Enter a valid API key')
        else:
            file_path = os.path.join("static", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            img = Image.open(file_path)
            genai.configure(api_key=API_KEY)
            resized_img = img.resize((600, 420))
            resized_path = os.path.join("static", f"resized/resized_{uploaded_file.name}")
            resized_img.save(resized_path)

            # Caption generation
            model = genai.GenerativeModel('gemini-pro-vision')
            caption = model.generate_content(["Write a caption for the image in english",img])
            tags=model.generate_content(["Generate 5 hash tags for the image in a line in english",img])
            st.image(img, caption=f"Caption: {caption.text}")
            st.write(f"Tags: {tags.text}")
