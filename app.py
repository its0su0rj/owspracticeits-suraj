# app.py
# Romantic interactive birthday website - final combined file
# Put images into ./images/ (names like page1.1.jpg OR page1_1.jpg)
# Put songs into ./songs/ (names like page1.1.mp3 OR page1_1.mp3). Also put songs/background.mp3 for soft ambient music.

import streamlit as st
from PIL import Image, ImageOps
import os, io, base64, random

# ---------- Config ----------
st.set_page_config(page_title="🎉 Happy Birthday", layout="wide")

# ---------- Editable content: QUESTIONS / ANSWERS / MESSAGES / SONG_HINTS ----------
# Each page: 1..4. Each list length must match ITEMS_PER_PAGE (4).
ITEMS_PER_PAGE = 4

QUESTIONS = {
    1: ["(Write question 1 for page 1)", "(Write question 2 for page 1)", "(Write question 3 for page 1)", "(Write question 4 for page 1)"],
    2: ["(Write question 1 for page 2)", "(Write question 2 for page 2)", "(Write question 3 for page 2)", "(Write question 4 for page 2)"],
    3: ["(Write question 1 for page 3)", "(Write question 2 for page 3)", "(Write question 3 for page 3)", "(Write question 4 for page 3)"],
    4: ["(Write question 1 for page 4)", "(Write question 2 for page 4)", "(Write question 3 for page 4)", "(Write question 4 for page 4)"],
}

# Exact answers (case-insensitive). Fill these or the app will tell you to configure the slot.
ANSWERS = {
    1: ["ans1", "ans2", "ans3", "ans4"],
    2: ["ans1", "ans2", "ans3", "ans4"],
    3: ["ans1", "ans2", "ans3", "ans4"],
    4: ["ans1", "ans2", "ans3", "ans4"],
}

# Messages shown after correct answer (rich romantic lines allowed)
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

# Song hints (optional). If left blank, the app will try to auto-find songs named as pageX.Y.mp3 or pageX_Y.mp3
SONG_HINTS = {
    1: ["page1.1.mp3", "page1.2.mp3", "page1.3.mp3", "page1.4.mp3"],
    2: ["page2.1.mp3", "page2.2.mp3", "page2.3.mp3", "page2.4.mp3"],
    3: ["page3.1.mp3", "page3.2.mp3", "page3.3.mp3", "page3.4.mp3"],
    4: ["page4.1.mp3", "page4.2.mp3", "page4.3.mp3", "page4.4.mp3"],
}

