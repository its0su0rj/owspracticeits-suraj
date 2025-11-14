import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="Happy Birthday", layout="wide")

# ---------------- HOME PAGE BUTTONS -----------------

st.markdown(
    """
    <h1 style='text-align:center; color:#ff4d6d;'>🎉 Happy Birthday 🎉</h1>
    <h3 style='text-align:center; color:#ff79a8;'>A little surprise waits for you… 💖</h3>
    <br>
    """,
    unsafe_allow_html=True,
)

pg = st.session_state.get("page", "home")

col1, col2, col3, col4 = st.columns(4)
if col1.button("🌈 Journey", use_container_width=True): st.session_state.page = "journey"
if col2.button("✨ Qualities", use_container_width=True): st.session_state.page = "qualities"
if col3.button("💞 Memories", use_container_width=True): st.session_state.page = "memories"
if col4.button("🌟 Future", use_container_width=True): st.session_state.page = "future"

page = st.session_state.get("page", "home")

# Helper to load image

def load_img(name):
    path = f"images/{name}.jpg"
    if os.path.exists(path):
        return Image.open(path)
    return None

# Helper for question-based reveal

def reveal_block(img_name, question, answer, message):
    img = load_img(img_name)
    if img:
        st.image(img, use_column_width=True)

    user = st.text_input(f"❓ {question}", key=img_name)
    if st.button("Submit Answer", key=img_name+"btn"):
        if user.strip().lower() == answer.lower():
            st.success(message)
        else:
            st.error("Try again 😊")
    st.markdown("---")

# ---------------- PAGES -----------------

if page == "journey":
    st.header("🌈 Journey — From Little Moments to Today")
    for i in range(1, 6):
        reveal_block(f"page1.{i}", f"What number is this picture?", str(i), f"💖 This moment was special… and so are you.")

elif page == "qualities":
    st.header("✨ Qualities — The Magic You Carry")
    for i in range(1, 6):
        reveal_block(f"page2.{i}", f"Type the number {i}", str(i), f"🌟 One of your many beautiful qualities shines here.")

elif page == "memories":
    st.header("💞 Memories — Our Sweet Little World")
    for i in range(1, 6):
        reveal_block(f"page3.{i}", f"Enter {i}", str(i), f"📸 A memory worth a thousand smiles.")

elif page == "future":
    st.header("🌟 Future — The Beautiful Path Ahead")
    for i in range(1, 6):
        reveal_block(f"page4.{i}", f"Answer {i}", str(i), f"🚀 The future is bright, and so are you.")
