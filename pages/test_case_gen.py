# pages/test_case_gen.py
import streamlit as st
import base64
import pandas as pd
from io import BytesIO
from utils import file_utils, ai_utils
import utils.ui_utils as ui_utils

# Initialize session state
if "test_cases" not in st.session_state:
    st.session_state.test_cases = []
if "test_cases_str" not in st.session_state:
    st.session_state.test_cases_str = ""
if "editing_test_case" not in st.session_state:
    st.session_state.editing_test_case = None
if "editing_index" not in st.session_state:
    st.session_state.editing_index = None
if "selected_test_cases" not in st.session_state:
    st.session_state.selected_test_cases = []


def render_test_case_gen():
    st.markdown("## 🧪 Test Case Generator")
    st.caption("Create comprehensive test cases using AI or manually")

    tab1, tab2 = st.tabs(["📝 Manual Creation", "🤖 AI Generation"])

    # -------------------------
    # Manual creation tab
    # -------------------------
    with tab1:
        st.markdown("### Create Test Case")
        with st.form("manual_test_case_form", clear_on_submit=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                area = st.text_input("Area", placeholder="UI/UX", key="mc_area")
            with col2:
                module_name = st.text_input("Module", placeholder="Authentication", key="mc_module")
            with col3:
                submodule = st.text_input("Sub-Module", placeholder="Login", key="mc_submodule")

            col1, col2 = st.columns([3, 1])
            with col1:
                title = st.text_input("Test Scenario*", placeholder="User login with valid credentials", key="mc_title")
            with col2:
                priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=1, key="mc_priority")

            col1, col2 = st.columns(2)
            with col1:
                preconditions = st.text_area(
                    "Preconditions",
                    placeholder="• User is registered\n• Application is running",
                    height=100,
                    key="mc_preconditions",
                )
            with col2:
                test_data = st.text_area(
                    "Test Data",
                    placeholder="Username: testuser\nPassword: Test@123",
                    height=100,
                    key="mc_testdata",
                )

            steps = st.text_area(
                "Test Steps*",
                placeholder="1. Navigate to login page\n2. Enter username\n3. Enter password\n4. Click login",
                height=120,
                key="mc_steps",
            )
            expected = st.text_area(
                "Expected Results*",
                placeholder="• User redirected to dashboard\n• Welcome message displayed",
                height=100,
                key="mc_expected",
            )

            attachments = st.file_uploader(
                "Attachments (optional)",
                type=["png", "jpg", "jpeg", "txt", "pdf", "xlsx", "xls", "docx"],
                accept_multiple_files=True,
                key="mc_attachments",
            )

            submitted = st.form_submit_button("💾 Save Test Case", use_container_width=True)
            if submitted:
                if not title or not steps or not expected:
                    st.error("⚠️ Please fill required fields (marked with *)")
                else:
                    attachments_data = []
                    for f in attachments or []:
                        content = base64.b64encode(f.read()).decode("utf-8")
                        attachments_data.append({"name": f.name, "type": f.type, "content": content})

                    test_case = {
                        "id": f"TC_{len(st.session_state.test_cases) + 1:03d}",
                        "area": area,
                        "module": module_name,
                        "submodule": submodule,
                        "title": title,
                        "preconditions": [p.strip() for p in preconditions.split("\n") if p.strip()],
                        "test_data": [d.strip() for d in test_data.split("\n") if d.strip()],
                        "test_steps": [s.strip() for s in steps.split("\n") if s.strip()],
                        "expected_results": [e.strip() for e in expected.split("\n") if e.strip()],
                        "priority": priority,
                        "attachments": attachments_data,
                        "selected": False,
                    }
                    st.session_state.test_cases.append(test_case)
                    ui_utils.show_toast("✅ Test case saved!")
                    st.rerun()

        # Generate from context
        with st.expander("🔄 Generate from Current Context", expanded=False):
            num_generate = st.number_input("Cases to generate", 1, 20, 5, key="mc_num_generate")
            if st.button("🚀 Generate", use_container_width=True, key="mc_generate_from_context"):
                context = {
                    "area": st.session_state.get("mc_area", ""),
                    "module": st.session_state.get("mc_module", ""),
                    "submodule": st.session_state.get("mc_submodule", ""),
                    "title": st.session_state.get("mc_title", ""),
                    "preconditions": st.session_state.get("mc_preconditions", ""),
                    "test_data": st.session_state.get("mc_testdata", ""),
                    "steps": st.session_state.get("mc_steps", ""),
                    "expected": st.session_state.get("mc_expected", ""),
                    "priority": st.session_state.get("mc_priority", "Medium"),
                }

                context_prompt = f"""Based on this context, generate {num_generate} test cases:
Area: {context['area']}
Module: {context['module']}
SubModule: {context['submodule']}
Scenario: {context['title']}
Steps: {context['steps']}
Expected: {context['expected']}"""

                with st.spinner("Generating..."):
                    generated_cases = ai_utils.generate_test_cases_from_prompt(
                        context_prompt, num_cases=num_generate, priority=context['priority']
                    )
                    if generated_cases:
                        for i, tc in enumerate(generated_cases):
                            tc["id"] = f"TC_{len(st.session_state.test_cases) + i + 1:03d}"
                            tc.setdefault("area", context['area'])
                            tc.setdefault("module", context['module'])
                            tc.setdefault("submodule", context['submodule'])
                            tc["selected"] = False
                            st.session_state.test_cases.append(tc)
                        ui_utils.show_toast(f"✅ Generated {len(generated_cases)} cases!")
                        st.rerun()

    # -------------------------
    # AI Generation tab
    # -------------------------
    with tab2:
        st.markdown("### Generate from Requirements")
        user_story = st.text_area(
            "Requirements or User Story",
            height=200,
            placeholder="Example:\nAs a user, I want to login so that I can access my account.\n\nAcceptance Criteria:\n• Valid credentials allow login\n• Invalid credentials show error",
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            num_test_cases = st.slider("Cases to Generate", 1, 50, 10, key="gen_req_num")
        with col2:
            priority = st.selectbox("Default Priority", ["High", "Medium", "Low"], index=1)
            
        if st.button("🤖 Generate Test Cases", use_container_width=True, type="primary"):
            if user_story:
                with st.spinner(f"Generating {num_test_cases} test cases..."):
                    generated_cases = ai_utils.generate_test_cases_from_prompt(
                        user_story, num_cases=num_test_cases, priority=priority
                    )
                    if generated_cases:
                        for i, tc in enumerate(generated_cases):
                            tc["id"] = f"TC_{len(st.session_state.test_cases) + i + 1:03d}"
                            tc["selected"] = False
                            tc.setdefault("attachments", [])
                        st.session_state.test_cases.extend(generated_cases)
                        ui_utils.show_toast(f"✅ Generated {len(generated_cases)} cases!")
                        st.rerun()
            else:
                st.warning("⚠️ Please enter requirements")

    # -------------------------
    # Test Case Management
    # -------------------------
    if st.session_state.test_cases:
        st.markdown("---")
        st.markdown("## 📋 Test Case Library")
        
        # Bulk actions
        col1, col2, col3, col4, col5 = st.columns([1, 1.5, 1.5, 1.5, 1])
        with col1:
            all_selected = all(tc.get("selected", False) for tc in st.session_state.test_cases)
            select_all = st.checkbox("Select All", value=all_selected)
            if select_all != all_selected:
                for tc in st.session_state.test_cases:
                    tc["selected"] = select_all

        selected_count = sum(1 for tc in st.session_state.test_cases if tc.get("selected", False))
        
        with col2:
            if selected_count > 0:
                if st.button(f"🤖 Automate ({selected_count})", use_container_width=True):
                    st.session_state.selected_test_cases = [
                        tc for tc in st.session_state.test_cases if tc.get("selected", False)
                    ]
                    st.switch_page("pages/test_automation.py") if hasattr(st, 'switch_page') else None
        with col3:
            if st.button("📥 Export Excel", use_container_width=True):
                rows = []
                for tc in st.session_state.test_cases:
                    rows.append({
                        "ID": tc.get("id", ""),
                        "Area": tc.get("area", ""),
                        "Module": tc.get("module", ""),
                        "SubModule": tc.get("submodule", ""),
                        "Title": tc.get("title", ""),
                        "Priority": tc.get("priority", ""),
                        "Preconditions": "\n".join(tc.get("preconditions", [])),
                        "Test Data": "\n".join(tc.get("test_data", [])),
                        "Steps": "\n".join(tc.get("test_steps", [])),
                        "Expected": "\n".join(tc.get("expected_results", [])),
                    })
                df = pd.DataFrame(rows)
                buffer = BytesIO()
                df.to_excel(buffer, index=False, sheet_name="TestCases")
                buffer.seek(0)
                st.download_button(
                    "💾 Download",
                    buffer,
                    "test_cases.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        
        with col4:
            if selected_count > 0:
                if st.button(f"🗑️ Delete ({selected_count})", use_container_width=True):
                    st.session_state.test_cases = [
                        tc for tc in st.session_state.test_cases if not tc.get("selected", False)
                    ]
                    ui_utils.show_toast(f"✅ Deleted {selected_count} cases")
                    st.rerun()

        # Display test cases
        for idx, tc in enumerate(st.session_state.test_cases):
            col1, col2 = st.columns([0.05, 0.95])
            with col1:
                selected = st.checkbox("", value=tc.get("selected", False), key=f"sel_{tc['id']}", label_visibility="collapsed")
                tc["selected"] = selected
            
            with col2:
                priority_colors = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                priority_icon = priority_colors.get(tc['priority'], "⚪")
                
                with st.expander(f"{priority_icon} **{tc['id']}** - {tc['title']}", expanded=False):
                    if tc.get("area") or tc.get("module") or tc.get("submodule"):
                        info_parts = [p for p in [tc.get("area"), tc.get("module"), tc.get("submodule")] if p]
                        st.caption(" > ".join(info_parts))
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        if tc.get("preconditions"):
                            st.markdown("**Preconditions:**")
                            for pre in tc["preconditions"]:
                                st.markdown(f"• {pre}")
                    with col_b:
                        if tc.get("test_data"):
                            st.markdown("**Test Data:**")
                            for data in tc["test_data"]:
                                st.markdown(f"• {data}")
                    
                    st.markdown("**Test Steps:**")
                    for i, step in enumerate(tc["test_steps"], 1):
                        st.markdown(f"{i}. {step}")
                    
                    st.markdown("**Expected Results:**")
                    for result in tc["expected_results"]:
                        st.markdown(f"✓ {result}")
                    
                    # Actions
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✏️ Edit", key=f"edit_{tc['id']}", use_container_width=True):
                            st.session_state.editing_test_case = tc
                            st.session_state.editing_index = idx
                            st.rerun()
                    with col2:
                        if st.button("🤖 Automate", key=f"auto_{tc['id']}", use_container_width=True):
                            st.session_state.selected_test_cases = [tc]
                            # Navigate to automation page
    else:
        st.info("💡 No test cases yet. Create or generate test cases to get started.")

    # Edit modal
    if st.session_state.editing_test_case:
        tc = st.session_state.editing_test_case
        idx = st.session_state.editing_index
        
        st.markdown("---")
        st.markdown(f"### ✏️ Editing: {tc['id']}")
        
        with st.form(f"edit_form_{tc['id']}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                area = st.text_input("Area", value=tc.get("area", ""))
            with col2:
                module = st.text_input("Module", value=tc.get("module", ""))
            with col3:
                submodule = st.text_input("Sub-Module", value=tc.get("submodule", ""))
            
            col1, col2 = st.columns([3, 1])
            with col1:
                title = st.text_input("Test Scenario*", value=tc["title"])
            with col2:
                priority = st.selectbox("Priority", ["High", "Medium", "Low"], 
                                      index=["High", "Medium", "Low"].index(tc["priority"]))
            
            col1, col2 = st.columns(2)
            with col1:
                preconditions = st.text_area("Preconditions", value="\n".join(tc["preconditions"]), height=100)
            with col2:
                test_data = st.text_area("Test Data", value="\n".join(tc.get("test_data", [])), height=100)
            
            steps = st.text_area("Test Steps*", value="\n".join(tc["test_steps"]), height=120)
            expected = st.text_area("Expected Results*", value="\n".join(tc["expected_results"]), height=100)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("💾 Save Changes", use_container_width=True):
                    st.session_state.test_cases[idx] = {
                        "id": tc["id"],
                        "area": area,
                        "module": module,
                        "submodule": submodule,
                        "title": title,
                        "preconditions": [p.strip() for p in preconditions.split("\n") if p.strip()],
                        "test_data": [d.strip() for d in test_data.split("\n") if d.strip()],
                        "test_steps": [s.strip() for s in steps.split("\n") if s.strip()],
                        "expected_results": [e.strip() for e in expected.split("\n") if e.strip()],
                        "priority": priority,
                        "attachments": tc.get("attachments", []),
                        "selected": tc.get("selected", False),
                    }
                    st.session_state.editing_test_case = None
                    ui_utils.show_toast("✅ Updated!")
                    st.rerun()
            with col2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state.editing_test_case = None
                    st.rerun()