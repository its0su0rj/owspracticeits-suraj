import streamlit as st
import pandas as pd
import os

# List of images for each section
library_images = [
    
    "https://raw.githubusercontent.com/guptaankit01/krishnalibrary/main/library1.jpg",
    "https://raw.githubusercontent.com/guptaankit01/krishnalibrary/main/library2.jpg",
    "https://raw.githubusercontent.com/guptaankit01/krishnalibrary/main/library31.jpg",
    "https://raw.githubusercontent.com/guptaankit01/krishnalibrary/main/library4.jpg",
    "https://raw.githubusercontent.com/guptaankit01/krishnalibrary/main/librarylast.jpg"# Updated GitHub URL
]

girls_images = [
    
    "https://raw.githubusercontent.com/guptaankit01/krishnalibrary/main/girls1.jpg"
]

boys_images = [
    "https://raw.githubusercontent.com/guptaankit01/krishnalibrary/main/boys1.jpg"
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
    st.header("Welcome to the Krishna Library")
    st.write(
    "The library features a beautiful, calming environment with air conditioning, comfortable chairs, and proper tables. It is designed to support long-hour study sessions effectively."
)
    st.markdown(
    "<span style='color:red; font-weight:bold;'>A 24/7 CCTV monitoring system ensures safety at all times.</span>",
    unsafe_allow_html=True
)


    st.markdown('[Chat with us on WhatsApp](https://wa.me/8809680722)')
    display_images(library_images)
    st.video("https://youtu.be/GlUyCSSF6RI?si=1MZFVshIQxZ8jKl-")

elif st.session_state['page'] == 'Girls':
    st.header("Girls Section")
    st.write(
    "A 24/7 CCTV monitoring system ensures safety at all times.\n\n")
    st.markdown(
    "<span style='color:green; font-weight:bold;'>To all the girls studying here: Embrace your strength, pursue your passions with determination, and let this library be a sanctuary where your dreams take flight. Your dedication and hard work will pave the way for a brighter future.</span>",
    unsafe_allow_html=True
)
    st.write("avl=seat available, res=seat taken")


    if st.button('Check Available Slots'):
        try:
            df = pd.read_csv(os.path.join('girls_slots.csv'))
            st.table(df)
        except Exception as e:
            st.error(f"Error loading the CSV file: {e}")
    display_images(girls_images)

elif st.session_state['page'] == 'Boys':
    st.header("Boys Section")
    st.write("avl=seat available, res=seat taken")
    if st.button('Check Available Slots'):
        try:
            df = pd.read_csv(os.path.join('boys_slots.csv'))
            st.table(df)
        except Exception as e:
            st.error(f"Error loading the CSV file: {e}")
    display_images(boys_images)

elif st.session_state['page'] == 'About':
    st.header("About")
    st.image("https://raw.githubusercontent.com/guptaankit01/krishnalibrary/main/fee.jpg", use_column_width=True)
    st.write("Contact us at:")
    st.write("Ankit Gupta")
    st.write("**Phone:** 8809680722")
    st.write("**Email:** akedufiles@gmail.com")
