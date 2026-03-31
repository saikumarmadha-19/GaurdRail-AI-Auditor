# 🛡️ GuardRail AI: Autonomous Data Governance Auditor

An Agentic AI system built to automate data auditing and repair using Local LLMs (Ollama/Llama3).

## 🚀 The Problem
MNCs handle petabytes of data where manual auditing for PII (Privacy) and Data Quality is impossible. 

## 💡 The Solution
This project uses an **AI Agentic Workflow** to:
1. **Scan:** Use Python/Pandas to generate metadata summaries.
2. **Reason:** Use Llama3 to identify anomalies (PII, Type Mismatches, Outliers).
3. **Act:** Execute automated repairs via JSON-based tool calling.
4. **Govern:** Maintain a **Human-in-the-Loop** approval flow for data safety.

## 🛠️ Tech Stack
- **Brain:** Ollama (Llama 3)
- **Orchestration:** LangChain
- **Frontend:** Streamlit
- **Data:** Pandas

## ⚙️ How to Run
1. Install Ollama and run `ollama pull llama3`.
2. Install requirements: `pip install -r requirements.txt`.
3. Run the app: `streamlit run app.py`.# GaurdRail-AI-Auditor
# GaurdRail-AI-Auditor
