# app.py
# Streamlit - Romantic Birthday Interactive Site (clean rewrite)
# Usage:
#  - Place images in ./images/ named like: page1.1.jpg, page1.2.jpg ... page4.4.jpg
#  - Place optional songs in ./songs/ named like: page1.1.mp3 OR page1_1.mp3
#  - Edit the QUESTIONS / ANSWERS / MESSAGES / SONG_FILES dictionaries below to customize
#  - Run: pip install streamlit pillow
#         streamlit run app.py

import streamlit as st
from PIL import Image, ImageOps
import os
import io
import base64

# ---------- CONFIG ----------
st.set_page_config(page_title="🎉 Happy Birthday", layout="wide")

# Number of items per page (4 as requested)
ITEMS_PER_PAGE = 4

# --- Customize these dictionaries: (you will replace strings/questions/answers/messages/songs) --- #
# Keys: page numbers 1..4. Each value is a list of length ITEMS_PER_PAGE

QUESTIONS = {
    1: ["(write question 1 here)", "(question 2)", "(question 3)", "(question 4)"],
    2: ["(write question 1 here)", "(question 2)", "(question 3)", "(question 4)"],
    3: ["(write question 1 here)", "(question 2)", "(question 3)", "(question 4)"],
    4: ["(write question 1 here)", "(question 2)", "(question 3)", "(question 4)"],
}

# Correct answers for each question (user will enter them in the app when testing / or pre-fill here)
ANSWERS = {
    1: ["ans1", "ans2", "ans3", "ans4"],
    2: ["ans1", "ans2", "ans3", "ans4"],
    3: ["ans1", "ans2", "ans3", "ans4"],
    4: ["ans1", "ans2", "ans3", "ans4"],
}

# Messages to reveal after correct answer (romantic text)
MESSAGES = {
    1: [
        "💖 This moment was unforgettable — you light up my world.",
        "🌸 Your smile in this memory is my favorite view.",
        "✨ Every little thing you do is magic.",
        "🌙 With you every night feels like a dream."
    ],
    2: [
        "🌟 Your kindness heals and inspires.",
        "🔥 Your courage is breathtaking.",
        "💫 Your laughter is my favorite sound.",
        "🌈 You make ordinary days extraordinary."
    ],
    3: [
        "📷 This memory holds a thousand smiles.",
        "🎁 I keep this day in my heart forever.",
        "🍃 Gentle winds carried us into that sunlit moment.",
        "☕ Late night talks, warm hugs — I treasure it all."
    ],
    4: [
        "🚀 The future with you is bright and infinite.",
        "🌼 I see joy, travel, success and us together.",
        "🏡 A home filled with love, laughter, and soft mornings.",
        "💍 I hope the best years are still ahead for you."
    ],
}

# Song filenames (without folder). The code will try variations like "page1.1.mp3" or "page1_1.mp3"
# Put the mp3 files inside ./songs/
SONG_FILES = {
    1: ["page1.1.mp3", "page1.2.mp3", "page1.3.mp3", "page1.4.mp3"],
    2: ["page2.1.mp3", "page2.2.mp3", "page2.3.mp3", "page2.4.mp3"],
    3: ["page3.1.mp3", "page3.2.mp3", "page3.3.mp3", "page3.4.mp3"],
    4: ["page4.1.mp3", "page4.2.mp3", "page4.3.mp3", "page4.4.mp3"],
}
# ----------------------------------------------------------------------------------------------- #

