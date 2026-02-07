import streamlit as st

st.set_page_config(page_title="Valentine 💖", page_icon="💘", layout="centered")

st.markdown(
    """
    <style>
    body {
        background-color: #ffe6ee;
    }

    .container {
        background: white;
        padding: 40px;
        border-radius: 20px;
        width: 350px;
        margin: auto;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        font-family: 'Arial', sans-serif;
    }

    .title {
        font-size: 24px;
        margin-bottom: 30px;
        font-weight: bold;
    }

    .btn-yes {
        background-color: #ff4d6d;
        color: white;
        border: none;
        padding: 12px 30px;
        font-size: 18px;
        border-radius: 30px;
        cursor: pointer;
        margin-right: 20px;
    }

    .btn-no {
        background-color: #cccccc;
        color: black;
        border: none;
        padding: 12px 30px;
        font-size: 18px;
        border-radius: 30px;
        cursor: pointer;
        position: absolute;
    }
    </style>

    <div class="container">
        <div class="title">Will you be my Valentine? 💕</div>

        <button class="btn-yes" onclick="alert('YAY!!! 💖🥰')">
            Yes
        </button>

        <button class="btn-no" id="noBtn">
            No
        </button>
    </div>

    <script>
    const noBtn = document.getElementById("noBtn");

    noBtn.addEventListener("mouseover", () => {
        const x = Math.random() * (window.innerWidth - 100);
        const y = Math.random() * (window.innerHeight - 100);

        noBtn.style.left = `${x}px`;
        noBtn.style.top = `${y}px`;
    });
    </script>
    """,
    unsafe_allow_html=True
)                        
