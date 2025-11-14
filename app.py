import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="Happy Birthday", layout="wide")

# ---------- GLOBAL STYLING ----------
st.markdown("""
<style>
/* Floating hearts */
@keyframes floatHeart {
  0% {transform: translateY(0) scale(1); opacity: 1;}
  100% {transform: translateY(-200px) scale(1.6); opacity: 0;}
}
.heart {
  position: fixed;
  bottom: 10px;
  right: 10px;
  font-size: 22px;
  color: #ff4d6d;
  animation: floatHeart 4s linear infinite;
  z-index: 9999;
}

/* Glow and highlighting */
.glow {
  text-shadow: 0 0 12px #ff4d6d, 0 0 22px #ff8fab;
}

/* Page Titles */
.main-title {
    text-align:center; font-size:50px; color:#ff4d6d; font-weight:900;
    text-shadow:0px 0px 18px #ff8fab;
}
.sub-title {
    text-align:center; font-size:22px; color:#ff8fab;
}
.page-header {
    text-align:center; font-size:33px; color:#ff4d6d; font-weight:800; margin-top:10px;
    text-shadow:0px 0px 10px #ffb3c6;
}

/* Block Box */
.block-box {
    background: rgba(255,240,244,0.9);
    padding:20px; border-radius:18px;
    box-shadow:0px 0px 20px rgba(255,150,180,0.45);
    backdrop-filter: blur(4px);
}
</style>

<div class='heart'>❤️</div>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<div class='main-title glow'>🎉 Happy Birthday My Love 🎉</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>A journey of you.. filled with your beauty, noor, elegance and magic 💖</div>", unsafe_allow_html=True)

# ---------- PAGE BUTTONS ----------
col1, col2, col3, col4, col5 = st.columns(5)
if col1.button("🌈 Journey", use_container_width=True): st.session_state.page = "journey"
if col2.button("✨ Qualities", use_container_width=True): st.session_state.page = "qualities"
if col3.button("💞 Memories", use_container_width=True): st.session_state.page = "memories"
if col4.button("🌟 Future", use_container_width=True): st.session_state.page = "future"
if col5.button("💌 My Last Message", use_container_width=True): st.session_state.page = "letter"

page = st.session_state.get("page", "journey")

# ---------- HELPERS ----------
def load_img(name):
    exts = [".jpg", ".jpeg", ".png", ".webp"]
    for e in exts:
        p = f"images/{name}{e}"
        if os.path.exists(p): return Image.open(p)
    return None

def load_song(name):
    p = f"songs/{name}.mp3"
    if os.path.exists(p): return open(p, 'rb').read()
    return None

# ---------- SPECIAL REVEAL (ONLY PAGE 1 HAS QUESTIONS) ----------
def reveal_q(name, question, correct_answer, message, song_name):
    st.markdown("<div class='block-box'>", unsafe_allow_html=True)
    user = st.text_input(question, key=name)

    if st.button("Submit", key=name+"btn"):
        if user.strip().lower() == correct_answer.lower():
            st.success("Correct baby! 💖🥺✨")
            img = load_img(name)
            if img: st.image(img, use_column_width=True)
            st.markdown(f"<p style='font-size:20px; color:#d6336c;'><b>{message}</b></p>", unsafe_allow_html=True)
            song = load_song(song_name)
            if song: st.audio(song)
        else:
            st.error("Nahi jaanu… phir se try karo 🥺💞")

    st.markdown("</div><br>", unsafe_allow_html=True)

# ---------- STANDARD IMAGE + ROMANTIC MESSAGE (NO QUESTIONS) ----------
def reveal_auto(name, message):
    st.markdown("<div class='block-box'>", unsafe_allow_html=True)
    img = load_img(name)
    if img: st.image(img, use_column_width=True)
    st.markdown(f"<p style='font-size:20px; color:#d6336c;'><b>{message}</b></p>", unsafe_allow_html=True)
    st.markdown("</div><br>", unsafe_allow_html=True)

# ---------- PAGE 1 : Questions GO HERE ----------
if page == "journey":
    st.markdown("<div class='page-header glow'>🌈 Journey — You Since Childhood</div>", unsafe_allow_html=True)

    reveal_q(
        "page1.1",
        "1. In childhood you were cute or supercute? ❤️",
        "supercute",
        "From day one… your face had that angel charm. Supercute is still less… you were meant to glow. ✨🥺❤️",
        "song1"
    )
    reveal_q(
        "page1.2",
        "2. Best duo… with whom? (Ma or life partner) 💕",
        "ma",
        "Your bond with your Ma is the purest. The softness in your heart comes from her… and the love in your eyes too. 💖",
        "song2"
    )
    reveal_q(
        "page1.3",
        "3. First time in Muzaf… Rakhi trip… Which colored top? (red or black) 🎀",
        "red",
        "That red top… uff. Even the sun would've been jealous of your warm glow that day. 🔥❤️",
        "song3"
    )
    reveal_q(
        "page1.4",
        "4. You looked gorgeous during Chhath… more beautiful in morning or evening? 🌅",
        "evening",
        "Evening light touching your face is like God painting his favorite creation. Noor hi noor. ✨😍",
        "song4"
    )

# ---------- PAGE 2 : Qualities ----------
elif page == "qualities":
    st.markdown("<div class='page-header glow'>✨ Your Qualities — The Magic You Carry</div>", unsafe_allow_html=True)

    romantic_msgs = [
        "Your intelligence shines brighter than your beauty… and that's saying something because you're breathtaking. 💖",
        "Your confidence is quiet, elegant and powerful… just like you. 🌹✨",
        "Your smile? A full weapon. Even my sadness bows down before it. 😊❤️",
        "Your presence feels like calmness wrapped in softness. Noor ki dukaan ho tum. ✨😍"
    ]

    for i in range(1,5):
        reveal_auto(f"page2.{i}", romantic_msgs[i-1])

# ---------- PAGE 3 : Memories ----------
elif page == "memories":
    st.markdown("<div class='page-header glow'>💞 Memories — Our Sweetest Moments</div>", unsafe_allow_html=True)

    memory_msgs = [
        "Some moments aren't just memories… they are feelings that stay alive forever. 💕",
        "Every picture with you is a festival for my heart. 🥺❤️",
        "Your laughter in these memories still echoes in my chest… soft and magical. ✨",
        "These aren’t just memories… these are reasons I fall for you again. 💖"
    ]

    for i in range(1,5):
        reveal_auto(f"page3.{i}", memory_msgs[i-1])

# ---------- PAGE 4 : Future ----------
elif page == "future":
    st.markdown("<div class='page-header glow'>🌟 Future — A Beautiful Tomorrow Awaits</div>", unsafe_allow_html=True)

    future_msgs = [
        "The future looks beautiful… because you are in it. 🌈❤️",
        "Some dreams are meant to be lived together… ours is one of them. ✨",
        "Your potential is limitless… I can't wait to see you win. 🌟",
        "One day we'll look back at today and smile… knowing love grew stronger. 💞"
    ]

    for i in range(1,5):
        reveal_auto(f"page4.{i}", future_msgs[i-1])

# ---------- LAST PAGE ----------
elif page == "letter":
    st.markdown("<div class='page-header glow'>💌 My Last Message For You</div>", unsafe_ALLOW_HTML=True)

    bg = load_song("lastsong")
    if bg: st.audio(bg)

    st.markdown("""
    <div class='block-box' style='font-size:20px; line-height:1.6; color:#c9184a;'>
    ❤️ If love had a face… it would look like you.<br><br>
    🌙 Every day with you feels like softness, warmth and magic stitched together.<br><br>
    ✨ You are not just beautiful… you are rare. The kind of girl for whom even destiny pauses.<br><br>
    💕 I don't know what the future holds… but I know one thing — my heart already chose you.<br><br>
    🎀 Happy Birthday, meri jaan. You deserve galaxies. Not just today… but always.
    </div>
    """, unsafe_allow_html
