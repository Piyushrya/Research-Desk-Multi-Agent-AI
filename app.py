
import time
import traceback
from datetime import datetime

import streamlit as st

from agents import (
    build_reader_agent,
    build_search_agent,
    critic_chain,
    writer_chain,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Research Desk | AI Research Studio",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap'
    );

    :root {
        --background: #0b1020;
        --panel: #111a30;
        --panel-light: #17233d;
        --border: #263653;
        --text: #edf2ff;
        --muted: #9aa9c5;
        --accent: #a78bfa;
        --accent-blue: #7c9cff;
        --success: #54d6a0;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 85% 0%,
                rgba(124, 92, 230, 0.12),
                transparent 30%
            ),
            var(--background);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        background: #0e1629;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
    }

    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--text) !important;
        letter-spacing: -0.4px;
    }

    p, li, label {
        color: #d0d9ed;
    }

    .brand {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: 1px;
        color: #ffffff;
    }

    .brand-subtitle {
        color: var(--muted);
        font-size: 0.76rem;
        margin-top: 4px;
    }

    .hero {
        padding: 2.2rem 2rem;
        border: 1px solid var(--border);
        border-radius: 22px;
        background: linear-gradient(
            125deg,
            rgba(124, 92, 230, 0.17),
            rgba(17, 26, 48, 0.96) 48%,
            rgba(50, 91, 160, 0.12)
        );
        margin-bottom: 1.6rem;
    }

    .eyebrow {
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.72rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }

    .hero-title {
        color: white;
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(2rem, 4vw, 3.25rem);
        font-weight: 700;
        line-height: 1.12;
        letter-spacing: -1.5px;
        margin: 0;
    }

    .hero-description {
        color: #b4c1da;
        font-size: 1rem;
        line-height: 1.8;
        max-width: 760px;
        margin-top: 1rem;
    }

    .hero-credit {
        margin-top: 1.4rem;
        color: #c4b5fd;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 2px;
    }

    .section-heading {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #f4f6ff;
        margin: 1.3rem 0 0.8rem;
    }

    .agent-card {
        background: linear-gradient(
            150deg,
            #15213a,
            #10182b
        );
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.15rem;
        min-height: 168px;
        height: 100%;
    }

    .agent-number {
        color: var(--accent);
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .agent-name {
        color: #f1f5ff;
        font-weight: 700;
        font-size: 0.93rem;
        margin-bottom: 0.5rem;
    }

    .agent-description {
        color: var(--muted);
        font-size: 0.79rem;
        line-height: 1.6;
    }

    .panel {
        border: 1px solid var(--border);
        background: rgba(17, 26, 48, 0.88);
        border-radius: 16px;
        padding: 1.2rem;
        margin: 0.5rem 0 1rem;
    }

    .muted {
        color: var(--muted);
        font-size: 0.86rem;
    }

    .status-line {
        color: var(--success);
        font-size: 0.83rem;
        font-weight: 600;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(
            100deg,
            #8b5cf6,
            #647ff0
        );
        border: none;
        color: white;
        border-radius: 10px;
        font-weight: 700;
        min-height: 2.8rem;
    }

    div.stButton > button[kind="primary"]:hover {
        border: 1px solid #c4b5fd;
        color: white;
    }

    div.stDownloadButton > button {
        border-radius: 10px;
        border: 1px solid #4c5f85;
        background: #17233d;
        color: white;
    }

    div.stDownloadButton > button:hover {
        border-color: var(--accent);
        color: white;
    }

    .stTextInput input,
    .stTextArea textarea {
        background: #10192c !important;
        color: white !important;
        border-color: #344461 !important;
        border-radius: 10px !important;
    }

    div[data-baseweb="select"] > div {
        background: #10192c;
        border-color: #344461;
    }

    [data-testid="stMetric"] {
        background: #111a30;
        border: 1px solid var(--border);
        padding: 1rem;
        border-radius: 13px;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff;
    }

    hr {
        border-color: var(--border);
    }

    .footer {
        text-align: center;
        color: #7f8eaa;
        font-size: 0.75rem;
        padding: 2rem 0 1rem;
        letter-spacing: 0.5px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def to_text(value):
    """Convert model output into readable text."""

    if value is None:
        return ""

    if isinstance(value, str):
        return value

    if isinstance(value, list):
        parts = []

        for item in value:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(item.get("text", ""))
                else:
                    parts.append(str(item))
            else:
                parts.append(str(item))

        return "\n".join(parts)

    if hasattr(value, "content"):
        return to_text(value.content)

    return str(value)


def get_agent_response(result):
    """Extract the final message from a LangChain agent result."""

    if isinstance(result, dict):
        messages = result.get("messages", [])

        if messages:
            return to_text(messages[-1])

    return to_text(result)


def run_pipeline(topic, depth, progress_bar, status_text):
    """Run the search, reader, writer and critic stages."""

    start_time = time.time()

    search_agent = build_search_agent()
    reader_agent = build_reader_agent()

    research_prompt = f"""
Research topic: {topic}

Research depth: {depth}

Search for credible and relevant sources.
Include source titles, URLs, dates, findings, and limitations
where available. Do not invent sources or facts.
"""

    # Stage 1: Search
    status_text.markdown(
        '<p class="status-line">Stage 1 of 4: Searching the web</p>',
        unsafe_allow_html=True,
    )

    search_result = search_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": research_prompt,
                }
            ]
        }
    )

    search_text = get_agent_response(search_result)

    progress_bar.progress(25)

    # Stage 2: Read relevant webpages
    status_text.markdown(
        '<p class="status-line">Stage 2 of 4: Reading source webpages</p>',
        unsafe_allow_html=True,
    )

    reader_prompt = f"""
Research topic:
{topic}

Research depth:
{depth}

Search results:
{search_text}

Read up to five of the most relevant HTTP or HTTPS source URLs
from these search results using the scrape_url tool.

Prioritize sources that contain direct evidence relevant to the topic.
If a page cannot be read, report that limitation.
Return the source URL with each finding.
Do not invent information or claim you read a page if you did not.
"""

    reader_result = reader_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": reader_prompt,
                }
            ]
        }
    )

    reader_text = get_agent_response(reader_result)

    progress_bar.progress(50)

    # Stage 3: Write the report
    status_text.markdown(
        '<p class="status-line">Stage 3 of 4: Writing the report</p>',
        unsafe_allow_html=True,
    )

    combined_research = f"""
WEB SEARCH RESULTS
==================
{search_text}

READ SOURCE FINDINGS
===================
{reader_text}
"""

    report = writer_chain.invoke(
        {
            "topic": topic,
            "research": combined_research,
        }
    )

    report = to_text(report)

    progress_bar.progress(75)

    # Stage 4: Critic review
    status_text.markdown(
        '<p class="status-line">Stage 4 of 4: Reviewing report quality</p>',
        unsafe_allow_html=True,
    )

    review = critic_chain.invoke(
        {
            "topic": topic,
            "report": report,
            "research": combined_research,
        }
    )

    review = to_text(review)

    progress_bar.progress(100)

    return {
        "topic": topic,
        "depth": depth,
        "search": search_text,
        "sources": reader_text,
        "research": combined_research,
        "report": report,
        "review": review,
        "duration": round(time.time() - start_time, 1),
        "created_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
    }


