# utils/ui_utils.py
import streamlit as st
from pathlib import Path
import time

def load_css():
    """Load custom CSS from assets folder"""
    css_path = Path(__file__).resolve().parents[1] / "assets" / "style.css"
    if css_path.exists():
        try:
            css = css_path.read_text(encoding="utf-8")
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Could not load CSS: {e}")
    else:
        st.warning(f"CSS file not found at {css_path}")

def show_toast(message, duration=3):
    """
    Display a toast notification
    
    Args:
        message: Message to display
        duration: Duration in seconds (default 3)
    """
    st.session_state.show_toast = True
    st.session_state.toast_message = message
    st.session_state.toast_time = time.time()

def safe_rerun():
    """
    Safely rerun the Streamlit app using the appropriate method
    """
    try:
        # Try using st.rerun() (Streamlit >= 1.27)
        if hasattr(st, "rerun"):
            st.rerun()
        # Fallback to experimental_rerun
        elif hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        else:
            # Last resort: stop execution
            st.stop()
    except Exception:
        st.stop()

def display_test_case_card(test_case, index):
    """
    Display a test case in a card format
    
    Args:
        test_case: Test case dictionary
        index: Index in the list
    """
    priority_colors = {
        "High": "🔴",
        "Medium": "🟡",
        "Low": "🟢"
    }
    
    priority_icon = priority_colors.get(test_case.get('priority', 'Medium'), "⚪")
    
    with st.container():
        col1, col2 = st.columns([0.05, 0.95])
        
        with col1:
            selected = st.checkbox(
                "",
                value=test_case.get("selected", False),
                key=f"select_{test_case['id']}_{index}",
                label_visibility="collapsed"
            )
            test_case["selected"] = selected
        
        with col2:
            with st.expander(
                f"{priority_icon} **{test_case['id']}** - {test_case['title']}",
                expanded=False
            ):
                # Display metadata
                if test_case.get("area") or test_case.get("module") or test_case.get("submodule"):
                    info_parts = [
                        p for p in [
                            test_case.get("area"),
                            test_case.get("module"),
                            test_case.get("submodule")
                        ] if p
                    ]
                    if info_parts:
                        st.caption(" > ".join(info_parts))
                
                # Display content in columns
                if test_case.get("preconditions") or test_case.get("test_data"):
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        if test_case.get("preconditions"):
                            st.markdown("**Preconditions:**")
                            for pre in test_case["preconditions"]:
                                st.markdown(f"• {pre}")
                    
                    with col_b:
                        if test_case.get("test_data"):
                            st.markdown("**Test Data:**")
                            for data in test_case["test_data"]:
                                st.markdown(f"• {data}")
                
                # Test steps
                if test_case.get("test_steps"):
                    st.markdown("**Test Steps:**")
                    for i, step in enumerate(test_case["test_steps"], 1):
                        st.markdown(f"{i}. {step}")
                
                # Expected results
                if test_case.get("expected_results"):
                    st.markdown("**Expected Results:**")
                    for result in test_case["expected_results"]:
                        st.markdown(f"✓ {result}")
                
                # Action buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(
                        "✏️ Edit",
                        key=f"edit_{test_case['id']}_{index}",
                        use_container_width=True
                    ):
                        st.session_state.editing_test_case = test_case
                        st.session_state.editing_index = index
                        safe_rerun()
                
                with col2:
                    if st.button(
                        "🤖 Automate",
                        key=f"automate_{test_case['id']}_{index}",
                        use_container_width=True
                    ):
                        st.session_state.selected_test_cases = [test_case]
                        # Navigation will be handled by the calling function

def format_code_file(file_name, content, language="java"):
    """
    Format and display a code file
    
    Args:
        file_name: Name of the file
        content: Code content
        language: Programming language (default java)
    """
    with st.expander(f"📄 {file_name}", expanded=False):
        st.code(content, language=language, line_numbers=True)

def create_download_button(data, filename, label, mime_type, key=None):
    """
    Create a styled download button
    
    Args:
        data: Data to download
        filename: Name for the downloaded file
        label: Button label
        mime_type: MIME type of the file
        key: Unique key for the button
    """
    return st.download_button(
        label=label,
        data=data,
        file_name=filename,
        mime=mime_type,
        key=key,
        use_container_width=True
    )

def display_stats(test_cases, selected_test_cases):
    """
    Display statistics about test cases
    
    Args:
        test_cases: List of all test cases
        selected_test_cases: List of selected test cases
    """
    col1, col2, col3, col4 = st.columns(4)
    
    priority_counts = {"High": 0, "Medium": 0, "Low": 0}
    for tc in test_cases:
        priority = tc.get("priority", "Medium")
        if priority in priority_counts:
            priority_counts[priority] += 1
    
    with col1:
        st.metric("Total Cases", len(test_cases))
    with col2:
        st.metric("Selected", len(selected_test_cases))
    with col3:
        st.metric("High Priority", priority_counts["High"])
    with col4:
        st.metric("Medium Priority", priority_counts["Medium"])