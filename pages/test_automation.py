# pages/test_automation.py
import streamlit as st
import zipfile
from io import BytesIO
from utils import ai_utils, code_utils
import utils.ui_utils as ui_utils

def render_test_automation():
    st.subheader("🤖 Java Selenium Automation Generator")

    if not st.session_state.selected_test_cases:
        st.info("No test cases selected for automation")
        st.markdown("Go to **Test Case Generator** to create and select test cases")
        if st.button("Go to Test Case Generator"):
            st.experimental_set_query_params(page="Test Case Generator")
            ui_utils.safe_rerun()
        return

    st.success(f"Generating automation code for {len(st.session_state.selected_test_cases)} test cases")

    st.markdown('<div class="combined-toggle">', unsafe_allow_html=True)
    mode = st.radio("Generation Mode:", ["Combined Test Suite", "Separate Test Classes"], key="generation_mode_radio", horizontal=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Generate Automation Code", key="generate_automation", use_container_width=True):
        st.session_state.automation_code = {}
        if mode == "Combined Test Suite":
            automation_code = ai_utils.generate_combined_automation_code(st.session_state.selected_test_cases)
            if automation_code:
                st.session_state.automation_code["combined"] = code_utils.parse_generated_code(automation_code)
                ui_utils.show_toast("✅ Combined test suite generated successfully!")
        else:
            for tc in st.session_state.selected_test_cases:
                automation_code = ai_utils.generate_test_case_automation_code(tc)
                st.session_state.automation_code[tc['id']] = code_utils.parse_generated_code(automation_code)
            ui_utils.show_toast("✅ Automation code generated successfully!")

    if st.session_state.automation_code:
        if mode == "Combined Test Suite" and "combined" in st.session_state.automation_code:
            st.markdown("### 🧩 Combined Test Suite")
            st.subheader("Generated Automation Code")
            for file_name, content in st.session_state.automation_code["combined"].items():
                with st.expander(f"📄 {file_name}"):
                    st.code(content, language='java')

            # Zip for download
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
                for file_name, content in st.session_state.automation_code["combined"].items():
                    zip_file.writestr(file_name, content)
            zip_buffer.seek(0)
            st.download_button("Download Combined Test Suite", data=zip_buffer, file_name="CombinedTestSuite.zip", mime="application/zip", use_container_width=True)

            st.markdown("### Test Cases in this Suite")
            for test_case in st.session_state.selected_test_cases:
                with st.expander(f"{test_case['id']}: {test_case['title']}"):
                    st.markdown(f"**Priority:** `{test_case['priority']}`")
                    st.markdown("**Steps:**")
                    for step in test_case['test_steps']:
                        st.markdown(f"- {step}")
                    st.markdown("**Expected Results:**")
                    for result in test_case['expected_results']:
                        st.markdown(f"- {result}")
        else:
            # Separate files view
            tabs = st.tabs([f"Test Case: {tc['id']}" for tc in st.session_state.selected_test_cases])
            for idx, tc in enumerate(st.session_state.selected_test_cases):
                with tabs[idx]:
                    st.markdown(f"### {tc['title']}")
                    st.markdown(f"**ID:** {tc['id']} | **Priority:** `{tc['priority']}`")
                    with st.expander("Test Case Details", expanded=False):
                        st.markdown("**Steps:**")
                        for step in tc['test_steps']:
                            st.markdown(f"- {step}")
                        st.markdown("**Expected Results:**")
                        for result in tc['expected_results']:
                            st.markdown(f"- {result}")
                    if tc['id'] in st.session_state.automation_code:
                        st.subheader("Generated Automation Code")
                        for file_name, content in st.session_state.automation_code[tc['id']].items():
                            with st.expander(f"📄 {file_name}"):
                                st.code(content, language='java')
                        # ZIP download
                        zip_buffer = BytesIO()
                        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
                            for file_name, content in st.session_state.automation_code[tc['id']].items():
                                zip_file.writestr(file_name, content)
                        zip_buffer.seek(0)
                        st.download_button(label=f"Download Code for {tc['id']}", data=zip_buffer, file_name=f"{tc['id']}_automation.zip", mime="application/zip", use_container_width=True)
                    else:
                        st.info("Click 'Generate Automation Code' to create Java code")
