import streamlit as st

# Embed the flower shower effect
st.markdown("""
    <style>
        .flower {
            position: absolute;
            z-index: 9999;
            pointer-events: none;
            animation: fall 10s linear infinite;
            opacity: 0.8;
        }
        @keyframes fall {
            0% { transform: translateY(-100%); }
            100% { transform: translateY(100vh); }
        }
    </style>
    <script>
        const addFlower = () => {
            const flower = document.createElement('div');
            flower.classList.add('flower');
            flower.style.left = Math.random() * 100 + 'vw';
            flower.style.width = Math.random() * 10 + 20 + 'px';
            flower.style.height = flower.style.width;
            flower.style.backgroundImage = 'url(https://raw.githubusercontent.com/guptaankit01/krishnalibrary/main/girls1.jpg)';
            flower.style.backgroundSize = 'cover';
            document.body.appendChild(flower);

            setTimeout(() => {
                flower.remove();
            }, 10000);
        }

        setInterval(addFlower, 500);
    </script>
""", unsafe_allow_html=True)

# Your existing Streamlit code
st.header("Testing Flower Shower Effect")
st.write("If the flower shower works, flowers should appear on the screen.")
