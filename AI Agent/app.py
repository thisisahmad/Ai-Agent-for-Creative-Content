import streamlit as st
from text_generator import generate_creative_content
from image_processor import generate_image_caption
from PIL import Image
import tempfile

# Streamlit app configuration
st.title("AI Agent for Creative Content")
st.write("Generate creative content and image captions with AI.")

# Input section for content generation
st.header("Generate Creative Text Content")
query = st.text_input("Enter a topic for content generation")

if st.button("Generate Content"):
    if query:
        # Generate creative text content
        content = generate_creative_content(query)
        st.subheader("Generated Content")
        st.write(content)
    else:
        st.warning("Please enter a topic.")

# Image caption generation section
st.header("Generate Image Caption")
uploaded_image = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

if st.button("Generate Caption"):
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Use a temporary file to save the uploaded image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image_file:
            temp_image_file.write(uploaded_image.getbuffer())
            temp_image_path = temp_image_file.name

        # Generate caption using the image
        caption = generate_image_caption(temp_image_path)
        st.subheader("Generated Caption")
        st.write(caption)
    else:
        st.warning("Please upload an image.")
