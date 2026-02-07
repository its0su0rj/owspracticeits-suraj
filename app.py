import streamlit as st

st.set_page_config(page_title="Valentine 💖", page_icon="💘")

st.markdown(
    """
    <style>
    body {
        background-color: #ffe6ee;
    }

    .wrapper {
        display: flex;
        justify-content: center;
        margin-top: 100px;
    }

    .card {
        background: white;
        padding: 40px;
        border-radius: 25px;
        width: 320px;
        text-align: center;
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        position: relative;
        font-family: Arial, sans-serif;
    }

    h2 {
        margin-bottom: 30px;
    }

    .btn-yes {
        background-color: #ff4d6d;
        color: white;
        border: none;
        padding: 12px 28px;
        font-size: 18px;
        border-radius: 25px;
        cursor: pointer;
        margin-right: 10px;
    }

    .btn-no {
        background-color: #ddd;
        color: black;
        border: none;
        padding: 12px 28px;
        font-size: 18px;
        border-radius: 25px;
        cursor: pointer;
        position: absolute;
        left: 180px;
        top: 170px;
    }
    </style>

    <div class="wrapper">
        <div class="card">
            <h2>Will you be my Valentine? 💕</h2>

            <button class="btn-yes"
                onclick="document.getElementById('result').innerHTML='💖 YAY!!! 💖'">
                Yes
            </button>

            <button class="btn-no" id="noBtn">
                No
            </button>

            <p id="result" style="margin-top:20px;font-size:20px;"></p>
        </div>
    </div>

    <script>
    const noBtn = document.getElementById("noBtn");
    const card = document.querySelector(".card");

    noBtn.addEventListener("mouseover", () => {
        const maxX = card.clientWidth - noBtn.offsetWidth;
        const maxY = card.clientHeight - noBtn.offsetHeight;

        const x = Math.random() * maxX;
        const y = Math.random() * maxY;

        noBtn.style.left = x + "px";
        noBtn.style.top = y + "px";
    });
    </script>
    """,
    unsafe_allow_html=True
)
