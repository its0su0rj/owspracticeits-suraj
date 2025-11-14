# app.py
# Final cleaned romantic birthday app
# Place images in ./images/ as page1.1.jpg (or page1_1.jpg) ... page4.4.jpg
# Place songs in ./songs/: song1.mp3, song2.mp3, song3.mp3, song4.mp3, lastsong.mp3, optional background.mp3

import streamlit as st
from PIL import Image, ImageOps
import os, base64, random

st.set_page_config(page_title="🎉 Happy Birthday", layout="wide")

# ------------------ Editable content ------------------
# Page 1 has 4 questions (you provided). Case-insensitive.
QUESTIONS_PAGE1 = [
    "1. In childhood you were cute or supercute? (Write 'cute' or 'supercute')",
    "2. Best duo... with whom? (Write 'ma' or 'life partner')",
    "3. First time rakhi trip: which top color did you wear? (red or black)",
    "4. You look gorgeous in Chhath — more beautiful in evening or morning?"
]
ANSWERS_PAGE1 = ["supercute", "ma", "red", "evening"]  # case-insensitive

# Romantic messages for all pages are auto-filled (you requested)
MESSAGES_PAGE2 = [
    "Your intelligence sparkles like stars; your beauty only highlights it. You are flawless.",
    "Confidence and kindness — you wear them both effortlessly. I admire you every day.",
    "Your laugh breaks the clouds away — everything brighter with you in it.",
    "You are a radiant presence; the world is softer when you smile."
]

MESSAGES_PAGE3 = [
    "This memory is a warm lamp in my heart — forever glowing because of you.",
    "Every photo with you is a chapter of joy I read again and again.",
    "Your laughter in these moments still lives in my chest — soft and warm.",
    "I fall for you again in every memory; thank you for being my favorite."
]

MESSAGES_PAGE4 = [
    "The future looks golden because you will shine in everything you do.",
    "I see travel, laughter, growth and us — all painted with your light.",
    "You will achieve so much; your strength humbles and inspires me.",
    "We'll turn tiny moments into a grand love story — and I can't wait."
]

# Song filenames (page1 reveals). Put these files inside songs/
SONG_SLOT_FILES = ["song1.mp3", "song2.mp3", "song3.mp3", "song4.mp3"]
# Final message song
LAST_SONG_FILE = "lastsong.mp3"
# Background ambient music (optional)
BACKGROUND_FILE = "background.mp3"

ITEMS_PER_PAGE = 4

# ------------------ Styling & effects ------------------
st.markdown("""
<style>
.main-title {text-align:center; font-size:44px; color:#ff2d6f; font-weight:900; margin-bottom:6px;}
.subtitle {text-align:center; font-size:16px; color:#ff8fab; margin-bottom:14px;}
/* heartbeat + glow for all buttons */
button[kind="primary"], button[kind="secondary"], .stButton>button {
  animation: heartbeat 1.6s infinite;
  border-radius: 12px !important;
  box-shadow: 0 8px 22px rgba(255,77,109,0.12);
  font-weight:700 !important;
}
.stButton>button:hover { box-shadow: 0 12px 34px rgba(255,50,90,0.2); transform: translateY(-3px); }
@keyframes heartbeat {
  0% {transform: scale(1);}
  25% {transform: scale(1.06);}
  40% {transform: scale(0.98);}
  60% {transform: scale(1.03);}
  100% {transform: scale(1);}
}

/* glowing reveal box */
.glow-box { background: linear-gradient(180deg,#fff7fb,#fff1f6); padding:14px; border-radius:12px;
           box-shadow: 0 8px 30px rgba(255,120,150,0.06); border: 1px solid rgba(255,100,140,0.08);
           margin-bottom: 12px;
}

/* floating hearts and sparkles */
.heart { position: fixed; bottom: 12px; left: 50%; transform: translateX(-50%); font-size:28px; z-index:9999; opacity:0.95;}
.sparkle { position: fixed; top:-10px; font-size:20px; color:#ffd6e8; z-index:9998; pointer-events:none; }

/* typewriter container */
.typewriter { font-size:18px; color:#c81d62; font-weight:700; white-space: pre-wrap; }

/* page header */
.page-header { text-align:center; font-size:28px; color:#ff3b6b; margin-top:10px; margin-bottom:8px; font-weight:800; }
</style>

<div class="heart">💖</div>
<div class="sparkle" style="left:20%; animation: fall 6s linear infinite;">✨</div>
<div class="sparkle" style="left:40%; animation: fall 7s linear infinite;">🌟</div>
<div class="sparkle" style="left:60%; animation: fall 5.5s linear infinite;">💫</div>
""", unsafe_allow_html=True)

# Background music injection (optional)
def inject_background(path="songs/" + BACKGROUND_FILE):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        html = f"""
        <audio autoplay loop controls style="position:fixed; bottom:16px; right:16px; width:260px; z-index:9999; opacity:0.92;">
            <source src="data:audio/mp3;base64,{data}" type="audio/mp3">
        </audio>
        """
        st.markdown(html, unsafe_allow_html=True)

