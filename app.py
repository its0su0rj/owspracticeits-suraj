import streamlit as st
from streamlit_image_carousel import image_carousel
import pandas as pd

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
        box-shadow: 0px 4px 2px -2px gray;
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
        transition: background-color 0.3s, box-shadow 0.3s;
    }
    .button:hover {
        background-color: #e0e0e0;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    }
    .icon {
        font-size: 24px;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state to store which button was last clicked
if 'page' not in st.session_state:
    st.session_state['page'] = 'Library'

# Create the button container with icons
st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button(f'<div class="icon">📚</div>Library', unsafe_allow_html=True):
    st.session_state['page'] = 'Library'
if st.button(f'<div class="icon">👧</div>Girls', unsafe_allow_html=True):
    st.session_state['page'] = 'Girls'
if st.button(f'<div class="icon">👦</div>Boys', unsafe_allow_html=True):
    st.session_state['page'] = 'Boys'
if st.button(f'<div class="icon">ℹ️</div>About', unsafe_allow_html=True):
    st.session_state['page'] = 'About'
st.markdown('</div>', unsafe_allow_html=True)

# Add space below the button container to ensure content is visible
st.write("\n\n\n")  # Add space to push down the content below the fixed buttons

# Display content based on the page selected
if st.session_state['page'] == 'Library':
    st.header("Welcome to the Library")
    st.write("This is the introduction about the library. Here you will find a vast collection of books.")
    
    st.subheader("Gallery")
    image_list = [
        "https://via.placeholder.com/300x200?text=Library+1",
        "https://via.placeholder.com/300x200?text=Library+2",
        "https://via.placeholder.com/300x200?text=Library+3"
    ]
    image_carousel(image_list)
    
    st.subheader("Library Introduction Video")
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    st.video(video_url)

elif st.session_state['page'] == 'Girls':
    st.header("Girls Section")
    image_list = [
        "https://via.placeholder.com/300x200?text=Girls+1",
        "https://via.placeholder.com/300x200?text=Girls+2",
        "https://via.placeholder.com/300x200?text=Girls+3"
    ]
    image_carousel(image_list)

    st.subheader("Check Available Slots")
    if st.button("Check Available Slots"):
        data = {
            "Seat No": [i for i in range(1, 13)],
            "Slot 1": ["Available" for _ in range(12)],
            "Slot 2": ["Occupied" for _ in range(12)],
            "Slot 3": ["Available" for _ in range(12)]
        }
        df = pd.DataFrame(data)
        st.table(df)

elif st.session_state['page'] == 'Boys':
    st.header("Boys Section")
    image_list = [
        "https://via.placeholder.com/300x200?text=Boys+1",
        "https://via.placeholder.com/300x200?text=Boys+2",
        "https://via.placeholder.com/300x200?text=Boys+3"
    ]
    image_carousel(image_list)

    st.subheader("Check Available Slots")
    if st.button("Check Available Slots"):
        data = {
            "Seat No": [i for i in range(1, 13)],
            "Slot 1": ["Available" for _ in range(12)],
            "Slot 2": ["Occupied" for _ in range(12)],
            "Slot 3": ["Available" for _ in range(12)]
        }
        df = pd.DataFrame(data)
        st.table(df)

elif st.session_state['page'] == 'About':
    st.header("About Us")
    st.subheader("Fee Structure")
    st.image("/mnt/data/Screenshot_2024-08-11-12-46-11-34_c4b2fae5edd267b2847f1b32e9bc41c3.jpg")

    st.subheader("Contact Information")
    st.write("Phone: +1234567890")
    st.write("Email: info@library.com")
