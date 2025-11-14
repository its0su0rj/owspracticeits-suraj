import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="Happy Birthday", layout="wide")

# ---------- STYLING ----------
st.markdown("""
<style>
.main-title {
    text-align:center; font-size:45px; color:#ff4d6d; font-weight:900;
}
.sub-title {
    text-align:center; font-size:22px; color:#ff8fab;
}
.page-header {
    text-align:center; font-size:33px; color:#ff4d6d; font-weight:800; margin-top:10px;
}
.block-box {
    background: #fff0f4; padding:20px; border-radius:18px;
    box-shadow:0px 0px 12px rgba(255,150,180,0.35);
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<div class='main-title'>🎉 Happy Birthday 🎉</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>A small journey filled with feelings… 💖</div>", unsafe_allow_html=True)

# ---------- HOME BUTTONS ----------
pg = st.session_state.get("page", "home")

col1, col2, col3, col4, col5 = st.columns(5)
if col1.button("🌈 Journey", use_container_width=True): st.session_state.page = "journey"
if col2.button("✨ Qualities", use_container_width=True): st.session_state.page = "qualities"
if col3.button("💞 Memories", use_container_width=True): st.session_state.page = "memories"
if col4.button("🌟 Future", use_container_width=True): st.session_state.page = "future"
if col5.button("💌 My Last Message", use_container_width=True): st.session_state.page = "letter"

page = st.session_state.get("page", "home")

# ---------- HELPERS ----------
def load_img(name):
    path = f"images/{name}.jpg"
    if os.path.exists(path): return Image.open(path)
    return None

def load_song(name):
    path = f"songs/{name}.mp3"
    if os.path.exists(path): return open(path, 'rb').read()
    return None

# block: reveal image + message + song after correct answer

def reveal_block(name, question_text, correct_answer, message_text, song_name):
    st.markdown("<div class='block-box'>", unsafe_allow_html=True)

    # user question
    user = st.text_input(question_text, key=name)
    if st.button("Submit", key=name+"btn"):
        if user.strip().lower() == correct_answer.lower():
            st.success("Correct! 💖")

            # show image
            img = load_img(name)
            if img: st.image(img, use_column_width=True)

            # show message
            st.markdown(f"<p style='font-size:20px; color:#d6336c;'><b>{message_text}</b></p>", unsafe_allow_html=True)

            # play song
            song = load_song(song_name)
            if song: st.audio(song)
        else:
            st.error("Try again 😊")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>")

# ---------- PAGES ----------

if page == "journey":
    st.markdown("<div class='page-header'>🌈 Journey — From Little Steps to Beautiful Love</div>", unsafe_allow_html=True)

    # YOU WILL WRITE REAL QUESTIONS + MESSAGES + SONG NAMES HERE
    reveal_block("page1.1", "Type the number which is my favourite ", "15", "Your beautiful message here…", "song1")
    reveal_block("page1.2", "Write question 2…", "ans2", "Message 2…", "song2")
    reveal_block("page1.3", "Write question 3…", "ans3", "Message 3…", "song3")
    reveal_block("page1.4", "Write question 4…", "ans4", "Message 4…", "song4")

elif page == "qualities":
    st.markdown("<div class='page-header'>✨ Qualities — The Magic You Carry</div>", unsafe_allow_html=True)

    reveal_block("page2.1", "Your question…", "ans1", "Message…", "song1")
    reveal_block("page2.2", "Your question…", "ans2", "Message…", "song2")
    reveal_block("page2.3", "Your question…", "ans3", "Message…", "song3")
    reveal_block("page2.4", "Your question…", "ans4", "Message…", "song4")

elif page == "memories":
    st.markdown("<div class='page-header'>💞 Memories — These Moments Live Forever</div>", unsafe_allow_html=True)

    reveal_block("page3.1", "Your question…", "ans1", "Message…", "song1")
    reveal_block("page3.2", "Your question…", "ans2", "Message…", "song2")
    reveal_block("page3.3", "Your question…", "ans3", "Message…", "song3")
    reveal_block("page3.4", "Your question…", "ans4", "Message…", "song4")

elif page == "future":
    st.markdown("<div class='page-header'>🌟 Future — A Beautiful Tomorrow Awaits</div>", unsafe_allow_html=True)

    reveal_block("page4.1", "Your question…", "ans1", "Message…", "song1")
    reveal_block("page4.2", "Your question…", "ans2", "Message…", "song2")
    reveal_block("page4.3", "Your question…", "ans3", "Message…", "song3")
    reveal_block("page4.4", "Your question…", "ans4", "Message…", "song4")

elif page == "letter":
    st.markdown("<div class='page-header'>💌 My Last Message For You</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='block-box' style='font-size:20px; line-height:1.6; color:#c9184a;'>
    💖 Sometimes words fall short, but feelings don't.<br><br>
    💫 If I could capture every emotion I feel for you, the sky would run out of stars.<br><br>
    🌷 You are not just a part of my life — you are the softest chapter, the sweetest page.<br><br>
    🌙 I wish your birthday brings you endless smiles, warm hugs, and moments that feel like magic.
    </div>
    """, unsafe_allow_html=True)
