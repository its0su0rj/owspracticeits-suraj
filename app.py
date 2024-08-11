import streamlit as st
from streamlit.components.v1 import html

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

# Custom CSS and JavaScript for carousel
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
            max-width: 800px;
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
    </style>
"""

def create_carousel(images):
    carousel_images = ''.join([f'<img src="{img}" class="carousel-slide">' for img in images])
    carousel_buttons = '''
        <button id="prev" class="carousel-button">&#10094;</button>
        <button id="next" class="carousel-button">&#10095;</button>
    '''
    st.components.v1.html(f'<div class="carousel-container">{carousel_images}{carousel_buttons}</div>{carousel_script}', height=450)

# Initialize session state to store which button was last clicked
if 'page' not in st.session_state:
    st.session_state['page'] = 'Library'

# Create the button container
st.sidebar.header("Navigation")
if st.sidebar.button('📚 Library'):
    st.session_state['page'] = 'Library'
if st.sidebar.button('👧 Girls'):
    st.session_state['page'] = 'Girls'
if st.sidebar.button('👦 Boys'):
    st.session_state['page'] = 'Boys'
if st.sidebar.button('ℹ️ About'):
    st.session_state['page'] = 'About'

# Display content based on the page selected
if st.session_state['page'] == 'Library':
    st.header("Welcome to the Library")
    st.write("This is a brief introduction about the library.")
    create_carousel(library_images)
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

elif st.session_state['page'] == 'Girls':
    st.header("Girls Section")
    create_carousel(girls_images)
    if st.button('Check Available Slots'):
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
    create_carousel(boys_images)
    if st.button('Check Available Slots'):
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
    st.image("https://via.placeholder.com/800x400?text=Fee+Structure", use_column_width=True)
    st.write("Contact us at:")
    st.write("**Phone:** +1234567890")
    st.write("**Email:** info@example.com")
