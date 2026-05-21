
# ==============================
# Imports
# ==============================
import os
import gradio as gr
from google.colab import userdata

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.agents import initialize_agent, AgentType
from langchain_core.tools import tool

# ==============================
# API Key (Gemini)
# ==============================
os.environ["GOOGLE_API_KEY"] = userdata.get("GOOGLE_API_KEY")

# ==============================
# LLM + Embeddings
# ==============================
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.2
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = None  # global

# ==============================
# Process Medical PDFs
# ==============================
def process_pdfs(files):
    global vectordb

    if not files:
        return "⚠️ Upload at least one medical PDF."

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = []

    for file in files:
        pdf_docs = PyPDFLoader(file.name).load()
        for d in pdf_docs:
            d.metadata["type"] = "MEDICAL_DOC"
        docs.extend(splitter.split_documents(pdf_docs))

    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embeddings
    )

    return f"✅ Medical PDFs processed. Total chunks: {len(docs)}. Go to Ask tab."

# ==============================
# Tool
# ==============================
@tool
def search_docs(query: str) -> str:
    """Search medical documents and return evidence."""
    global vectordb
    if vectordb is None:
        return "NO_DOCUMENTS: Please upload and process medical PDFs first."

    results = vectordb.as_retriever(search_kwargs={"k": 6}).invoke(query)
    if not results:
        return "NO_MATCHES: Nothing relevant found in the documents."

    return "\n\n".join(
        f"{r.page_content}"
        for r in results
    )

# ==============================
# Agent
# ==============================
SYSTEM_RULES = """
You are a Medical Document Explainer Agent.

TASK:
- Answer questions only using uploaded medical documents
- Explain in VERY SIMPLE language
- Explain medicines, test results, and precautions
- If info is missing, say: "I don't see this information in the documents."

RULES:
- Use search_docs BEFORE answering
- Do NOT give medical advice
- Always end with:
  "This is NOT a substitute for a doctor's advice. Please consult a doctor."
"""

agent = initialize_agent(
    tools=[search_docs],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# ==============================
# Chat
# ==============================
def medical_chat(message, history):
    return agent.run(f"{SYSTEM_RULES}\n\nUser question: {message}")

# ==============================
# UI
# ==============================
with gr.Blocks() as demo:
    gr.Markdown("# 🩺 Medical Document Explainer")

    with gr.Tab("Upload"):
        files = gr.File(
            label="Upload Medical PDFs",
            file_types=[".pdf"],
            file_count="multiple"
        )
        b = gr.Button("Process", variant="primary")
        s = gr.Textbox(label="Status", lines=4, interactive=False)
        b.click(process_pdfs, files, s)

    with gr.Tab("Ask"):
        gr.ChatInterface(
            fn=medical_chat,
            examples=[
                "What does this medicine do?",
                "What precautions should I take?",
                "Explain the blood test results in simple words.",
                "Summarize the discharge advice."
            ]
        )

demo.launch(share=True)
