"""
app.py

4-page Streamlit Birthday Wish website (single-file).
Pages:
 1) Journey — timeline (images/ + optional captions.csv)
 2) Qualities — editable cards highlighting her strengths
 3) Memories — gallery with enlarged view + download ZIP
 4) Future — vision board, wishes, e-card generator

How to use:
 - Place ~50 images in ./images/ (use numeric prefixes to control order)
 - Optional captions.csv with columns: filename,date,caption,section
 - Install: pip install streamlit pillow pandas
 - Run: streamlit run app.py

Notes:
 - This file is intentionally self-contained and focuses on speed and simplicity so you can finish in 4 hours.
"""

import streamlit as st
from PIL import Image, ImageOps
import os, glob, io, zipfile, base64, random
import pandas as pd

# ---------- Page config ----------
st.set_page_config(page_title="Happy Birthday 💖", layout="wide")

# ---------- Constants ----------
IMAGE_DIR = "images"
SUPPORTED = ("*.jpg","*.jpeg","*.png","*.webp")

# ---------- Helpers ----------

def natural_key(s):
    import re
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", s)]


def load_images():
    paths = []
    for pat in SUPPORTED:
        paths.extend(glob.glob(os.path.join(IMAGE_DIR, pat)))
    return sorted(paths, key=natural_key)


def load_captions(path="captions.csv"):
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            df['filename'] = df['filename'].astype(str)
            return df.set_index('filename').to_dict(orient='index')
        except Exception as e:
            st.warning(f"Couldn't read captions.csv: {e}")
    return {}


def image_bytes(path_or_file, max_size=(1200,1200)):
    if hasattr(path_or_file, 'read'):
        img = Image.open(path_or_file)
    else:
        img = Image.open(path_or_file)
    img = ImageOps.exif_transpose(img)
    img.thumbnail(max_size)
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=85)
    return buf.getvalue()


def make_zip(paths, captions_map=None):
    b = io.BytesIO()
    with zipfile.ZipFile(b, 'w') as z:
        for p in paths:
            if hasattr(p, 'read'):
                p.seek(0)
                z.writestr(p.name, p.read())
            else:
                z.write(p, arcname=os.path.basename(p))
        if captions_map:
            df = pd.DataFrame.from_dict(captions_map, orient='index')
            z.writestr('captions.csv', df.to_csv(index_label='filename'))
    b.seek(0)
    return b


def b64_image_for_html(bts):
    return base64.b64encode(bts).decode('utf-8')

# ---------- UI bits ----------

def header(name):
    st.markdown(f"<div style='display:flex;align-items:center;gap:16px'>"
                f"<div style='font-size:40px;font-weight:800;color:#ff2d6f'>🎉 Happy Birthday, {name}!</div>"
                f"</div>", unsafe_allow_html=True)
    st.markdown("<hr/>", unsafe_allow_html=True)


def confetti():
    st.components.v1.html("""
    <canvas id='c' style='position:fixed;pointer-events:none;top:0;left:0;width:100%;height:100%;'></canvas>
    <script src='https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js'></script>
    <script>
    var myConfetti = confetti.create(document.getElementById('c'), { resize: true, useWorker: true });
    myConfetti({particleCount: 300, spread: 150, origin: {y:0.6}});
    </script>
    """, height=0)

# ---------- Load data ----------
paths = load_images()
captions_map = load_captions()

# ---------- Sidebar ----------
st.sidebar.title("Build & Preview")
name = st.sidebar.text_input("Display name (on header)", value="My Love")
page = st.sidebar.radio("Page", ["Journey","Qualities","Memories","Future"]) 
music = st.sidebar.file_uploader("Optional: background music (mp3)", type=['mp3'])
order = st.sidebar.selectbox("Image order", ["filename","reverse","random"], index=0)
show_dates = st.sidebar.checkbox("Show dates if available", True)
auto_caption = st.sidebar.checkbox("Auto-generate captions from filenames", value=True)

if order == 'reverse':
    paths = list(reversed(paths))
elif order == 'random':
    random.shuffle(paths)

if music:
    st.audio(music.read())

# ---------- Pages ----------

if page == 'Journey':
    header(name)
    st.markdown("### Her Journey — Childhood to Today")
    st.write("A timeline that tells the story. Arrange files with numeric prefixes (001_, 002_...).")

    if not paths:
        st.warning("No images found in ./images. Upload images or create the folder and add photos.")
        uploaded = st.file_uploader("Quick upload images to preview (multiple)", accept_multiple_files=True, type=['png','jpg','jpeg','webp'])
        if uploaded:
            paths = uploaded

    for i,p in enumerate(paths):
        if hasattr(p, 'name'):
            fname = p.name
        else:
            fname = os.path.basename(p)
        meta = captions_map.get(fname, {})
        caption = meta.get('caption','') or (os.path.splitext(fname)[0].replace('_',' ').title() if auto_caption else '')
        date = meta.get('date','')
        img_bts = image_bytes(p, max_size=(1000,1000))

        left = (i % 2 == 0)
        if left:
            c1,c2 = st.columns([1,2])
            with c1:
                st.image(img_bts, use_column_width=True)
            with c2:
                st.markdown(f"**{caption}**")
                if show_dates and date:
                    st.markdown(f"*{date}*")
                st.write("\n")
        else:
            c1,c2 = st.columns([2,1])
            with c1:
                st.markdown(f"**{caption}**")
                if show_dates and date:
                    st.markdown(f"*{date}*")
                st.write("\n")
            with c2:
                st.image(img_bts, use_column_width=True)

    st.markdown('---')
    col1,col2 = st.columns(2)
    with col1:
        if st.button('Download ZIP of Journey'):
            if not paths:
                st.warning('No images to zip')
            else:
                b = make_zip(paths, captions_map)
                st.download_button('Download', data=b, file_name='journey_images.zip')
    with col2:
        if st.button('Surprise Confetti'):
            confetti()


