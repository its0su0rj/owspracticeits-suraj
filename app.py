import streamlit as st

# Initialize session state to store which button was last clicked
if 'page' not in st.session_state:
    st.session_state['page'] = 'Home'

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
    .stButton > button {
        margin: 0px 5px;
        width: 120px;
        height: 40px;
        color: white;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        font-size: 16px;
    }
    .home-button {
        background-color: #007bff; /* Blue */
    }
    .explore-button {
        background-color: #28a745; /* Green */
    }
    .categories-button {
        background-color: #ffc107; /* Yellow */
        color: black;
    }
    .account-button {
        background-color: #17a2b8; /* Teal */
    }
    .cart-button {
        background-color: #dc3545; /* Red */
    }
    </style>
""", unsafe_allow_html=True)

# Create the button container
st.markdown('<div class="button-container">', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button('Home'):
        st.session_state['page'] = 'Home'
    st.markdown('<style>div.stButton > button:first-child {background-color: #007bff;}</style>', unsafe_allow_html=True)

with col2:
    if st.button('Explore'):
        st.session_state['page'] = 'Explore'
    st.markdown('<style>div.stButton > button:first-child {background-color: #28a745;}</style>', unsafe_allow_html=True)

with col3:
    if st.button('Categories'):
        st.session_state['page'] = 'Categories'
    st.markdown('<style>div.stButton > button:first-child {background-color: #ffc107; color: black;}</style>', unsafe_allow_html=True)

with col4:
    if st.button('Account'):
        st.session_state['page'] = 'Account'
    st.markdown('<style>div.stButton > button:first-child {background-color: #17a2b8;}</style>', unsafe_allow_html=True)

with col5:
    if st.button('Cart'):
        st.session_state['page'] = 'Cart'
    st.markdown('<style>div.stButton > button:first-child {background-color: #dc3545;}</style>', unsafe_allow_html=True)

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