inject_background()

st.markdown("<div class='main-title'>🎉 Happy Birthday! 🎉</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>A little interactive journey — unlock images, messages & songs ✨</div>", unsafe_allow_html=True)

# ------------------ Page navigation buttons on homepage ------------------
if 'page' not in st.session_state:
    st.session_state.page = "home"

# Homepage buttons
if st.session_state.page == "home":
    c1, c2, c3, c4, c5 = st.columns([1,1,1,1,0.6])
    with c1:
        if st.button("🌈 Journey", key="btn_journey"): st.session_state.page = "journey"
    with c2:
        if st.button("✨ Qualities", key="btn_qualities"): st.session_state.page = "qualities"
    with c3:
        if st.button("💞 Memories", key="btn_memories"): st.session_state.page = "memories"
    with c4:
        if st.button("🌟 Future", key="btn_future"): st.session_state.page = "future"
    with c5:
        if st.button("💌 My Last Message", key="btn_letter"): st.session_state.page = "letter"
# If user navigated to a page directly earlier, we keep that in session_state
if st.session_state.page == "home":
    st.info("Click a section to begin — Journey, Qualities, Memories, Future, or My Last Message.")

# --------------- Utilities for files ---------------
def find_image(base_name):
    # tries dot and underscore variants and common extensions
    exts = [".jpg", ".jpeg", ".png", ".webp"]
    variants = [base_name, base_name.replace(".", "_")]
    for v in variants:
        for e in exts:
            path = os.path.join("images", v + e)
            if os.path.exists(path):
                return path
    return None

def find_song(base_name):
    variants = [base_name, base_name.replace(".", "_")]
    exts = [".mp3", ".wav", ".ogg"]
    for v in variants:
        for e in exts:
            path = os.path.join("songs", v + e)
            if os.path.exists(path):
                return path
    return None

def play_song_by_path(path):
    try:
        with open(path, "rb") as f:
            st.audio(f.read(), format="audio/mp3")
    except Exception:
        st.error("Couldn't play the song file.")

# Confetti
def show_confetti():
    st.components.v1.html("""
    <canvas id='c' style='position:fixed;pointer-events:none;top:0;left:0;width:100%;height:100%;'></canvas>
    <script src='https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js'></script>
    <script>var myConfetti = confetti.create(document.getElementById('c'), { resize: true, useWorker: true });
           myConfetti({particleCount: 220, spread: 160, origin: {y:0.6}});</script>
    """, height=0)

# Typewriter display (JS) for message lines (safe short text)
def typewriter_html(msg, uid):
    safe = msg.replace("\n", "\\n").replace("'", "\\'")
    html = f"""
    <div class="typewriter"><span id="{uid}"></span></div>
    <script>
    const txt = '{safe}';
    const el = document.getElementById('{uid}');
    let i=0;
    function type(){ if(i<txt.length){ el.innerHTML += txt.charAt(i); i++; setTimeout(type, 20);} }
    type();
    </script>
    """
    return html

# ------------------ Page 1: Journey (with questions & songs) ------------------
def page_journey():
    st.markdown("<div class='page-header'>🌈 Journey — From Childhood to Today</div>", unsafe_allow_html=True)
    # Four questions already provided and answers prefilled
    for idx in range(1, ITEMS_PER_PAGE + 1):
        base = f"page1.{idx}"
        st.markdown("<div class='glow-box'>", unsafe_allow_html=True)
        # show question for slot idx
        question = QUESTIONS_PAGE1[idx - 1]
        st.markdown(f"<div style='font-weight:700; color:#c81d62; margin-bottom:6px;'>{question}</div>", unsafe_allow_html=True)
        key_input = f"p1_input_{idx}"
        key_submit = f"p1_submit_{idx}"
        key_reveal = f"p1_revealed_{idx}"
        user = st.text_input("", key=key_input, placeholder="Type answer and press Submit")
        if st.button("Submit", key=key_submit):
            if user.strip().lower() == ANSWERS_PAGE1[idx - 1].lower():
                st.session_state[key_reveal] = True
            else:
                st.error("Not quite — try again 🥺")
        # If revealed => show image + romantic message + song
        if st.session_state.get(key_reveal, False):
            img_path = find_image(base)
            if img_path:
                try:
                    img = Image.open(img_path)
                    img = ImageOps.exif_transpose(img)
                    st.image(img, use_column_width=True)
                except Exception:
                    st.error("Image found but couldn't be opened.")
            else:
                st.info(f"Place the image file named like images/{base}.jpg (or underscore variant)")
            # message (we will craft 4 special messages for page1)
            # Create beautiful lines per idx
            page1_messages = [
                "From your earliest days you shone — supercute doesn't cover your little miracle glow. Your eyes told stories before words did.",
                "Your bond with Ma is woven of lullabies, warmth and unending care. That love made you who you are — tender, strong and luminous.",
                "That red top moment — I remember how the world paused: that color met your glow and created a sun that day. Pure fire.",
                "Evening lights wrap your face like poetry. No one captures dusk the way you do — soft, radiant and unforgettable."
            ]
            msg = page1_messages[idx - 1]
            # typewriter effect
            html = typewriter_html(msg, f"p1_msg_{idx}")
            st.components.v1.html(html, height=80)
            # song: try SONG_SLOT_FILES mapping first, else try base name
            song_hint = SONG_SLOT_FILES[idx - 1] if idx - 1 < len(SONG_SLOT_FILES) else ""
            song_path = None
            if song_hint:
                candidate = os.path.join("songs", song_hint)
                if os.path.exists(candidate):
                    song_path = candidate
                else:
                    # try without extension variants
                    song_path = find_song(os.path.splitext(song_hint)[0])
            if not song_path:
                song_path = find_song(base)
            if song_path:
                play_song_by_path(song_path)
            else:
                st.info("No song found for this memory (place mp3 in songs/ with matching name).")
            # confetti celebration
            show_confetti()
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("")  # spacing

