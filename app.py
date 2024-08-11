import streamlit as st

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
    </style>
""", unsafe_allow_html=True)

# Initialize session state to store which button was last clicked
if 'page' not in st.session_state:
    st.session_state['page'] = 'Home'

# Create the button container
st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button('Home'):
    st.session_state['page'] = 'Home'
if st.button('Explore'):
    st.session_state['page'] = 'Explore'
if st.button('Categories'):
    st.session_state['page'] = 'Categories'
if st.button('Account'):
    st.session_state['page'] = 'Account'
if st.button('Cart'):
    st.session_state['page'] = 'Cart'
st.markdown('</div>', unsafe_allow_html=True)

# Display content based on the page selected
st.write("\n\n")  # Add some space below the button container
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
