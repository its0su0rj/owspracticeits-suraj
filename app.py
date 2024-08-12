import streamlit as st
import pandas as pd
import os

# List of images for each section
library_images = [
    "https://via.placeholder.com/800x400?text=Library+Image+1",
    "https://via.placeholder.com/800x400?text=Library+Image+2",
    "https://via.placeholder.com/800x400?text=Library+Image+3"
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

# Custom CSS for buttons and carousel
carousel_script = """
    <script>
        let currentSlide = 0;
        function showSlide(index) {
            const slides = document.getElementsByClassName('carousel-slide');
            if (index >= slides.length) currentSlide = 0;
            if (index < 0) currentSlide = slides.length - 1;
            for (let i = 0; i < slides.length; i++) {
                slides[i].style.display = 'none';
            }
            slides[currentSlide].style.display = 'block';
        }
        function nextSlide() {
            currentSlide++;
            showSlide(currentSlide);
        }
        function prevSlide() {
            currentSlide--;
            showSlide(currentSlide);
        }
        document.addEventListener('DOMContentLoaded', function () {
            showSlide(currentSlide);
            document.getElementById('prev').addEventListener('click', prevSlide);
            document.getElementById('next').addEventListener('click', nextSlide);
        });
    </script>
    <style>
        .carousel-container {
            max-width: 100%;
            margin: auto;
            position: relative;
        }
        .carousel-slide {
            display: none;
            width: 100%;
            height: auto;
        }
        .carousel-button {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background-color: rgba(0, 0, 0, 0.5);
            color: white;
            border: none;
            padding: 10px;
            cursor: pointer;
            z-index: 1001;
        }
        .carousel-button#prev {
            left: 0;
        }
        .carousel-button#next {
            right: 0;
        }
        
        /* Custom CSS for the navigation bar */
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
"""

def create_carousel(images):
    carousel_images = ''.join([f'<img src="{img}" class="carousel-slide">' for img in images])
    carousel_buttons = '''
        <button id="prev" class="carousel-button">&#10094;</button>
        <button id="next" class="carousel-button">&#10095;</button>
    '''
    st.components.v1.html(f'<div class="carousel-container">{carousel_images}{carousel_buttons}</div>{carousel_script}', height=550)

# Add the custom CSS for the buttons
st.markdown(f"{carousel_script}", unsafe_allow_html=True)

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

# Display content based on the page selected
if st.session_state['page'] == 'Library':
    st.header("Welcome to the Library")
    st.write("This is a brief introduction about the library.")
    st.markdown('[Chat with us on WhatsApp](https://wa.me/8809680722)')
    create_carousel(library_images)
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

elif st.session_state['page'] == 'Girls':
    st.header("Girls Section")
    #create_carousel(girls_images)
    if st.button('Check Available Slots'):
        try:
            df = pd.read_csv(os.path.join('girls_slots.csv'))
            st.table(df)
        except Exception as e:
            st.error(f"Error loading the CSV file: {e}")
    create_carousel(girls_images)

    
    #if st.button('Check Available Slots'):
     #   # URL of the CSV file on GitHub for the Girls section
      #  csv_url = "https://github.com/its0su0rj/owspracticeits-suraj/blob/c0d780332ca385c8879d8ac813727b0b990b9e56/slots.csv"
       # 
        ## Fetch and display the CSV data
        #df = pd.read_csv(csv_url)
        #st.table(df)
  

elif st.session_state['page'] == 'Boys':
    st.header("Boys Section")
    #create_carousel(boys_images)
    
    #if st.button('Check Available Slots'):
        # URL of the CSV file on GitHub for the Boys section
     #   csv_url = "https://github.com/its0su0rj/owspracticeits-suraj/blob/f29a7634156756b337291c96e1ebd1eb94f66b23/slots_17_rows.csv"
        
        # Fetch and display the CSV data
      #  df = pd.read_csv(csv_url)
       # st.table(df)
    if st.button('Check Available Slots'):
        try:
            df = pd.read_csv(os.path.join('boys_slots.csv'))
            st.table(df)
        except Exception as e:
            st.error(f"Error loading the CSV file: {e}")
    create_carousel(boys_images)

elif st.session_state['page'] == 'About':
    st.header("About")
    st.image("https://via.placeholder.com/800x400?text=Fee+Structure", use_column_width=True)
    st.write("Contact us at:")
    st.write("**Phone:** +1234567890")
    st.write("**Email:** info@example.com")