# ---------- Styling & Animations (heartbeat, glow, hearts, sparkles, typewriter, fade-in) ----------
st.markdown("""
<style>
/* Page headings */
.main-title {text-align:center; font-size:44px; color:#ff2d6f; font-weight:900; margin-bottom:4px;}
.subtitle {text-align:center; font-size:18px; color:#ff8fab; margin-bottom:18px;}

/* Button style + heartbeat pulse + glow on hover */
button[kind="secondary"], button[kind="primary"], .stButton>button {
    animation: heartbeat 1.6s infinite;
    border-radius: 14px !important;
    font-weight: 700 !important;
    padding: 0.6rem 1.1rem !important;
    font-size: 1.05rem !important;
    transition: box-shadow 0.25s ease, transform 0.15s ease;
    box-shadow: 0 6px 18px rgba(255,77,109,0.12);
}
.stButton>button:hover {
    box-shadow: 0 10px 30px rgba(255,50,90,0.22) !important;
    transform: translateY(-3px);
}

@keyframes heartbeat {
  0% { transform: scale(1); box-shadow: 0 0 0 rgba(255,0,90,0.0);}
  25% { transform: scale(1.06); box-shadow: 0 0 12px rgba(255,0,90,0.08);}
  40% { transform: scale(0.98); }
  60% { transform: scale(1.03); box-shadow: 0 0 18px rgba(255,0,90,0.12);}
  100% { transform: scale(1); box-shadow: 0 0 0 rgba(255,0,90,0.0);}
}

/* Floating hearts */
@keyframes floatHeart { 0% {transform: translateY(0) scale(0.9); opacity: 1;} 50% {transform: translateY(-60px) scale(1.1); opacity: 0.8;} 100% {transform: translateY(-120px) scale(0.8); opacity: 0;} }
.heart-container {position: fixed; bottom: 10px; left: 50%; transform: translateX(-50%); z-index: 9999; pointer-events: none;}
.heart { position: absolute; font-size: 28px; color: #ff4d6d; animation: floatHeart 3.2s linear infinite; }

/* Falling sparkles */
@keyframes fallSparkle { 0% {transform: translateY(-10vh) scale(0.5); opacity: 0;} 40% {opacity: 1;} 100% {transform: translateY(100vh) scale(1); opacity: 0;} }
.sparkle { position: fixed; top: -10px; left: 50%; font-size: 20px; color: #ffd6e8; animation: fallSparkle 6s linear infinite; z-index: 9998; pointer-events: none; }
.sparkle:nth-child(2) { left: 30%; animation-delay: 1.5s; }
.sparkle:nth-child(3) { left: 70%; animation-delay: 3s; }
.sparkle:nth-child(4) { left: 20%; animation-delay: 4.2s; }
.sparkle:nth-child(5) { left: 80%; animation-delay: 5.1s; }

/* Glow border for reveal boxes */
.glow-box { border: 2px solid #ff4d6d; border-radius: 14px; padding: 14px; animation: glowPulse 2.7s ease-in-out infinite; background: linear-gradient(180deg,#fff7fb,#fff1f6); box-shadow: 0 10px 30px rgba(255,77,109,0.06); }
@keyframes glowPulse { 0% { box-shadow: 0 0 10px rgba(255,77,109,0.18);} 50% { box-shadow: 0 0 26px rgba(255,50,90,0.28);} 100% { box-shadow: 0 0 10px rgba(255,77,109,0.18);} }

/* Fade-in for revealed image */
.fade-in { animation: fadeIn 0.9s ease-in-out; }
@keyframes fadeIn { from {opacity:0; transform: translateY(6px);} to {opacity:1; transform: translateY(0);} }

/* Typewriter for message text */
.typewriter { overflow: hidden; white-space: nowrap; border-right: .12em solid rgba(200,30,90,0.6); font-size:18px; color:#c81d62; font-weight:700; }
@keyframes typing { from { width: 0 } to { width: 100% } }
@keyframes blinkCaret { 50% { border-color: transparent; } }

/* make the typewriter effect container */
.typewriter-inner { display: inline-block; }

/* small polish */
.page-header { text-align:center; font-size:30px; color:#ff3b6b; margin-top:8px; margin-bottom:12px; font-weight:800; }
.question-label { font-weight:700; color:#c81d62; margin-bottom:6px; }
</style>

<!-- hearts and sparkles markup -->
<div class='heart-container'>
  <div class='heart' style='left:-90px; animation-delay:0s;'>❤️</div>
  <div class='heart' style='left:-30px; animation-delay:0.6s;'>💗</div>
  <div class='heart' style='left:30px; animation-delay:1.2s;'>💕</div>
  <div class='heart' style='left:90px; animation-delay:1.8s;'>💖</div>
</div>

<div class='sparkle'>✨</div>
<div class='sparkle'>❄️</div>
<div class='sparkle'>🌟</div>
<div class='sparkle'>✨</div>
<div class='sparkle'>💫</div>
""", unsafe_allow_html=True)

