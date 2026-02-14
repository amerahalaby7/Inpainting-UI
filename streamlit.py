import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

st.title("Image Coordinate Picker")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    st.write("Click on the point you want to select:")
    
    # Display image with click detection
    coordinates = streamlit_image_coordinates(image, key="image")
    
    # Display coordinates when user clicks
    if coordinates:
        st.write(f"Coordinates: X = {coordinates['x']}, Y = {coordinates['y']}")