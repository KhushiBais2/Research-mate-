
import os
import html
import hashlib
import streamlit as st

from src.rag_pipeline import process_document, answer_question


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ResearchMate | AI Research Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOGO_PATH = os.path.join(
    BASE_DIR,
    "assets",
    "researchmate_logo.png"
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "data",
    "uploaded_papers"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "paper_data" not in st.session_state:
    st.session_state.paper_data = None

if "file_hash" not in st.session_state:
    st.session_state.file_hash = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# --------------------------------------------------
# CUSTOM CSS - LIGHT THEME WITH BLUE ACCENT
# --------------------------------------------------

st.markdown(
    """
    <style>

    /* Main application */
    .stApp {
        background-color: #F8FAFC !important;
        color: #1E293B !important;
    }

    /* Main content */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* General headings */
    h1, h2, h3, h4 {
        color: #1E293B !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #1E293B !important;
    }

    /* Sidebar description */
    .sidebar-description {
        color: #64748B !important;
        font-size: 13px !important;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 15px;
        line-height: 1.5;
    }

    /* Sidebar logo */
    section[data-testid="stSidebar"] img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    /* Sidebar navigation */
    section[data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 10px !important;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        font-size: 17px !important;
        font-weight: 500 !important;
        padding: 9px 8px !important;
        min-height: 44px;
        border-radius: 8px;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background-color: #EFF6FF !important;
    }

    /* Dashboard banner */
    .hero-banner {
        background: linear-gradient(
            120deg,
            #1D4ED8,
            #2563EB,
            #3B82F6
        );
        padding: 35px;
        border-radius: 18px;
        margin-bottom: 25px;
    }

    .hero-banner h1 {
        color: #FFFFFF !important;
        font-size: 34px;
        margin-bottom: 10px;
    }

    .hero-banner p {
        color: #DBEAFE !important;
        font-size: 16px;
    }

    /* Feature cards */
    .feature-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 22px;
        min-height: 150px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }

    .feature-card h3 {
        color: #1D4ED8 !important;
        font-size: 18px;
    }

    .feature-card p {
        color: #64748B !important;
        font-size: 14px;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        padding: 18px;
        border-radius: 12px;
    }

    div[data-testid="stMetricLabel"] {
        color: #64748B !important;
    }

    div[data-testid="stMetricValue"] {
        color: #1D4ED8 !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px;
        padding: 9px 20px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #1D4ED8 !important;
        color: #FFFFFF !important;
    }

    /* Text area */
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
    }

    .stTextArea textarea::placeholder {
        color: #94A3B8 !important;
    }

    /* File uploader */
    div[data-testid="stFileUploader"] {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
    }

    div[data-testid="stFileUploader"] button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
    }

    div[data-testid="stFileUploader"] button span,
    div[data-testid="stFileUploader"] button p {
        color: #FFFFFF !important;
    }

    div[data-testid="stFileUploader"] button svg {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
    }

    div[data-testid="stFileUploader"] button:hover {
        background-color: #1D4ED8 !important;
    }

    div[data-testid="stFileUploader"] section {
        background-color: #FFFFFF !important;
        border: 1px dashed #93C5FD !important;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
    }

    /* Chat message containers */
    div[data-testid="stChatMessage"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 15px;
    }

    /* FIX: Chat text visibility */
    div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
    div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
    div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] span,
    div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong,
    div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
    div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] em,
    div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h1,
    div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h2,
    div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h3 {
        color: #1E293B !important;
    }

    /* Expander text */
    div[data-testid="stExpander"] [data-testid="stMarkdownContainer"],
    div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p,
    div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] span {
        color: #1E293B !important;
    }

    /* Source text */
    .source-text {
        background-color: #F1F5F9 !important;
        color: #1E293B !important;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #CBD5E1;
        font-size: 14px;
        line-height: 1.7;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
    }

    .source-text * {
        color: #1E293B !important;
    }

    /* Source heading */
    .source-heading {
        color: #1D4ED8 !important;
        font-weight: 600;
        margin-bottom: 8px;
    }

    /* Divider */
    hr {
        border-color: #E2E8F0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HELPER FUNCTION - DISPLAY SOURCES
# --------------------------------------------------

def display_sources(sources):

    if not sources:
        st.info("No source information available.")
        return

    for i, source in enumerate(sources, start=1):

        page = source.get("page", "N/A")
        score = source.get("score", 0)

        source_text = html.escape(
            source.get("text", "").strip()
        )

        with st.expander(
            f"Source {i} | Page {page} | Similarity Score: {score:.3f}"
        ):

            st.markdown(
                '<p class="source-heading">Retrieved Text</p>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="source-text">{source_text}</div>',
                unsafe_allow_html=True
            )


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    # Display logo
    if os.path.exists(LOGO_PATH):

        st.image(
            LOGO_PATH,
            width=220
        )

    else:

        st.warning("ResearchMate logo not found.")

    # Description
    st.markdown(
        """
        <div class="sidebar-description">
            Your AI-powered research paper assistant
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # Navigation
    selected_page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📄 Research Workspace",
            "💬 Previous Results"
        ],
        label_visibility="collapsed"
    )


# --------------------------------------------------
# DASHBOARD PAGE
# --------------------------------------------------

