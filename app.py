import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Initialize session state to store which button was last clicked
if 'page' not in st.session_state:
    st.session_state['page'] = 'Library'

# Function to reset the image index
def reset_image_index():
    st.session_state['image_index'] = 0

# Custom CSS to style the buttons and position them horizontally at the top
st.markdown("""
    <style>
    .button-container {
        display: flex;
        justify-content: space-around;
        background-color: #f8f9fa;
        padding: 10px;
        position: fixed;
        width: 100%;
        top: 0;
        left: 0;
        z-index: 1000;
    }
    .button {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 10px 20px;
        border-radius: 5px;
        text-align: center;
        font-size: 16px;
        cursor: pointer;
        width: 100px;
    }
    .button:hover {
        background-color: #e0e0e0;
    }
    .icon {
        font-size: 20px;
        margin-right: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Create the button container
st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button('📚 Library', on_click=reset_image_index):
    st.session_state['page'] = 'Library'
if st.button('👧 Girls', on_click=reset_image_index):
    st.session_state['page'] = 'Girls'
if st.button('👦 Boys', on_click=reset_image_index):
    st.session_state['page'] = 'Boys'
if st.button('ℹ️ About', on_click=reset_image_index):
    st.session_state['page'] = 'About'
st.markdown('</div>', unsafe_allow_html=True)

# Add some space below the button container
st.write("\n\n") 

# Carousel component
imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

# Page-specific content
if st.session_state['page'] == 'Library':
    st.header("Welcome to the Library")
    st.write("This is a brief introduction about the library.")
    
    # List of images for Library
    library_images = [
        "https://via.placeholder.com/800x400?text=Library+Image+1",
        "https://via.placeholder.com/800x400?text=Library+Image+2",
        "https://via.placeholder.com/800x400?text=Library+Image+3"
    ]
    
    # Display the image carousel
    selectedImageUrl = imageCarouselComponent(imageUrls=library_images, height=400)
    
    if selectedImageUrl:
        st.image(selectedImageUrl, width=700)
    
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

elif st.session_state['page'] == 'Girls':
    st.header("Girls Section")
    
    # List of images for Girls
    girls_images = [
        "https://via.placeholder.com/800x400?text=Girls+Image+1",
        "https://via.placeholder.com/800x400?text=Girls+Image+2",
        "https://via.placeholder.com/800x400?text=Girls+Image+3"
    ]
    
    # Display the image carousel
    selectedImageUrl = imageCarouselComponent(imageUrls=girls_images, height=400)
    
    if selectedImageUrl:
        st.image(selectedImageUrl, width=700)
    
    if st.button('Check Available Slots'):
        # Create a DataFrame to display the available slots
        data = {
            'Seat No': [f'Seat {i}' for i in range(1, 13)],
            'Slot 1': ['Available']*12,
            'Slot 2': ['Occupied']*12,
            'Slot 3': ['Available']*12
        }
        df = pd.DataFrame(data)
        st.table(df)

elif st.session_state['page'] == 'Boys':
    st.header("Boys Section")
    
    # List of images for Boys
    boys_images = [
        "https://via.placeholder.com/800x400?text=Boys+Image+1",
        "https://via.placeholder.com/800x400?text=Boys+Image+2",
        "https://via.placeholder.com/800x400?text=Boys+Image+3"
    ]
    
    # Display the image carousel
    selectedImageUrl = imageCarouselComponent(imageUrls=boys_images, height=400)
    
    if selectedImageUrl:
        st.image(selectedImageUrl, width=700)
    
    if st.button('Check Available Slots'):
        # Create a DataFrame to display the available slots
        data = {
            'Seat No': [f'Seat {i}' for i in range(1, 13)],
            'Slot 1': ['Available']*12,
            'Slot 2': ['Occupied']*12,
            'Slot 3': ['Available']*12
        }
        df = pd.DataFrame(data)
        st.table(df)

elif st.session_state['page'] == 'About':
    st.header("About")
    st.image("https://via.placeholder.com/800x400?text=Fee+Structure", width=700)
    st.write("Contact us at:")
    st.write("**Phone:** +1234567890")
    st.write("**Email:** info@example.com")

