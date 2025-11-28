# pages/home.py
import streamlit as st

def render_home():
    st.markdown('<div class="header"><h1>🤖 QE Test Automation</h1></div>', unsafe_allow_html=True)
    st.markdown("Generate professional test cases and  Selenium automation code")
    st.image("https://cdn-icons-png.flaticon.com/512/1046/1046784.png", width=200)
    st.markdown("---")
    st.markdown('<div class="footer">QE Test Automation Suite | Powered by Gemini 1.5 Flash</div>', unsafe_allow_html=True)