# ---------- Styling ----------
st.markdown(
    """
    <style>
    .main-title {text-align:center; font-size:44px; color:#ff2d6f; font-weight:900;}
    .subtitle {text-align:center; font-size:18px; color:#ff8fab; margin-bottom:18px;}
    .btn-card {background: linear-gradient(135deg,#ffecd2,#fcb6d1); padding:18px; border-radius:14px; text-align:center;
              box-shadow: 0 8px 24px rgba(255,100,150,0.12); font-weight:700; font-size:20px;}
    .page-header {text-align:center; font-size:30px; color:#ff3b6b; margin-top:8px; margin-bottom:12px; font-weight:800;}
    .reveal-box {background:linear-gradient(180deg,#fff7fb,#fff1f6); padding:14px; border-radius:12px;
                 box-shadow: 0 6px 18px rgba(255,120,150,0.08);}
    .question-label {font-weight:700; color:#c81d62;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='main-title'>🎉 Happy Birthday! 🎉</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>A little interactive journey — unlock images, messages & songs ✨</div>", unsafe_allow_html=True)

# ---------- Homepage big buttons ----------
cols = st.columns([1,1,1,1,0.4])  # last column small spacer for the 'My Last Message' button later
if 'page' not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    c1, c2, c3, c4, c5 = cols
    if c1.button("🌈 Journey", key="btn_journey"):
        st.session_state.page = "journey"
    if c2.button("✨ Qualities", key="btn_qualities"):
        st.session_state.page = "qualities"
    if c3.button("💞 Memories", key="btn_memories"):
        st.session_state.page = "memories"
    if c4.button("🌟 Future", key="btn_future"):
        st.session_state.page = "future"
    # extra button (rightmost)
    if c5.button("💌 My Last Message", key="btn_last"):
        st.session_state.page = "letter"

# Utility: find an image file for a base name like "page1.1" with supported extensions
def find_image_file(base_name):
    exts = [".jpg", ".jpeg", ".png", ".webp"]
    for ext in exts:
        p = os.path.join("images", base_name + ext)
        if os.path.exists(p):
            return p
    return None

# Utility: find song file; support "page1.1.mp3" or "page1_1.mp3"
def find_song_file(base_name):
    # try exact base_name (with .mp3) then underscore variant
    candidates = [
        os.path.join("songs", base_name + ".mp3"),
        os.path.join("songs", base_name.replace('.', '_') + ".mp3"),
        os.path.join("songs", base_name + ".wav"),
        os.path.join("songs", base_name.replace('.', '_') + ".wav"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

# Small confetti (HTML+canvas-confetti) — only triggered manually via function
def show_confetti():
    st.components.v1.html(
        """<canvas id='c' style='position:fixed;pointer-events:none;top:0;left:0;width:100%;height:100%;'></canvas>
           <script src='https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js'></script>
           <script>var myConfetti = confetti.create(document.getElementById('c'), { resize: true, useWorker: true });
           myConfetti({particleCount: 200, spread: 140, origin: {y:0.6}});</script>""",
        height=0,
    )

# Function to render a single reveal block (question -> reveal image+message+song on correct)
def render_reveal_block(page_no: int, item_no: int):
    """
    page_no: 1..4
    item_no: 1..ITEMS_PER_PAGE
    """
    base_name = f"page{page_no}.{item_no}"  # expected image base name
    q_text = QUESTIONS.get(page_no, [""] * ITEMS_PER_PAGE)[item_no-1]
    correct = ANSWERS.get(page_no, [""] * ITEMS_PER_PAGE)[item_no-1]
    message = MESSAGES.get(page_no, [""] * ITEMS_PER_PAGE)[item_no-1]
    song_hint = SONG_FILES.get(page_no, [""] * ITEMS_PER_PAGE)[item_no-1]

    # Unique keys to preserve states
    input_key = f"input_p{page_no}_{item_no}"
    submit_key = f"submit_p{page_no}_{item_no}"
    revealed_key = f"revealed_p{page_no}_{item_no}"

    st.markdown("<div class='reveal-box'>", unsafe_allow_html=True)

    # Show the question area (user will replace q_text in dict above)
    # Use placeholder instead of label-only white bar
    st.markdown(f"<div class='question-label'>🔒 Unlock this memory</div>", unsafe_allow_html=True)
    st.write(q_text)  # this is where you will write the actual question text in QUESTIONS dict

    # Input for answer — placeholder makes it visually cleaner
    user_ans = st.text_input("Type your answer here:", key=input_key, placeholder="Type answer and press Submit")

    if st.button("Submit", key=submit_key):
        # store correctness in session_state to keep revealed after reruns
        if user_ans.strip().lower() == correct.strip().lower() and correct.strip() != "":
            st.session_state[revealed_key] = True
        else:
            # if correct string is empty (user hasn't filled ANSWERS) then treat any non-empty as incorrect but remind
            if correct.strip() == "":
                st.warning("This slot isn't configured yet. Put the correct answer into the app's QUESTIONS/ANSWERS dict.")
            else:
                st.error("Not quite — try again 💫")

    # If already revealed, show image+message+song
    if st.session_state.get(revealed_key, False):
        # Image
        imgfile = find_image_file(base_name)
        if imgfile:
            try:
                img = Image.open(imgfile)
                img = ImageOps.exif_transpose(img)
                st.image(img, use_column_width=True)
            except Exception as e:
                st.error("Image found but couldn't open it.")
        else:
            st.info(f"Image not found: images/{base_name}.jpg (place file there)")

        # Romantic message (styled)
        st.markdown(f"<div style='font-size:18px; color:#c81d62; font-weight:700; margin-top:8px;'>{message}</div>", unsafe_allow_html=True)

        # Song (if present)
        # Try provided SONG_FILES filename first, else try default name base_name
        song_path = None
        # prefer song listed in SONG_FILES mapping (if file exists)
        if song_hint:
            # if song_hint provided with extension, check as is
            if os.path.exists(os.path.join("songs", song_hint)):
                song_path = os.path.join("songs", song_hint)
            else:
                # maybe the mapping omitted extension or used dot vs underscore; try find_song_file
                song_path = find_song_file(song_hint.replace(".mp3", "").replace(".wav", ""))
        if not song_path:
            song_path = find_song_file(base_name)

        if song_path:
            try:
                with open(song_path, "rb") as f:
                    audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/mp3")
            except Exception as e:
                st.error("Song found but couldn't be played.")
        else:
            st.info("No song found for this memory (put mp3 in songs/).")

        # Confetti to celebrate correct answer (small)
        show_confetti()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("")  # separation

# ---------- Page rendering ----------
def render_page(page_name):
    st.markdown(f"<div class='page-header'>{page_name}</div>", unsafe_allow_html=True)

    # Render ITEMS_PER_PAGE reveal blocks in two-column layout
    cols = st.columns(2)
    # We'll show 2 blocks per column (so 4 total)
    idx = 0
    for col in cols:
        with col:
            for i in range(ITEMS_PER_PAGE // 2):
                idx += 1
                render_reveal_block(render_page.NUM, idx)

# Attach attribute to function for current numeric page id
render_page.NUM = 1

if st.session_state.page == "journey":
    render_page.NUM = 1
    render_page("🌈 Journey — beautiful little steps")

elif st.session_state.page == "qualities":
    render_page.NUM = 2
    render_page("✨ Qualities — the magic you carry")

elif st.session_state.page == "memories":
    render_page.NUM = 3
    render_page("💞 Memories — our sweet little world")

elif st.session_state.page == "future":
    render_page.NUM = 4
    render_page("🌟 Future — the beautiful tomorrow")

elif st.session_state.page == "letter":
    st.markdown("<div class='page-header'>💌 My Last Message For You</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='background:linear-gradient(180deg,#fff7fb,#fff1f6); padding:22px; border-radius:12px;
                    box-shadow:0 8px 30px rgba(255,120,150,0.08); font-size:18px; color:#b81c5a;'>
        💖 Sometimes words fall short, but feelings don't.<br><br>
        💫 If I could capture every emotion I feel for you, the sky would run out of stars.<br><br>
        🌷 You are not just a part of my life — you are the softest chapter, the sweetest page.<br><br>
        🌙 I wish your birthday brings endless smiles, warm hugs, and moments that feel like magic.
        </div>
        """,
        unsafe_allow_html=True,
    )

# Back to home button at bottom
st.markdown("<hr/>", unsafe_allow_html=True)
if st.button("⬅️ Back to Home"):
    st.session_state.page = "home"
    # optionally reset revealed state if you want:
    # for p in range(1,5):
    #    for i in range(1, ITEMS_PER_PAGE+1):
    #        key = f"revealed_p{p}_{i}"
    #        st.session_state[key] = False
