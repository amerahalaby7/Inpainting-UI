import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
st.title("Image Coordinate Picker")

# Upload image
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    st.write("Click on the point you want to select:")
    
    # Display image with click detection
    coordinates = streamlit_image_coordinates(image, key="image")
    
    # Store coordinates in session state
    if coordinates:
        st.session_state['x'] = coordinates['x']
        st.session_state['y'] = coordinates['y']
    
    # Display selected coordinates
    if 'x' in st.session_state and 'y' in st.session_state:
        st.success(f"Selected Coordinates: X = {st.session_state['x']}, Y = {st.session_state['y']}")
        
        # Button to send request
        if st.button("Process Image"):
            st.write("Sending request to FastAPI...")
            
            # هنا هنحط الكود بتاع إرسال الطلب للـ FastAPI
            
            st.write("---")
            st.subheader("Output Image:")
            # عرض الصورة الأصلية مؤقتاً
            st.image(image, caption="Processing...", use_container_width=True)