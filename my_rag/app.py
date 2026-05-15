import streamlit as st
from src.rag import RAGPipeline
from pathlib import Path
import time

st.set_page_config(
    page_title="RAG System",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

def inject_custom_css(theme='dark'):
    if theme == 'dark':
        bg_gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        text_color = "#ffffff"
        secondary_bg = "rgba(255, 255, 255, 0.05)"
        border_color = "rgba(255, 255, 255, 0.1)"
        accent_gradient = "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
    else:
        bg_gradient = "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)"
        text_color = "#1a1a1a"
        secondary_bg = "rgba(0, 0, 0, 0.03)"
        border_color = "rgba(0, 0, 0, 0.1)"
        accent_gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"

    css = f"""
    <style>
    :root {{
        --bg-gradient: {bg_gradient};
        --text-color: {text_color};
        --secondary-bg: {secondary_bg};
        --border-color: {border_color};
        --accent-gradient: {accent_gradient};
    }}

    .stApp {{
        background: var(--bg-gradient);
        background-attachment: fixed;
    }}

    .stChatMessage {{
        background: var(--secondary-bg);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid var(--border-color);
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}

    .stChatMessage:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }}

    .stButton > button {{
        background: var(--accent-gradient);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}

    .stButton > button:hover {{
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }}

    .stTextInput > div > div > input {{
        border-radius: 10px;
        border: 2px solid var(--border-color);
        background: var(--secondary-bg);
        transition: border-color 0.3s ease;
    }}

    .stTextInput > div > div > input:focus {{
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }}

    .stSlider > div > div > div {{
        background: var(--accent-gradient);
    }}

    .stExpander {{
        background: var(--secondary-bg);
        border-radius: 10px;
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }}

    .stMetric {{
        background: var(--secondary-bg);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid var(--border-color);
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .stChatMessage {{
        animation: fadeIn 0.3s ease;
    }}

    h1, h2, h3 {{
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

@st.cache_resource
def get_rag_pipeline():
    return RAGPipeline()

def main():
    rag = get_rag_pipeline()

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'

    inject_custom_css(st.session_state.theme)

    col1, col2 = st.columns([6, 1])
    with col1:
        st.title("🔮 RAG System")
        st.markdown("*Retrieval-Augmented Generation with Local Models*")
    with col2:
        if st.button("🌓" if st.session_state.theme == 'dark' else "🌞"):
            st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
            st.rerun()

    with st.sidebar:
        st.header("⚙️ Settings")

        st.subheader("Retrieval")
        top_k = st.slider("Top-K Results", 1, 10, 5)
        similarity_threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.3, 0.05)

        st.subheader("Generation")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
        max_tokens = st.slider("Max Tokens", 128, 1024, 512, 64)

        st.divider()

        st.subheader("📚 Document Library")
        stats = rag.get_stats()
        st.metric("Total Chunks", stats['document_count'])
        st.metric("Unique Sources", len(stats['sources']))

        if stats['sources']:
            with st.expander("View Sources"):
                for source in stats['sources']:
                    st.text(Path(source).name)

        st.divider()

        st.subheader("📤 Upload Documents")
        uploaded_files = st.file_uploader(
            "Upload PDF, TXT, or MD files",
            type=['pdf', 'txt', 'md'],
            accept_multiple_files=True
        )

        if uploaded_files:
            if st.button("Ingest Files"):
                with st.spinner("Processing files..."):
                    success_count = 0
                    for uploaded_file in uploaded_files:
                        temp_path = Path(f"./data/documents/uploads/{uploaded_file.name}")
                        temp_path.parent.mkdir(parents=True, exist_ok=True)

                        with open(temp_path, 'wb') as f:
                            f.write(uploaded_file.getbuffer())

                        if rag.ingest_file(str(temp_path)):
                            success_count += 1

                    st.success(f"✓ Ingested {success_count}/{len(uploaded_files)} files")
                    st.rerun()

        if st.button("🗑️ Clear Database"):
            rag.clear_database()
            st.success("Database cleared!")
            st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📎 Sources"):
                    for i, source in enumerate(message["sources"], 1):
                        st.caption(f"{i}. {Path(source['source']).name} (similarity: {source['similarity_score']:.3f})")

    if prompt := st.chat_input("Ask a question about your documents..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            try:
                result = rag.query(
                    query=prompt,
                    top_k=top_k,
                    similarity_threshold=similarity_threshold,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True
                )

                if "error" in result:
                    response = result['response']
                    message_placeholder.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    full_response = ""
                    for chunk in result['stream']:
                        full_response += chunk
                        message_placeholder.markdown(full_response + "▌")

                    message_placeholder.markdown(full_response)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": full_response,
                        "sources": result.get('context_chunks', [])
                    })

                    with st.expander("📎 Sources"):
                        for i, chunk in enumerate(result.get('context_chunks', []), 1):
                            st.caption(f"{i}. {Path(chunk['source']).name} (similarity: {chunk['similarity_score']:.3f})")

            except Exception as e:
                error_msg = f"Error: {str(e)}"
                message_placeholder.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main()
