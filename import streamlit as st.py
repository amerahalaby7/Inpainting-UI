import streamlit as st
from PIL import Image

st.title("Image Coordinate Picker")

# رفع الصورة - هنستخدم نص انجليزي في label
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # فتح الصورة
    image = Image.open(uploaded_file)
    
    # عرض الصورة
    st.image(image, caption="Uploaded Image", use_container_width=True) 