# ---------- Soft background music (autoplay loop) ----------
def inject_background_music(path="songs/background.mp3"):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        audio_html = f"""
        <audio autoplay loop style="position: fixed; bottom: 16px; left: 16px; width: 260px; z-index:9999; opacity:0.92;" controls>
            <source src="data:audio/mp3;base64,{data}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

# call it (will silently do nothing if file missing)
inject_background_music()

# ---------- Header ----------
st.markdown("<div class='main-title'>🎉 Happy Birthday! 🎉</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>A little interactive journey — unlock images, messages & songs ✨</div>", unsafe_allow_html=True)

# ---------- Page navigation (big colorful buttons on homepage) ----------
if 'page' not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    c1, c2, c3, c4, c5 = st.columns([1,1,1,1,0.6])
    with c1:
        if st.button("🌈 Journey", key="btn_journey"):
            st.session_state.page = "journey"
    with c2:
        if st.button("✨ Qualities", key="btn_qualities"):
            st.session_state.page = "qualities"
    with c3:
        if st.button("💞 Memories", key="btn_memories"):
            st.session_state.page = "memories"
    with c4:
        if st.button("🌟 Future", key="btn_future"):
            st.session_state.page = "future"
    with c5:
        if st.button("💌 My Last Message", key="btn_letter"):
            st.session_state.page = "letter"

# ---------- Utilities: locate image or song with flexible naming ----------
def find_image(base_name):
    # try base_name with dot and underscore and multiple extensions
    candidates = [
        os.path.join("images", base_name + ".jpg"),
        os.path.join("images", base_name + ".jpeg"),
        os.path.join("images", base_name + ".png"),
        os.path.join("images", base_name + ".webp"),
        os.path.join("images", base_name.replace('.', '_') + ".jpg"),
        os.path.join("images", base_name.replace('.', '_') + ".jpeg"),
        os.path.join("images", base_name.replace('.', '_') + ".png"),
        os.path.join("images", base_name.replace('.', '_') + ".webp"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

def find_song(base_name):
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

# Confetti display (canvas-confetti)
def show_confetti():
    st.components.v1.html("""
    <canvas id='c' style='position:fixed;pointer-events:none;top:0;left:0;width:100%;height:100%;'></canvas>
    <script src='https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js'></script>
    <script>
      var myConfetti = confetti.create(document.getElementById('c'), { resize: true, useWorker: true });
      myConfetti({particleCount: 220, spread: 160, origin: {y:0.6}});
    </script>
    """, height=0)

# ---------- Reveal block: question -> reveal image + message + song ----------
def render_reveal_block(page_no, item_no):
    """
    Each slot uses session_state to persist revelation.
    base file name: page{page_no}.{item_no}
    """
    base = f"page{page_no}.{item_no}"
    q_text = QUESTIONS.get(page_no, [""]*ITEMS_PER_PAGE)[item_no-1]
    correct = ANSWERS.get(page_no, [""]*ITEMS_PER_PAGE)[item_no-1]
    message = MESSAGES.get(page_no, [""]*ITEMS_PER_PAGE)[item_no-1]
    song_hint = SONG_HINTS.get(page_no, [""]*ITEMS_PER_PAGE)[item_no-1]

    key_input = f"input_p{page_no}_{item_no}"
    key_submit = f"submit_p{page_no}_{item_no}"
    key_revealed = f"revealed_p{page_no}_{item_no}"

    st.markdown("<div class='glow-box'>", unsafe_allow_html=True)
    st.markdown(f"<div class='question-label'>🔒 Unlock this memory</div>", unsafe_allow_html=True)
    st.write(q_text)

    user = st.text_input("", key=key_input, placeholder="Type your answer and press Submit")
    if st.button("Submit", key=key_submit):
        if correct.strip() == "":
            st.warning("This slot isn't configured yet. Please fill ANSWERS in the top of app.py.")
        elif user.strip().lower() == correct.strip().lower():
            st.session_state[key_revealed] = True
        else:
            st.error("Not quite — try again 💫")

    # If revealed -> show content
    if st.session_state.get(key_revealed, False):
        # image
        img_path = find_image(base)
        if img_path:
            try:
                img = Image.open(img_path)
                img = ImageOps.exif_transpose(img)
                st.image(img, use_column_width=True, caption=None, output_format="JPEG")
                # small fade-in helper: insert CSS class by wrapping in HTML (Streamlit images don't accept class directly)
                # show message below with typewriter effect
            except Exception:
                st.error("Image found but couldn't be opened.")
        else:
            st.info(f"Image not found: images/{base}.jpg (or try underscore variant).")

        # typewriter message
        # We'll render the message using JS to animate typing
        typed_html = f"""
        <div style="margin-top:8px;">
          <span class='typewriter'>
            <span id='tw_{page_no}_{item_no}' class='typewriter-inner'></span>
          </span>
        </div>
        <script>
        const msg = {repr(message)};
        const el = document.getElementById('tw_{page_no}_{item_no}');
        // simple typewriter
        (function typeWriter(text, element, i, speed){
            if (i < text.length) {{
                element.innerHTML += text.charAt(i);
                setTimeout(function(){{ typeWriter(text, element, i+1, speed); }}, speed);
            }} else {{
                // blink caret stop after finish
                element.parentNode.style.borderRight = '0px';
            }}
        }})(msg, el, 0, 20);
        </script>
        """
        st.components.v1.html(typed_html, height=80)

        # play song if found
        song_path = None
        # prefer explicit hint if exists
        if song_hint and song_hint.strip() != "":
            s_candidate = song_hint
            # if hint has no path, check songs/...
            if os.path.exists(os.path.join("songs", s_candidate)):
                song_path = os.path.join("songs", s_candidate)
            else:
                # try find song by base name of hint
                base_hint = os.path.splitext(s_candidate)[0]
                song_path = find_song(base_hint)
        if not song_path:
            song_path = find_song(base)

        if song_path:
            try:
                with open(song_path, "rb") as f:
                    audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/mp3")
            except Exception:
                st.error("Song found but couldn't be played.")
        else:
            st.info("No song found for this memory (place mp3 in songs/).")

        # celebrate
        show_confetti()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("")  # spacing

# ---------- Page renderers ----------
def render_two_col_layout(page_no, title_line):
    st.markdown(f"<div class='page-header'>{title_line}</div>", unsafe_allow_html=True)
    # show 2 columns with two reveal blocks each (for 4 items)
    cols = st.columns(2)
    idx = 0
    for c in cols:
        with c:
            # show two items per column
            for i in range(ITEMS_PER_PAGE // 2):
                idx += 1
                render_reveal_block(page_no, idx)

# main page switching
if st.session_state.page == "journey":
    render_two_col_layout(1, "🌈 Journey — From Little Steps to Beautiful Love")

elif st.session_state.page == "qualities":
    render_two_col_layout(2, "✨ Qualities — The Magic You Carry")

elif st.session_state.page == "memories":
    render_two_col_layout(3, "💞 Memories — These Moments Live Forever")

elif st.session_state.page == "future":
    render_two_col_layout(4, "🌟 Future — A Beautiful Tomorrow Awaits")

elif st.session_state.page == "letter":
    st.markdown("<div class='page-header'>💌 My Last Message For You</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:linear-gradient(180deg,#fff7fb,#fff1f6); padding:22px; border-radius:12px;
                box-shadow:0 8px 30px rgba(255,120,150,0.08); font-size:18px; color:#b81c5a;'>
    💖 Sometimes words fall short, but feelings don't.<br><br>
    💫 If I could capture every emotion I feel for you, the sky would run out of stars.<br><br>
    🌷 You are not just a part of my life — you are the softest chapter, the sweetest page.<br><br>
    🌙 I wish your birthday brings endless smiles, warm hugs, and moments that feel like magic.
    </div>
    """, unsafe_allow_html=True)

# Back to home (persistent)
st.markdown("<hr/>", unsafe_allow_html=True)
if st.button("⬅️ Back to Home"):
    st.session_state.page = "home"

# End of file
