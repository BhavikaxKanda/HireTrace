# HireTrace AI

###AI-Powered Semantic Shortlisting & Bias-Free Ranking Agent

**HireTrace AI** is a specialized recruitment auditing platform designed to eliminate unconscious bias and manual inefficiency in technical hiring. Developed during the **AI Enablement Internship**, this tool leverages a multi-agent architecture to perform deep technical gap analysis while strictly adhering to enterprise-grade privacy standards.

**Core Features:**

* **The Privacy Shield**: Implements **Microsoft Presidio** to automatically redact PII (Names, Emails, Phone Numbers) locally before any data is transmitted to the LLM, ensuring 100% candidate anonymity during the audit phase.
* **Semantic Competency Mapping**: Moves beyond traditional keyword matching by evaluating high-level engineering logic, project complexity (e.g., RAG pipelines, Agentic AI), and transferable technical skills.
* **Deterministic Ranking Engine**: Configured with a strictly locked **Temperature (0.0)** to provide consistent, repeatable, and defensible scoring across multiple analysis runs.
* **Modest & Precise Scoring**: Utilizes a custom-calibrated scoring rubric that weights Skills Match (30%), Experience Relevance (25%), and Project Complexity (20%) to distinguish "High-Tier" engineers from "Average" matches.
* **High-Tech UI**: A professional dark-themed **Streamlit** interface featuring "shimmering" animated titles and action-oriented "glitter" buttons for a modern production-ready feel.

**Technical Stack:**

* **Frontend**: Streamlit
* **Intelligence**: Llama 3.1-8B-Instant (via Groq Cloud)
* **Security/PII**: Microsoft Presidio (Analyzer & Anonymizer)
* **Parsing**: PyPDF2 / PDFMiner
* **Database Management**: Integration logic for Vector Stores (Neon/PostgreSQL)

**Evaluation Logic:**

* The system evaluates candidates against high-level standards (e.g., Schneider Electric Business Analytics requirements), specifically looking for proficiency in Tableau, Excel modeling, and Python-driven data cleaning, while rewarding candidates who demonstrate advanced engineering logic in specialized projects.
