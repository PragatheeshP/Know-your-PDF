import tempfile
import streamlit as st

from rag.pdf_loader import extract_pdf
from rag.chunker import chunk_pages
from rag.embeddings import embed
from rag.vector_store import (
    create_collection,
    insert_chunks
)
from rag.retriever import search
from rag.llm import ask
st.set_page_config(
    page_title="Know your PDF",
    layout="wide"
)
st.title("📚 Know your PDF")
with st.sidebar:

    st.header("Quick Actions")

    if st.button("📄 Summarize"):
        st.session_state.quick_prompt = "Summarize this document in simple English."

    if st.button("⚠️ Risks & Red Flags"):
        st.session_state.quick_prompt = """
Analyze this document and identify:

- High-risk clauses
- Hidden liabilities
- Unfair terms
- Missing protections
- Potential legal concerns

Include page references.
"""

    if st.button("📝 Key Clauses"):
        st.session_state.quick_prompt = """
Extract the most important clauses from this document.

For each clause:
- Explain it
- Mention why it matters
- Include page number
"""

    if st.button("❓ Questions Before Signing"):
        st.session_state.quick_prompt = """
Generate important questions the user should ask before signing this document.
"""

    if st.button("👶 Explain Simply"):
        st.session_state.quick_prompt = """
Explain this document as if I have no legal background.
"""
    if st.button("New Chat"):

        st.session_state.messages = []

        st.rerun()
uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)

if uploaded_file:
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp:
        tmp.write(
            uploaded_file.read()
        )
        pdf_path = tmp.name
    pages = extract_pdf(pdf_path)
    chunks = chunk_pages(pages)
    embeddings = embed(
        [
            chunk["text"]
            for chunk in chunks
        ]
    )

    create_collection()
    insert_chunks(
        chunks,
        embeddings
    )
    st.success(
        f"Indexed {len(chunks)} chunks"
    )
    # Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    prompt = st.session_state.pop(
        "quick_prompt",
        None
    ) or st.chat_input( 
    prompt = st.chat_input(
        "Ask a question about your PDF"
    )
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        query_vector = embed(
            [prompt]
        )[0]

        results = search(query_vector)
        answer = ask(
            prompt,
            results,
            st.session_state.messages
        )
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):
            st.markdown(answer)
            if results:
                st.markdown("### Sources")

                for result in results:
                    st.markdown(
                        f"- Page {result.payload['page']}"
                    )