# ------------------ Pages 2,3,4 (auto messages & images, no questions) ------------------
def page_auto(page_no, title, messages_list):
    st.markdown(f"<div class='page-header'>{title}</div>", unsafe_allow_html=True)
    # show 4 images / messages: base names page{page_no}.1 .. page{page_no}.4
    for idx in range(1, ITEMS_PER_PAGE + 1):
        base = f"page{page_no}.{idx}"
        st.markdown("<div class='glow-box'>", unsafe_allow_html=True)
        img_path = find_image(base)
        if img_path:
            try:
                img = Image.open(img_path)
                img = ImageOps.exif_transpose(img)
                st.image(img, use_column_width=True)
            except Exception:
                st.error("Image found but couldn't be opened.")
        else:
            st.info(f"Place the image file named like images/{base}.jpg")
        # message
        msg = messages_list[idx - 1] if idx - 1 < len(messages_list) else "You are wonderful in every way."
        html = typewriter_html(msg, f"auto_{page_no}_{idx}")
        st.components.v1.html(html, height=80)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("")

# ------------------ Final letter page ------------------
def page_letter():
    st.markdown("<div class='page-header'>💌 My Last Message For You</div>", unsafe_allow_html=True)
    # play last song if available
    last_song_path = os.path.join("songs", LAST_SONG_FILE)
    if os.path.exists(last_song_path):
        play_song_by_path(last_song_path)
    else:
        st.info("Add songs/lastsong.mp3 to play a special song on this page.")
    st.markdown("""
    <div style='background:linear-gradient(180deg,#fff7fb,#fff1f6); padding:22px; border-radius:12px;
                box-shadow:0 8px 30px rgba(255,120,150,0.08); font-size:18px; color:#b81c5a;'>
    ❤️ If love had a shape, it would be the warmth in your smile.<br><br>
    🌙 Every moment with you becomes a favorite memory stitched with laughter.<br><br>
    ✨ You are not only breathtaking — your mind, your courage, your kindness make you rare and endlessly precious.<br><br>
    🎀 I love you more than words; I wish you galaxies on your birthday and always. Happy Birthday. 💖
    </div>
    """, unsafe_allow_html=True)

# ------------------ Main switch ------------------
page = st.session_state.get("page", "home")
if page == "home":
    # show big buttons again so user can choose from home if they navigated back
    c1, c2, c3, c4, c5 = st.columns([1,1,1,1,0.6])
    with c1:
        if st.button("🌈 Journey", key="hbtn_journey"): st.session_state.page = "journey"
    with c2:
        if st.button("✨ Qualities", key="hbtn_qualities"): st.session_state.page = "qualities"
    with c3:
        if st.button("💞 Memories", key="hbtn_memories"): st.session_state.page = "memories"
    with c4:
        if st.button("🌟 Future", key="hbtn_future"): st.session_state.page = "future"
    with c5:
        if st.button("💌 My Last Message", key="hbtn_letter"): st.session_state.page = "letter"

# Render the current selected page
if st.session_state.page == "journey":
    page_journey()
elif st.session_state.page == "qualities":
    page_auto(2, "✨ Qualities — The Magic You Carry", MESSAGES_PAGE2)
elif st.session_state.page == "memories":
    page_auto(3, "💞 Memories — Our Sweetest Moments", MESSAGES_PAGE3)
elif st.session_state.page == "future":
    page_auto(4, "🌟 Future — A Beautiful Tomorrow Awaits", MESSAGES_PAGE4)
elif st.session_state.page == "letter":
    page_letter()

# Back to home at bottom
st.markdown("<hr/>", unsafe_allow_html=True)
if st.button("⬅️ Back to Home"):
    st.session_state.page = "home"
