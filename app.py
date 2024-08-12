import streamlit as st
import pandas as pd
import os

# List of images for each section
library_images = [
    "https://via.placeholder.com/800x400?text=Library+Image+1",
    "https://via.placeholder.com/800x400?text=Library+Image+2",
    "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/IMG-20240812-WA0001.jpg"  # Updated GitHub URL
]

girls_images = [
    "https://via.placeholder.com/800x400?text=Girls+Image+1",
    "https://via.placeholder.com/800x400?text=Girls+Image+2",
    "https://via.placeholder.com/800x400?text=Girls+Image+3"
]

boys_images = [
    "https://via.placeholder.com/800x400?text=Boys+Image+1",
    "https://via.placeholder.com/800x400?text=Boys+Image+2",
    "https://via.placeholder.com/800x400?text=Boys+Image+3"
]

# Custom CSS for the navigation bar
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
    </style>
""", unsafe_allow_html=True)

# Initialize session state to store which button was last clicked
if 'page' not in st.session_state:
    st.session_state['page'] = 'Library'

# Create the button container
st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button('📚 Library'):
    st.session_state['page'] = 'Library'
if st.button('👧 Girls'):
    st.session_state['page'] = 'Girls'
if st.button('👦 Boys'):
    st.session_state['page'] = 'Boys'
if st.button('ℹ️ About'):
    st.session_state['page'] = 'About'
st.markdown('</div>', unsafe_allow_html=True)

# Add some space below the button container
st.write("\n\n") 

# Function to display images one below the other
def display_images(images):
    for img in images:
        st.image(img, use_column_width=True)

# Display content based on the page selected
if st.session_state['page'] == 'Library':
    st.header("Welcome to the Library")
    st.write("This is a brief introduction about the library.")
    st.markdown('[Chat with us on WhatsApp](https://wa.me/8809680722)')
    display_images(library_images)
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

elif st.session_state['page'] == 'Girls':
    st.header("Girls Section")
    if st.button('Check Available Slots'):
        try:
            df = pd.read_csv(os.path.join('girls_slots.csv'))
            st.table(df)
        except Exception as e:
            st.error(f"Error loading the CSV file: {e}")
    display_images(girls_images)

elif st.session_state['page'] == 'Boys':
    st.header("Boys Section")
    if st.button('Check Available Slots'):
        try:
            df = pd.read_csv(os.path.join('boys_slots.csv'))
            st.table(df)
        except Exception as e:
            st.error(f"Error loading the CSV file: {e}")
    display_images(boys_images)

elif st.session_state['page'] == 'About':
    st.header("About")
    st.image("https://via.placeholder.com/800x400?text=Fee+Structure", use_column_width=True)
    st.write("Contact us at:")
    st.write("**Phone:** +1234567890")
    st.write("**Email:** info@example.com")
