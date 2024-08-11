import streamlit as st

# Custom CSS to style the buttons, position them horizontally at the top, and add colors
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
        padding: 10px 20px;
        border-radius: 5px;
        text-align: center;
        font-size: 16px;
        cursor: pointer;
        width: 120px;
        color: white;
        text-decoration: none;
    }
    .home-button {
        background-color: #007bff; /* Blue */
    }
    .explore-button {
        background-color: #28a745; /* Green */
    }
    .categories-button {
        background-color: #ffc107; /* Yellow */
    }
    .account-button {
        background-color: #17a2b8; /* Teal */
    }
    .cart-button {
        background-color: #dc3545; /* Red */
    }
    .button:hover {
        opacity: 0.8;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state to store which button was last clicked
if 'page' not in st.session_state:
    st.session_state['page'] = 'Home'

# Create the button container
st.markdown('<div class="button-container">', unsafe_allow_html=True)

# Home Button
if st.markdown('<a href="#" class="button home-button" onclick="javascript:window.location.reload();">Home</a>', unsafe_allow_html=True):
    st.session_state['page'] = 'Home'

# Explore Button
if st.markdown('<a href="#" class="button explore-button" onclick="javascript:window.location.reload();">Explore</a>', unsafe_allow_html=True):
    st.session_state['page'] = 'Explore'

# Categories Button
if st.markdown('<a href="#" class="button categories-button" onclick="javascript:window.location.reload();">Categories</a>', unsafe_allow_html=True):
    st.session_state['page'] = 'Categories'

# Account Button
if st.markdown('<a href="#" class="button account-button" onclick="javascript:window.location.reload();">Account</a>', unsafe_allow_html=True):
    st.session_state['page'] = 'Account'

# Cart Button
if st.markdown('<a href="#" class="button cart-button" onclick="javascript:window.location.reload();">Cart</a>', unsafe_allow_html=True):
    st.session_state['page'] = 'Cart'

st.markdown('</div>', unsafe_allow_html=True)

# Spacer for the fixed position buttons
st.write("\n\n\n\n\n")  # Add space below the button container

# Display content based on the page selected
if st.session_state['page'] == 'Home':
    st.header("Welcome to the Home Page")
    st.write("Here is the introduction and information about the website.")
elif st.session_state['page'] == 'Explore':
    st.header("Explore Page")
    st.write("Explore various features and options.")
elif st.session_state['page'] == 'Categories':
    st.header("Categories Page")
    st.write("Browse through different categories.")
elif st.session_state['page'] == 'Account':
    st.header("Account Page")
    st.write("Manage your account settings and preferences.")
elif st.session_state['page'] == 'Cart':
    st.header("Cart Page")
    st.write("View items in your cart and proceed to checkout.")
