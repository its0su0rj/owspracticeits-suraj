import streamlit as st
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
    .carousel {
        position: relative;
        width: 100%;
        max-width: 700px;
        margin: auto;
        overflow: hidden;
    }
    .carousel-images {
        display: flex;
        transition: transform 0.5s ease;
    }
    .carousel-images img {
        width: 100%;
    }
    .carousel-controls {
        position: absolute;
        top: 50%;
        width: 100%;
        display: flex;
        justify-content: space-between;
        transform: translateY(-50%);
    }
    .carousel-button {
        background-color: rgba(0,0,0,0.5);
        border: none;
        color: white;
        padding: 10px;
        cursor: pointer;
    }
    .carousel-button:hover {
        background-color: rgba(0,0,0,0.8);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state to store which button was last clicked
if 'page' not in st.session_state:
    st.session_state['page'] = 'Library'

if 'image_index' not in st.session_state:
    st.session_state['image_index'] = 0

# Function to reset the image index
def reset_image_index():
    st.session_state['image_index'] = 0

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

# Function to generate carousel HTML
def generate_carousel(images):
    image_tags = "".join(f'<img src="{img}" alt="Image">' for img in images)
    return f"""
        <div class="carousel">
            <div class="carousel-images">
                {image_tags}
            </div>
            <div class="carousel-controls">
                <button class="carousel-button" onclick="prevSlide()">&#10094;</button>
                <button class="carousel-button" onclick="nextSlide()">&#10095;</button>
            </div>
        </div>
        <script>
        let index = 0;
        const images = document.querySelectorAll('.carousel-images img');

        function showSlide(i) {
            if (i >= images.length) index = 0;
            if (i < 0) index = images.length - 1;
            document.querySelector('.carousel-images').style.transform = `translateX(-${index * 100}%)`;
        }

        function prevSlide() {
            index--;
            showSlide(index);
        }

        function nextSlide() {
            index++;
            showSlide(index);
        }

        document.addEventListener('DOMContentLoaded', () => {
            showSlide(index);
        });
        </script>
    """

# Display content based on the page selected
if st.session_state['page'] == 'Library':
    st.header("Welcome to the Library")
    st.write("This is a brief introduction about the library.")
    
    # List of images
    library_images = [
        "https://via.placeholder.com/800x400?text=Library+Image+1",
        "https://via.placeholder.com/800x400?text=Library+Image+2",
        "https://via.placeholder.com/800x400?text=Library+Image+3"
    ]
    
    # Display image carousel
    st.markdown(generate_carousel(library_images), unsafe_allow_html=True)
    
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

elif st.session_state['page'] == 'Girls':
    st.header("Girls Section")
    
    # List of images
    girls_images = [
        "https://via.placeholder.com/800x400?text=Girls+Image+1",
        "https://via.placeholder.com/800x400?text=Girls+Image+2",
        "https://via.placeholder.com/800x400?text=Girls+Image+3"
    ]
    
    # Display image carousel
    st.markdown(generate_carousel(girls_images), unsafe_allow_html=True)

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
    
    # List of images
    boys_images = [
        "https://via.placeholder.com/800x400?text=Boys+Image+1",
        "https://via.placeholder.com/800x400?text=Boys+Image+2",
        "https://via.placeholder.com/800x400?text=Boys+Image+3"
    ]
    
    # Display image carousel
    st.markdown(generate_carousel(boys_images), unsafe_allow_html=True)

elif st.session_state['page'] == 'About':
    st.header("About")
    st.image("https://via.placeholder.com/800x400?text=Fee+Structure", use_column_width=True)
    st.write("Contact us at:")
    st.write("**Phone:** +1234567890")
    st.write("**Email:** info@example.com")
