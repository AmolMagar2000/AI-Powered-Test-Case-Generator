# utils/ai_utils.py
import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = None
if API_KEY:
    genai.configure(api_key=API_KEY)
    MODEL = genai.GenerativeModel("gemini-2.0-flash")

def _model_check():
    if MODEL is None:
        st.error("GEMINI_API_KEY not configured. Set GEMINI_API_KEY in your environment or .env")
        return False
    return True

def generate_test_cases_from_prompt(prompt_text, num_cases=10, priority="Medium"):
    if not _model_check(): return []
    prompt_template = f"""
You are a senior QA engineer with 15+ years of experience.
Generate {num_cases} comprehensive test cases based on the following requirements:

{prompt_text}

Instructions:
- Default Priority: {priority}
- Format test cases in JSON with this structure:
{{
    "test_cases": [
        {{
            "id": "TC_001",
            "title": "Test case title",
            "preconditions": ["Precondition 1"],
            "test_data": ["Data 1"],
            "test_steps": ["Step 1"],
            "expected_results": ["Expected 1"],
            "priority": "High/Medium/Low",
            "attachments": []
        }}
    ]
}}
"""
    try:
        resp = MODEL.generate_content(prompt_template)
        # try to extract JSON from response
        import re, json
        json_match = re.search(r'\{[\s\S]*\}', resp.text)
        if json_match:
            data = json.loads(json_match.group())
            return data.get("test_cases", [])
        return []
    except Exception as e:
        st.error("AI generation failed: " + str(e))
        return []

def generate_test_case_automation_code(test_case):
    if not _model_check(): return ""
    prompt_template = f"""
You are a super senior QA automation engineer with over 30 years of enterprise experience.
Write complete, production-grade Selenium test automation code in Java using TestNG and Page Object Model.

Based on the following test case:
- Title: {test_case.get('title')}
- Steps:
{chr(10).join(test_case.get('test_steps', []))}
- Expected Results:
{chr(10).join(test_case.get('expected_results', []))}

Output files should be indicated with lines like:
// FILE: src/main/java/com/qa/pages/[PageName]Page.java
[Java code here]

"""
    try:
        resp = MODEL.generate_content(prompt_template)
        return resp.text
    except Exception as e:
        st.error("AI generation failed: " + str(e))
        return ""

def generate_combined_automation_code(test_cases):
    if not _model_check(): return ""
    test_cases_str = "\n\n".join(
        [f"Test Case {i+1}: {tc.get('title')}\nSteps:\n{chr(10).join(tc.get('test_steps', []))}\nExpected:\n{chr(10).join(tc.get('expected_results', []))}"
         for i, tc in enumerate(test_cases)]
    )
    prompt_template = f"""
You are a super senior QA automation engineer with over 30 years of enterprise experience.
Create a SINGLE test class that includes test methods for the following test cases:

{test_cases_str}

Output the code with file markers as // FILE: path.
"""
    try:
        resp = MODEL.generate_content(prompt_template)
        return resp.text
    except Exception as e:
        st.error("AI generation failed: " + str(e))
        return ""
