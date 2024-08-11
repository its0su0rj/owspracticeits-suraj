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
    
    # Image carousel
    selected_image = st.selectbox("Select an image to view:", list(range(1, len(library_images) + 1)))
    st.image(library_images[selected_image - 1], use_column_width=True)
    
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

elif st.session_state['page'] == 'Girls':
    st.header("Girls Section")
    
    # List of images
    girls_images = [
        "https://via.placeholder.com/800x400?text=Girls+Image+1",
        "https://via.placeholder.com/800x400?text=Girls+Image+2",
        "https://via.placeholder.com/800x400?text=Girls+Image+3"
    ]
    
    # Image carousel
    selected_image = st.selectbox("Select an image to view:", list(range(1, len(girls_images) + 1)))
    st.image(girls_images[selected_image - 1], use_column_width=True)
    
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
    
    # Image carousel
    selected_image = st.selectbox("Select an image to view:", list(range(1, len(boys_images) + 1)))
    st.image(boys_images[selected_image - 1], use_column_width=True)
    
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
    st.image("https://via.placeholder.com/800x400?text=Fee+Structure", use_column_width=True)
    st.write("Contact us at:")
    st.write("**Phone:** +1234567890")
    st.write("**Email:** info@example.com")