elif page == 'Qualities':
    header(name)
    st.markdown("### Her Qualities & Capabilities")
    st.write("Write short heartfelt qualities and display them as elegant cards.")

    # simple form to collect 6 qualities
    with st.form('qualities'):
        cols = st.columns(2)
        q = []
        for i in range(6):
            title = cols[i%2].text_input(f'Quality {i+1} (title)', value=("Kind" if i==0 else ""), key=f'qtitle_{i}')
            note = cols[i%2].text_input(f'Note {i+1}', value=("Always supports everyone." if i==0 else ""), key=f'qnote_{i}')
            q.append((title,note))
        submitted = st.form_submit_button('Save Qualities')

    # render cards
    grid = st.columns(3)
    for i,(title,note) in enumerate(q):
        with grid[i%3]:
            st.markdown("<div style='padding:18px;border-radius:12px;background:white;box-shadow:0 6px 18px rgba(0,0,0,0.06)'>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:36px'>🌟</div>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='margin:6px 0'>{title}</h3>", unsafe_allow_html=True)
            st.write(note)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('---')
    st.write('Add a short personal wish to show when pressing the button below:')
    personal = st.text_area('Your message', value=f'Happy Birthday, {name}! You mean the world to me. ❤️')
    if st.button('Reveal Wish & Confetti'):
        confetti()
        st.success(personal)


elif page == 'Memories':
    header(name)
    st.markdown('### Memories — Gallery')
    st.write('Browse the photo gallery. Click a thumbnail to view larger in a popup-like frame.')

    if not paths:
        st.warning('No images found. Upload images to ./images or use the uploader below to test.')
        uploaded = st.file_uploader('Upload images (multiple)', accept_multiple_files=True, type=['png','jpg','jpeg','webp'])
        if uploaded:
            paths = uploaded

    per_row = st.slider('Thumbnails per row', 3, 6, 4)
    idx = 0
    while idx < len(paths):
        row_cols = st.columns(per_row)
        for col in row_cols:
            if idx >= len(paths): break
            p = paths[idx]
            fname = p.name if hasattr(p,'name') else os.path.basename(p)
            bts = image_bytes(p, max_size=(600,600))
            # show image and a button to open larger view
            with col:
                st.image(bts, use_column_width=True)
                if st.button('View', key=f'view_{idx}'):
                    html = f"<div style='text-align:center'>"
                    html += f"<img src='data:image/jpeg;base64,{b64_image_for_html(bts)}' style='max-width:90%;height:auto;border-radius:12px'/>"
                    cap = captions_map.get(fname, {}).get('caption','')
                    date = captions_map.get(fname, {}).get('date','')
                    if cap: html += f"<h3>{cap}</h3>"
                    if date and show_dates: html += f"<p><em>{date}</em></p>"
                    html += "</div>"
                    st.components.v1.html(html, height=600)
            idx += 1

    st.markdown('---')
    if st.button('Download Memories ZIP'):
        if not paths:
            st.warning('No images to download')
        else:
            b = make_zip(paths, captions_map)
            st.download_button('Download memories.zip', data=b, file_name='memories.zip')


elif page == 'Future':
    header(name)
    st.markdown('### Future — Vision Board & E-card')
    st.write('Write wishes, pick colors, generate a shareable e-card and playful predictions.')

    col1,col2 = st.columns([2,1])
    with col1:
        w1 = st.text_input('Wish 1', 'May you keep smiling and achieving your dreams')
        w2 = st.text_input('Wish 2', 'May love and success follow you always')
        w3 = st.text_input('Wish 3', 'Travel, health and happiness')

        yrs = st.slider('Imagine after how many years', 1, 10, 5)
        if st.button('Generate playful prediction'):
            words = ['creativity','compassion','leadership','adventure','wisdom','joy']
            pick = ', '.join(random.sample(words, 3))
            st.success(f'In {yrs} years: A blend of {pick} and a new hobby that lights her up!')

    with col2:
        color = st.color_picker('E-card background', '#fff0f6')
        sender = st.text_input('Signature', 'With love, Yours')
        if st.button('Create E-card'):
            html = f"<div style='padding:30px;border-radius:18px;background:{color};text-align:center'>"
            html += f"<h1>Happy Birthday, {name} 🎉</h1>"
            html += f"<p>{w1}<br/>{w2}<br/>{w3}</p>"
            html += f"<p style='margin-top:20px; font-weight:700'>{sender}</p></div>"
            st.components.v1.html(html, height=360)
            st.download_button('Download E-card (HTML)', data=html.encode('utf-8'), file_name='ecard.html')

    st.markdown('---')
    if st.button('Final Surprise: Confetti & Balloons'):
        confetti()
        st.balloons()

# ---------- Footer ----------

st.markdown('<hr/>', unsafe_allow_html=True)
st.caption('Made with ❤️ — edit app.py to adjust styles, messages and images')
