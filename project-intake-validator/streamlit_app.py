import sys
from pathlib import Path

# Add current directory to path to allow relative imports
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
from dotenv import load_dotenv
from src.piv.graph.graph import build_graph
from src.piv.llm.azure_openai_client import AzureOpenAILLM
import tempfile
import pandas as pd

st.set_page_config(page_title="Project Intake Validator", layout="wide")

st.title("📄 Project Intake Validator")
st.caption("Validate Header, Business Case, and Project Scope using Azure OpenAI + LangGraph")

load_dotenv()

# Build LLM client
try:
    llm = AzureOpenAILLM()
except Exception as e:
    st.error(f"Azure OpenAI configuration error: {e}")
    st.stop()

# Build graph
context = {"llm": llm, "prompts_dir": "prompts"}
graph = build_graph(context)

uploaded_file = st.file_uploader("Upload Excel Intake File (.xlsx)", type=["xlsx"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    st.success("File uploaded successfully. Click **Run Validation** below.")

    if st.button("Run Validation 🚀"):
        with st.spinner("Processing with Azure OpenAI…"):
            initial = {
                "source_path": str(Path(temp_path).resolve()),
                "document_text": "",
                "sections": {},
                "validation": {},
                "final_feedback": None,
            }

            result = graph.invoke(initial)

        st.subheader("📌 Final Feedback:")
        st.code(result["final_feedback"])

        st.subheader("📦 Extracted Sections")
        sections = result["sections"]

        with st.expander("Header Section"):
            st.json(sections.get("header", {}))

        with st.expander("Business Case Section"):
            st.json(sections.get("business_case", {}))

        with st.expander("Project Scope Section"):
            st.json(sections.get("project_scope", {}))

        st.subheader("🧪 Validation Details")
        st.json({k: v.model_dump() for k, v in result["validation"].items()})