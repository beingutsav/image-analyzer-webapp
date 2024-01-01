import streamlit as st
import requests
from io import BytesIO
from PIL import Image

# Streamlit UI
st.title("Fashion Designer Image Analyst")

prompt = st.text_area("Enter prompt:", "Consider yourself as a top-level fashion designer image analyst...")

uploaded_files = st.file_uploader("Upload images", type=["jpg", "jpeg"], accept_multiple_files=True)

if st.button("Submit"):
    if uploaded_files:
        image_paths = []
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Uploaded Image", use_column_width=True)
            image_path = f"temp_{uploaded_file.name}"
            image.save(image_path)
            image_paths.append(image_path)

        # Backend API request
        api_url = "http://127.0.0.1:8000/process-images/"
        files = [("image_files", (open(file, "rb"))) for file in image_paths]
        params = {"prompt": prompt}  # Pass prompt as a query parameter


        response = requests.post(api_url, files=files, params=params)

        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error(f"Error from backend API: {response.text}")

    else:
        st.warning("Please upload at least one image.")