# ============================================================
# SESSION STATE
# ============================================================

if "research_history" not in st.session_state:
    st.session_state.research_history = []

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand">RESEARCH DESK</div>
        <div class="brand-subtitle">
            AI Multi-Agent Research Studio
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### Workspace")
    st.write("Research Studio")
    st.caption("Four-stage research workflow")

    st.divider()

    st.markdown("### Session History")

    if not st.session_state.research_history:
        st.caption("Your completed research sessions will appear here.")

    for index, item in enumerate(
        reversed(st.session_state.research_history[-8:]),
        start=1,
    ):
        with st.expander(
            f"{item['topic'][:45]}",
            expanded=False,
        ):
            st.caption(item["created_at"])
            st.write(f"Research depth: {item['depth']}")
            st.write(f"Duration: {item['duration']} seconds")

            if st.button(
                "Open this report",
                key=f"history_{index}_{item['created_at']}",
            ):
                st.session_state.latest_result = item
                st.rerun()

    st.divider()

    if st.button("Clear session history", use_container_width=True):
        st.session_state.research_history = []
        st.session_state.latest_result = None
        st.rerun()

    st.caption("Created by Piyush Arya")


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">AI-powered research workspace</div>
        <div class="hero-title">
            Research smarter.<br>Write with evidence.
        </div>
        <div class="hero-description">
            An intelligent research studio that discovers web sources,
            reads relevant webpages, generates structured reports, and
            reviews the final output for quality.
        </div>
        <div class="hero-credit">CREATED BY PIYUSH ARYA</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# AGENT CARDS
# ============================================================

