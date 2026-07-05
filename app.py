import streamlit as st
import anthropic
import base64
from PIL import Image
import io
import re

st.set_page_config(page_title="OOTD Creator", page_icon="👗", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pinyon+Script&display=swap');

html, body, [class*="css"] {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-weight: 300;
    background-color: #fafaf8;
    color: #1a1a1a;
}

h1 {
    font-family: 'Pinyon Script', cursive !important;
    font-size: 2.8rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.01em;
    color: #1a1a1a;
}

.stButton > button {
    background-color: #1a1a1a;
    color: #fafaf8;
    border: none;
    border-radius: 0;
    padding: 0.75rem 2.5rem;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-weight: 300;
    font-size: 0.85rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    cursor: pointer;
    width: 100%;
    margin-top: 1rem;
}

.stButton > button:hover {
    background-color: #333;
}

.stTextInput > div > div > input {
    border: none;
    border-bottom: 1px solid #1a1a1a;
    border-radius: 0;
    background: transparent;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-weight: 300;
    font-size: 0.95rem;
    padding: 0.5rem 0;
}

h2 {
    font-size: 0.8rem !important;
    font-weight: 300 !important;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
    margin-top: 1.2rem;
    margin-bottom: 0.2rem;
    color: #1a1a1a;
}

div[data-testid="stFileUploader"] {
    border: 1px dashed #ccc;
    padding: 1rem;
    background: transparent;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>OOTD Creator</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-weight:300; color:#666; margin-bottom:2rem;'>Upload a piece. Define your vibe. Get your outfit.</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
vibe = st.text_input("", placeholder="your vibe — e.g. quiet luxury, y2k, office minimal", label_visibility="collapsed")

generate = st.button("Generate OOTD")

if generate and uploaded_file and vibe:
    with st.spinner(""):
        image = Image.open(uploaded_file)
        buffer = io.BytesIO()
        fmt = "JPEG" if uploaded_file.type == "image/jpeg" else "PNG"
        media_type = uploaded_file.type
        image.save(buffer, format=fmt)
        image_data = base64.standard_b64encode(buffer.getvalue()).decode("utf-8")

        client = anthropic.Anthropic()
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": f"You are a personal stylist. The user has this clothing item and wants to build an outfit with this vibe: '{vibe}'. Suggest a complete outfit: shoes, bottom, top, bag, accessories, and one styling tip. Be specific and concise. Start each section on a new line with ## followed by the section name. Do not use ** or * anywhere."
                        }
                    ],
                }
            ],
        )
        result = message.content[0].text
        result = re.sub(r"([^\n])(##)", r"\1\n\2", result)

    st.markdown("---")
    st.markdown(result)

elif generate and (not uploaded_file or not vibe):
    st.warning("Upload an item and describe your vibe first.")