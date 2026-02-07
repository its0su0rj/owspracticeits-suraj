import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Valentine 💖", page_icon="💘")

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
@keyframes floatUp {
  from { transform: translateY(0); opacity: 1; }
  to { transform: translateY(-120vh); opacity: 0; }
}

body {
    margin: 0;
    height: 100vh;
    background: linear-gradient(135deg, #fde2e4, #fadadd, #fff1f7);
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: 'Poppins', sans-serif;
    overflow: hidden;
}

.card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(14px);
    padding: 45px 35px;
    border-radius: 35px;
    width: 330px;
    text-align: center;
    box-shadow: 0 30px 60px rgba(0,0,0,0.15);
    position: relative;
}

.face {
    font-size: 52px;
    margin-bottom: 10px;
    transition: transform 0.3s ease;
}

h2 {
    font-size: 22px;
    margin-bottom: 30px;
}

.buttons {
    position: relative;
    height: 90px;
}

.btn-yes {
    background: linear-gradient(135deg, #ff4d6d, #ff8fab);
    color: white;
    border: none;
    padding: 14px 34px;
    font-size: 18px;
    border-radius: 35px;
    cursor: pointer;
    transition: transform 0.2s ease;
}

.btn-yes:hover {
    transform: scale(1.12);
}

.btn-no {
    background: #e6e6e6;
    color: #333;
    border: none;
    padding: 14px 34px;
    font-size: 18px;
    border-radius: 35px;
    cursor: pointer;
    position: absolute;
    left: 170px;
    top: 10px;
    transition: all 0.25s ease;
}

#result {
    margin-top: 22px;
    font-size: 22px;
}

.heart {
    position: absolute;
    bottom: -30px;
    font-size: 22px;
    animation: floatUp linear infinite;
}
</style>
</head>

<body>

<div class="card">
    <div class="face" id="face">😳</div>
    <h2>Will you be my Valentine? 💕</h2>

    <div class="buttons">
        <button class="btn-yes" onclick="sayYes()">Yes</button>
        <button class="btn-no" id="noBtn">No</button>
    </div>

    <div id="result"></div>
</div>

<script>
let noCount = 0;
const noBtn = document.getElementById("noBtn");
const face = document.getElementById("face");
const area = document.querySelector(".buttons");

noBtn.addEventListener("mouseover", () => {
    noCount++;

    face.innerHTML = noCount < 3 ? "🥺" : "😭";

    const maxX = area.clientWidth - noBtn.offsetWidth;
    const maxY = area.clientHeight - noBtn.offsetHeight;

    noBtn.style.left = Math.random() * maxX + "px";
    noBtn.style.top = Math.random() * maxY + "px";
    noBtn.style.transform = `scale(${Math.max(0.5, 1 - noCount * 0.1)})`;

    if (noCount >= 6) {
        noBtn.style.display = "none";
        face.innerHTML = "😔";
    }
});

function sayYes() {
    face.innerHTML = "🥰";
    document.getElementById("result").innerHTML = "💖 YAY!!! You made my day 💖";
    launchHearts();
}

function launchHearts() {
    for (let i = 0; i < 30; i++) {
        const heart = document.createElement("div");
        heart.className = "heart";
        heart.innerHTML = Math.random() > 0.5 ? "💖" : "✨";
        heart.style.left = Math.random() * 100 + "vw";
        heart.style.animationDuration = (3 + Math.random() * 3) + "s";
        document.body.appendChild(heart);

        setTimeout(() => heart.remove(), 6000);
    }
}
</script>

</body>
</html>
"""

components.html(html_code, height=650)