st.markdown(
    '<div class="section-heading">Your research team</div>',
    unsafe_allow_html=True,
)

agent_columns = st.columns(4)

agent_info = [
    (
        "01",
        "Search Agent",
        "Find relevant information and discover web sources.",
    ),
    (
        "02",
        "Reader Agent",
        "Read webpages and extract useful evidence.",
    ),
    (
        "03",
        "Writer Agent",
        "Turn research findings into a structured report.",
    ),
    (
        "04",
        "Critic Agent",
        "Evaluate clarity, evidence and completeness.",
    ),
]

for column, (number, name, description) in zip(
    agent_columns,
    agent_info,
):
    with column:
        st.markdown(
            f"""
            <div class="agent-card">
                <div class="agent-number">{number}</div>
                <div class="agent-name">{name}</div>
                <div class="agent-description">{description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# RESEARCH FORM
# ============================================================

st.markdown(
    '<div class="section-heading">Start a research session</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    with st.form("research_form"):
        topic = st.text_area(
            "Research topic",
            placeholder=(
                "Example: Compare recent developments in AI agents, "
                "their practical applications, limitations and future trends."
            ),
            height=120,
            max_chars=1500,
        )

        depth = st.selectbox(
            "Research depth",
            options=[
                "Quick overview",
                "Standard research",
                "Deep research",
            ],
            index=1,
        )

        submitted = st.form_submit_button(
            "Start Deep Research",
            type="primary",
            use_container_width=True,
        )


if submitted:
    if not topic.strip():
        st.warning("Enter a research topic before starting.")
    else:
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()

            with st.spinner("Running your research team..."):
                result = run_pipeline(
                    topic=topic.strip(),
                    depth=depth,
                    progress_bar=progress_bar,
                    status_text=status_text,
                )

            st.session_state.latest_result = result
            st.session_state.research_history.append(result)

            status_text.success(
                f"Research completed in {result['duration']} seconds."
            )

        except Exception as error:
            st.error(
                "The research pipeline could not be completed. "
                "Check the API key, model access, internet connection "
                "and installed packages."
            )

            with st.expander("Technical error details"):
                st.code(
                    f"{type(error).__name__}: {error}\n\n"
                    f"{traceback.format_exc()}"
                )


# ============================================================
# RESULTS DASHBOARD
# ============================================================

result = st.session_state.latest_result

if result:
    st.divider()

    st.markdown(
        '<div class="section-heading">Research results</div>',
        unsafe_allow_html=True,
    )

    st.markdown(f"## {result['topic']}")
    st.caption(
        f"Created {result['created_at']} | "
        f"Depth: {result['depth']} | "
        f"Duration: {result['duration']} seconds"
    )

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric("Pipeline stages", "4")
    metric2.metric("Execution time", f"{result['duration']} sec")
    metric3.metric("Report status", "Completed")

    report_tab, review_tab, search_tab, sources_tab = st.tabs(
        [
            "Final Report",
            "Critic Review",
            "Search Results",
            "Source Content",
        ]
    )

    with report_tab:
        st.markdown(result["report"])

        st.download_button(
            label="Download Report",
            data=result["report"],
            file_name="research_report.md",
            mime="text/markdown",
            key="download_final_report",
            use_container_width=True,
        )

    with review_tab:
        st.markdown(result["review"])

        st.download_button(
            label="Download Critic Review",
            data=result["review"],
            file_name="critic_review.md",
            mime="text/markdown",
            key="download_critic_review",
            use_container_width=True,
        )

    with search_tab:
        st.markdown("### Web search findings")
        st.markdown(result["search"])

        st.download_button(
            label="Download Search Results",
            data=result["search"],
            file_name="search_results.txt",
            mime="text/plain",
            key="download_search_results",
        )

    with sources_tab:
        st.markdown("### Extracted webpage content")
        st.markdown(result["sources"])

        st.download_button(
            label="Download Source Notes",
            data=result["sources"],
            file_name="source_notes.txt",
            mime="text/plain",
            key="download_source_notes",
        )

else:
    st.markdown(
        """
        <div class="panel">
            <div class="section-heading">Your reports will appear here</div>
            <p class="muted">
                Enter a research topic above to start the four-stage
                workflow. When processing finishes, your report, critic
                review, search findings and extracted source notes will
                appear in this workspace.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        RESEARCH DESK &nbsp; | &nbsp;
        AI MULTI-AGENT RESEARCH STUDIO<br><br>
        CREATED BY PIYUSH ARYA
    </div>
    """,
    unsafe_allow_html=True,
)
