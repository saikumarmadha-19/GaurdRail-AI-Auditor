import streamlit as st
from auditor_tool import DataAuditor
from langchain_ollama import OllamaLLM
import json

st.set_page_config(page_title="AI Data Auditor", layout="wide")
st.title("🛡️ GuardRail AI: Autonomous Data Auditor")

# 1. Sidebar - Configuration
st.sidebar.header("Settings")
model_name = st.sidebar.selectbox("Select Model", ["llama3"])
uploaded_file = st.sidebar.file_uploader("Upload your 'Dirty' Data CSV", type="csv")

if uploaded_file:
    # Initialize our Auditor and LLM
    # In a real app, we'd save the uploaded file temporarily
    with open("temp_data.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())

    auditor = DataAuditor("temp_data.csv")
    llm = OllamaLLM(model=model_name)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Raw Data Preview")
        st.dataframe(auditor.df.head())

    if st.button("🚀 Run AI Audit"):
        with st.spinner("Agent is analyzing data patterns..."):
            summary = auditor.get_audit_summary()

            # The prompt we perfected earlier
            prompt = f"Return ONLY a JSON list of fixes for this data: {summary}. Format: [{{'column': '...', 'old_value': '...', 'new_value': '...'}}]"

            response = llm.invoke(prompt)

            try:
                # Extract JSON
                json_start = response.find('[')
                json_end = response.rfind(']') + 1
                fixes = json.loads(response[json_start:json_end])

                st.subheader("AI Proposed Fixes")
                for i, fix in enumerate(fixes):
                    st.info(f"Issue {i + 1}: Change '{fix['old_value']}' to '{fix['new_value']}' in {fix['column']}")
                    if st.button(f"Approve Fix {i + 1}", key=f"btn_{i}"):
                        msg = auditor.fix_column_value(fix['column'], fix['old_value'], fix['new_value'])
                        st.success(msg)
            except Exception as e:
                st.error("AI returned non-JSON output. Try again.")
                st.write(response)