import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Valentine 💖", page_icon="💘")

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
    background-color: #ffe6ee;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    font-family: Arial, sans-serif;
}

.card {
    background: white;
    padding: 40px;
    border-radius: 25px;
    width: 320px;
    text-align: center;
    box-shadow: 0 15px 30px rgba(0,0,0,0.15);
    position: relative;
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

#result {
    margin-top: 20px;
    font-size: 20px;
}
</style>
</head>

<body>

<div class="card">
    <h2>Will you be my Valentine? 💕</h2>

    <button class="btn-yes" onclick="sayYes()">Yes</button>
    <button class="btn-no" id="noBtn">No</button>

    <div id="result"></div>
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

function sayYes() {
    document.getElementById("result").innerHTML = "💖 YAY!!! 💖";
}
</script>

</body>
</html>
"""

components.html(html_code, height=500)
