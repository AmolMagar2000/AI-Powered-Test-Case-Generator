# utils/file_utils.py
import PyPDF2
import docx
import pandas as pd
from io import BytesIO
import streamlit as st

def extract_text_from_txt(uploaded_file):
    return uploaded_file.read().decode("utf-8")

def extract_text_from_pdf(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
        text = "".join([p.extract_text() or "" for p in reader.pages])
        return text
    except Exception as e:
        st.error("Failed to read PDF: " + str(e))
        return ""

def extract_text_from_docx(uploaded_file):
    try:
        doc = docx.Document(BytesIO(uploaded_file.read()))
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        st.error("Failed to read DOCX: " + str(e))
        return ""

def extract_text_from_csv(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df.to_markdown()

def extract_text_from_xlsx(uploaded_file):
    df = pd.read_excel(uploaded_file)
    return df.to_markdown()

def extract_text_from_file(uploaded_file):
    t = uploaded_file.type
    if t == "text/plain":
        return extract_text_from_txt(uploaded_file)
    if t == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    if t == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(uploaded_file)
    if t == "text/csv":
        return extract_text_from_csv(uploaded_file)
    if t in ("application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
        return extract_text_from_xlsx(uploaded_file)
    st.error("Unsupported file type: " + t)
    return ""