if selected_page == "🏠 Dashboard":

    st.markdown(
        """
        <div class="hero-banner">
            <h1>Welcome to ResearchMate 📚</h1>
            <p>
                Understand research papers faster with AI-powered
                question answering and semantic search.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## Your Research Workspace")

    st.write(
        "Upload a research paper, ask questions, and get "
        "context-aware answers directly from your document."
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="feature-card">
                <h3>📄 PDF Analysis</h3>
                <p>
                    Upload research papers and automatically
                    extract their text for analysis.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="feature-card">
                <h3>🔍 Semantic Search</h3>
                <p>
                    Find relevant information using embeddings
                    and FAISS similarity search.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="feature-card">
                <h3>🤖 AI Answers</h3>
                <p>
                    Ask questions and receive answers generated
                    by the local Qwen language model.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    st.markdown("## Workspace Overview")

    metric1, metric2, metric3 = st.columns(3)

    with metric1:

        st.metric(
            "Total Conversations",
            len(st.session_state.chat_history)
        )

    with metric2:

        document_status = (
            "Uploaded"
            if st.session_state.paper_data is not None
            else "Not Uploaded"
        )

        st.metric(
            "Document Status",
            document_status
        )

    with metric3:

        st.metric(
            "Current Document",
            st.session_state.file_name or "None"
        )


# --------------------------------------------------
# RESEARCH WORKSPACE PAGE
# --------------------------------------------------

elif selected_page == "📄 Research Workspace":

    st.title("📄 Research Workspace")

    st.write(
        "Upload your research paper and ask questions "
        "to understand its content."
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload Research Paper (PDF)",
        type=["pdf"],
        help="Upload a text-based PDF research paper."
    )

    # ----------------------------------------------
    # PROCESS UPLOADED PDF
    # ----------------------------------------------

    if uploaded_file is not None:

        file_bytes = uploaded_file.getvalue()

        current_hash = hashlib.sha256(
            file_bytes
        ).hexdigest()

        if current_hash != st.session_state.file_hash:

            os.makedirs(
                UPLOAD_FOLDER,
                exist_ok=True
            )

            pdf_path = os.path.join(
                UPLOAD_FOLDER,
                uploaded_file.name
            )

            with open(pdf_path, "wb") as file:
                file.write(file_bytes)

            with st.spinner(
                "Processing research paper... Please wait."
            ):

                try:

                    index, chunks = process_document(pdf_path)

                    st.session_state.paper_data = {
                        "index": index,
                        "chunks": chunks
                    }

                    st.session_state.file_hash = current_hash
                    st.session_state.file_name = uploaded_file.name

                    # Clear old chat when a new PDF is uploaded
                    st.session_state.chat_history = []

                    st.success(
                        "Research paper processed successfully!"
                    )

                except Exception as e:

                    st.error(
                        f"Error processing PDF: {str(e)}"
                    )

                    st.stop()

        else:

            st.success(
                f"Using cached document: {uploaded_file.name}"
            )

    elif st.session_state.paper_data is not None:

        st.info(
            f"Previously processed document: "
            f"{st.session_state.file_name}"
        )

    # ----------------------------------------------
    # QUESTION INPUT
    # ----------------------------------------------

    st.divider()

    st.markdown("### 💬 Ask a Question")

    query = st.text_area(
        "Enter your question",
        placeholder=(
            "Example: Explain the types of machine learning "
            "discussed in this research paper."
        ),
        height=110
    )

    generate_button = st.button(
        "Generate Answer",
        use_container_width=True
    )

    # ----------------------------------------------
    # GENERATE ANSWER
    # ----------------------------------------------

    if generate_button:

        if st.session_state.paper_data is None:

            st.warning(
                "Please upload a research paper first."
            )

        elif not query.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            index = st.session_state.paper_data["index"]
            chunks = st.session_state.paper_data["chunks"]

            with st.spinner(
                "Searching the research paper and generating your answer..."
            ):

                try:

                    answer, sources = answer_question(
                        query,
                        index,
                        chunks,
                        top_k=3
                    )

                    st.session_state.chat_history.append(
                        {
                            "question": query,
                            "answer": answer,
                            "sources": sources
                        }
                    )

                except Exception as e:

                    st.error(
                        f"Error generating answer: {str(e)}"
                    )

    # ----------------------------------------------
    # DISPLAY CHAT HISTORY
    # ----------------------------------------------

    if st.session_state.chat_history:

        st.divider()

        st.markdown("## Conversation")

        for chat in st.session_state.chat_history:

            with st.chat_message("user"):

                st.markdown("**Your Question**")
                st.write(chat["question"])

            with st.chat_message("assistant"):

                st.markdown("**ResearchMate Answer**")
                st.markdown(chat["answer"])

                with st.expander("📚 View Sources"):

                    display_sources(
                        chat.get("sources", [])
                    )

        st.write("")

        if st.button(
            "🗑️ Clear Chat",
            use_container_width=True
        ):

            st.session_state.chat_history = []
            st.rerun()


# --------------------------------------------------
# PREVIOUS RESULTS PAGE
# --------------------------------------------------

elif selected_page == "💬 Previous Results":

    st.title("💬 Previous Results")

    st.write(
        "View your previously generated answers "
        "and their supporting research paper sources."
    )

    st.divider()

    if not st.session_state.chat_history:

        st.info(
            "No previous results available. "
            "Go to Research Workspace and ask a question."
        )

    else:

        st.success(
            f"{len(st.session_state.chat_history)} "
            "conversation(s) found."
        )

        for i, chat in enumerate(
            reversed(st.session_state.chat_history),
            start=1
        ):

            with st.expander(
                f"Conversation {i}: {chat['question']}"
            ):

                st.markdown("### Question")

                st.write(chat["question"])

                st.markdown("### ResearchMate Answer")

                st.markdown(chat["answer"])

                st.markdown("### 📚 Sources")

                display_sources(
                    chat.get("sources", [])
                )

        st.divider()

        if st.button(
            "🗑️ Clear Chat History",
            use_container_width=True
        ):

            st.session_state.chat_history = []
            st.rerun()
