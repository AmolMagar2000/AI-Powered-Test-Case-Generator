# app.py
import streamlit as st
import sys
from pathlib import Path

# Add project root to path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

import utils.ui_utils as ui_utils
from pages import test_case_gen, test_automation

# Page configuration
st.set_page_config(
    page_title="QE Test Automation Suite",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
ui_utils.load_css()

# Initialize session state
defaults = {
    'test_cases': [],
    'automation_code': {},
    'current_tc_id': "",
    'framework_generated': False,
    'framework_code': {},
    'file_content': "",
    'show_toast': False,
    'toast_message': "",
    'toast_time': 0,
    'selected_test_cases': [],
    'editing_test_case': None,
    'editing_index': None,
    'test_cases_str': "",
    'generation_mode': "Combined Test Suite",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Header
st.markdown('<div class="header"><h1>🤖 QE Test Automation Suite</h1></div>', unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("### 📋 Navigation")
    page = st.radio(
        "Select Page",
        ["Test Case Generator", "Test Automation"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total", len(st.session_state.test_cases))
    with col2:
        st.metric("Selected", len(st.session_state.selected_test_cases))
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info("Generate professional test cases and Selenium automation code using AI")

# Route to pages
if page == "Test Case Generator":
    test_case_gen.render_test_case_gen()
elif page == "Test Automation":
    test_automation.render_test_automation()

# Toast notification
import time
if st.session_state.get('show_toast'):
    if time.time() - st.session_state.get('toast_time', 0) < 3:
        st.markdown(
            f'<div class="toast">{st.session_state.toast_message}</div>',
            unsafe_allow_html=True
        )
    else:
        st.session_state.show_toast = False

# Footer
st.markdown("---")
st.markdown(
    '<div class="footer">QE Test Automation Suite | Powered by Gemini 2.0 Flash</div>',
    unsafe_allow_html=True
)