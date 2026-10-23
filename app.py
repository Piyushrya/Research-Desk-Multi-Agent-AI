import os
import streamlit as st

# Load deployed Streamlit Secrets into environment variables
for key in ("TAVILY_API_KEY", "GOOGLE_API_KEY"):
    try:
        value = st.secrets.get(key)
        if value:
            os.environ[key] = str(value)
    except (KeyError, FileNotFoundError):
        pass
import time
import traceback
from datetime import datetime

import streamlit as st

from concurrent.futures import ThreadPoolExecutor, as_completed

from agents import critic_chain, writer_chain
from tools import search_web_direct, scrape_url_text


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
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root { --ink:#18233b; --muted:#71809a; --paper:#f5f7ff; --pink:#a78bfa; --line:#dfe6f4; --blue:#536dfe; }
    html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
    .stApp { background:radial-gradient(ellipse at 8% 5%,rgba(116,143,255,.12),transparent 30%),radial-gradient(ellipse at 92% 22%,rgba(168,139,250,.12),transparent 28%),#f6f8ff; color:var(--ink); }
    [data-testid="stHeader"] { background:rgba(246,248,255,.92); }
    [data-testid="stMainBlockContainer"] { max-width:1440px; padding:2rem clamp(1.25rem,3.2vw,3rem) 3rem !important; }
    [data-testid="stVerticalBlock"] { gap:1rem; }
    [data-testid="stSidebar"] { background:#fbfcff; border-right:1px solid #e1e7f5; }
    [data-testid="stSidebar"] * { color:#51484b; }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color:#a09698; }
    [data-testid="stSidebar"] hr { border-color:#f0e3e4; }
    h1,h2,h3 { font-family:'Manrope',sans-serif !important; color:#292528 !important; letter-spacing:-.7px; }
    p,li,label { color:#756b6e; }
    .announcement { margin:-4.2rem -1rem 0; padding:9px 16px; background:linear-gradient(90deg,#536dfe,#9272f5,#47b8df); color:white; text-align:center; font-size:10px; letter-spacing:1.5px; font-weight:700; }
    .site-nav { display:flex; align-items:center; justify-content:space-between; gap:18px; padding:19px 2px 18px; color:#293752; font-size:11px; letter-spacing:.25px; border-bottom:1px solid #e2e8f5; margin-bottom:18px; }
    .site-logo { font-family:'Manrope',sans-serif; font-size:21px; font-weight:800; letter-spacing:-1.3px; color:#292326; }
    .site-logo span { color:#6578ff; }
    .nav-links { display:flex; gap:23px; align-items:center; color:#52617e; } .nav-links a { color:inherit; text-decoration:none; font-weight:600; transition:color .2s,transform .2s; } .nav-links a:hover { color:#536dfe; transform:translateY(-1px); }
    .nav-contact { border:1px solid #dce3f3; padding:8px 13px; border-radius:30px; color:#425174; background:rgba(255,255,255,.7); }
    .hero { position:relative; isolation:isolate; overflow:hidden; min-height:455px; display:flex; align-items:center; padding:clamp(2rem,5vw,4.2rem); margin:0 0 2.3rem; color:white; background-image:radial-gradient(circle at 78% 28%,rgba(105,130,255,.32),transparent 23%),radial-gradient(circle at 88% 82%,rgba(111,76,220,.30),transparent 28%),linear-gradient(118deg,#080f26 0%,#111d43 48%,#20265b 100%); background-size:cover; background-position:center; box-shadow:0 18px 50px rgba(47,65,130,.17); border-radius:8px; }
    .hero:after { content:''; position:absolute; z-index:-1; right:5%; top:8%; width:310px; height:310px; border:1px solid rgba(166,190,255,.6); border-radius:50%; box-shadow:0 0 0 24px rgba(135,157,255,.10),0 0 0 54px rgba(135,157,255,.08),0 0 0 90px rgba(135,157,255,.05); }
    .hero-content { position:relative; z-index:1; max-width:680px; }
    .hero-topline { display:inline-flex; align-items:center; gap:9px; color:#fff; text-transform:uppercase; letter-spacing:2px; font-size:.64rem; font-weight:700; margin-bottom:1.5rem; }
    .hero-dot { width:7px; height:7px; border-radius:50%; background:#83e7ff; display:inline-block; box-shadow:0 0 14px #83e7ff; }
    .hero-title { color:#fff; font-family:'Manrope',sans-serif; font-size:clamp(2.8rem,6.2vw,5.3rem); font-weight:800; line-height:.98; letter-spacing:-3px; margin:0; max-width:700px; text-shadow:0 2px 20px rgba(0,0,0,.08); }
    .hero-title span { color:#a9c5ff; }
    .hero-description { color:rgba(255,255,255,.9); font-size:.9rem; line-height:1.8; max-width:470px; margin-top:1.2rem; }
    .hero-bottom { display:flex; flex-wrap:wrap; gap:9px; align-items:center; margin-top:1.5rem; color:white; font-size:.68rem; font-weight:600; }
    .hero-pill { border:1px solid rgba(255,255,255,.48); background:rgba(255,255,255,.13); padding:8px 12px; border-radius:30px; backdrop-filter:blur(8px); }
    .hero-note { margin-top:1.2rem; color:rgba(255,255,255,.78); font-size:.62rem; letter-spacing:1.5px; text-transform:uppercase; }
    .section-heading { font-family:'Manrope',sans-serif; font-size:1.45rem; font-weight:800; color:#292528; margin:1.8rem 0 1rem; letter-spacing:-.7px; }
    .section-heading span { color:#6578ff; }
    .agent-card { position:relative; background:rgba(255,255,255,.68); border:0; border-top:2px solid #8b9bff; border-radius:0; padding:1rem .4rem 1.2rem; min-height:145px; height:100%; box-shadow:none; transition:transform .2s ease; }
    .agent-card:hover { transform:translateY(-3px); }
    .agent-number { color:#6578ff; font-family:'Manrope',sans-serif; font-size:.82rem; font-weight:700; margin-bottom:1.15rem; letter-spacing:.6px; }
    .agent-name { color:#292528; font-weight:800; font-size:.93rem; margin-bottom:.45rem; }
    .agent-description { color:#8a7f82; font-size:.77rem; line-height:1.7; }
    [data-testid="stForm"] { border:1px solid #dce4f5; border-top:2px solid #6578ff; background:rgba(255,255,255,.88); border-radius:12px; padding:1.5rem 1.5rem 1.25rem !important; margin:.75rem 0 1.75rem; box-shadow:0 12px 32px rgba(46,64,120,.06); }
    [data-testid="stForm"] [data-testid="stVerticalBlock"] { gap:1.1rem; }
    [data-testid="stForm"] label { margin-bottom:.35rem; font-weight:600; color:#56627a; }
    [data-testid="stForm"] textarea { min-height:112px; padding:14px 16px !important; line-height:1.55; }
    [data-testid="stForm"] div[data-baseweb="select"] > div { min-height:48px; }
    [data-testid="stForm"] div.stFormSubmitButton > button { margin-top:.2rem; min-height:3.1rem; border-radius:7px; }
    [data-testid="stVerticalBlockBorderWrapper"] { border:0 !important; background:transparent !important; }
    .panel { border:1px solid #e0e7f7; background:#fff; border-radius:5px; padding:1.4rem; margin:.5rem 0 1rem; box-shadow:0 8px 24px rgba(40,20,30,.025); }
    .muted { color:#8a7f82; font-size:.88rem; }
    .status-line { color:#536dfe; font-size:.84rem; font-weight:700; }
    div.stButton > button[kind="primary"], div.stFormSubmitButton > button { background:linear-gradient(100deg,#536dfe,#8b6df0); border:1px solid #6578ff; color:#fff; border-radius:3px; font-weight:700; min-height:2.8rem; box-shadow:none; transition:all .2s ease; letter-spacing:.2px; }
    div.stButton > button[kind="primary"]:hover, div.stFormSubmitButton > button:hover { background:linear-gradient(100deg,#4059e8,#795be0); color:white; transform:translateY(-1px); border-color:#6578ff; }
    div.stDownloadButton > button { border-radius:3px; border:1px solid #eadcde; background:#fff; color:#493e42; font-weight:600; }
    div.stDownloadButton > button:hover { border-color:#e99aa5; color:#c86f7d; }
    .stTextInput input,.stTextArea textarea { background:#fff !important; color:#292528 !important; border:1px solid #eadcde !important; border-radius:3px !important; }
    div[data-baseweb="select"] > div { background:#fff; border-color:#eadcde; border-radius:3px; }
    [data-testid="stMetric"] { background:#fff; border:1px solid #f0e3e4; padding:1rem; border-radius:4px; box-shadow:none; }
    [data-testid="stMetricLabel"] { color:#8a7f82; }
    [data-testid="stMetricValue"] { color:#292528; }
    [data-testid="stTabs"] button { color:#8a7f82; }
    [data-testid="stTabs"] button[aria-selected="true"] { color:#ce7886; border-bottom-color:#f3a0ad; }
    hr { border-color:#f0e3e4; }
    .footer { text-align:center; color:#a09698; font-size:.68rem; padding:2rem 0 1rem; letter-spacing:.55px; line-height:2.1; }
    .footer a { color:#d87f8d; text-decoration:none; font-weight:700; }
    .footer a:hover { color:#b75f6e; text-decoration:underline; }
    @media (max-width:700px) { [data-testid="stMainBlockContainer"] { padding:1.25rem 1rem 2rem !important; } [data-testid="stForm"] { padding:1rem !important; margin:.5rem 0 1.25rem; } .announcement { margin-top:-4.2rem; } .site-nav { padding:15px 0; } .nav-links { gap:10px; } .hero { min-height:390px; padding:1.5rem; background-position:center; } .hero-title { letter-spacing:-1.8px; font-size:clamp(2.7rem,12vw,4rem); } .hero:after { right:-190px; } }
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


@st.cache_data(ttl=600, show_spinner=False)
def cached_search(topic, max_results):
    """Cache identical searches for 10 minutes."""
    return search_web_direct(topic, max_results=max_results)


@st.cache_data(ttl=1800, show_spinner=False)
def cached_scrape(url, max_chars):
    """Cache successfully retrieved page text for 30 minutes."""
    return scrape_url_text(url, max_chars=max_chars)


def run_pipeline(topic, depth, progress_bar, status_text):
    """Run a faster four-stage pipeline with direct search and parallel scraping."""
    start_time = time.perf_counter()
    stage_times = {}

    # Depth controls both the number of results and how many pages are read.
    settings = {
        "Quick overview": {"results": 3, "pages": 2, "chars": 2500},
        "Standard research": {"results": 5, "pages": 3, "chars": 3500},
        "Deep research": {"results": 8, "pages": 5, "chars": 4500},
    }
    config = settings.get(depth, settings["Standard research"])

    # Stage 1: Direct Tavily search (avoids an extra Gemini tool-planning call).
    status_text.markdown(
        '<p class="status-line">Stage 1 of 4: Searching the web</p>',
        unsafe_allow_html=True,
    )
    stage_start = time.perf_counter()
    search_results = cached_search(topic.strip(), config["results"])
    stage_times["Search"] = round(time.perf_counter() - stage_start, 1)

    search_blocks = []
    urls = []
    for item in search_results:
        title = str(item.get("title", "Untitled source"))
        url = str(item.get("url", ""))
        snippet = str(item.get("content", ""))[:700]
        search_blocks.append(f"Title: {title}\nURL: {url}\nSnippet: {snippet}")
        if url.startswith(("https://", "http://")) and url not in urls:
            urls.append(url)
    search_text = "\n\n---\n\n".join(search_blocks) or "No search results were returned."
    progress_bar.progress(25)

    # Stage 2: scrape only the top N URLs, concurrently.
    status_text.markdown(
        '<p class="status-line">Stage 2 of 4: Reading source webpages in parallel</p>',
        unsafe_allow_html=True,
    )
    stage_start = time.perf_counter()
    selected_urls = urls[:config["pages"]]
    scraped = {}
    if selected_urls:
        with ThreadPoolExecutor(max_workers=min(5, len(selected_urls))) as pool:
            future_to_url = {
                pool.submit(cached_scrape, url, config["chars"]): url
                for url in selected_urls
            }
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    scraped[url] = future.result()
                except Exception as exc:
                    scraped[url] = f"Could not read this source: {type(exc).__name__}: {exc}"
    reader_text = "\n\n".join(
        f"Source URL: {url}\nExtracted content:\n{scraped.get(url, 'No content returned.') }"
        for url in selected_urls
    ) or "No readable source URLs were found in the search results."
    stage_times["Reader"] = round(time.perf_counter() - stage_start, 1)
    progress_bar.progress(50)

    combined_research = (
        "WEB SEARCH RESULTS\n==================\n"
        f"{search_text}\n\nREAD SOURCE FINDINGS\n===================\n{reader_text}"
    )

    # Stage 3: Writer (one model call).
    status_text.markdown(
        '<p class="status-line">Stage 3 of 4: Writing the report</p>',
        unsafe_allow_html=True,
    )
    stage_start = time.perf_counter()
    report = writer_chain.invoke({"topic": topic, "research": combined_research})
    if not isinstance(report, str):
        report = str(report)
    stage_times["Writer"] = round(time.perf_counter() - stage_start, 1)
    progress_bar.progress(75)

    # Stage 4: Critic (kept so the existing review tab still works).
    status_text.markdown(
        '<p class="status-line">Stage 4 of 4: Reviewing report quality</p>',
        unsafe_allow_html=True,
    )
    stage_start = time.perf_counter()
    review = critic_chain.invoke({"report": report})
    if not isinstance(review, str):
        review = str(review)
    stage_times["Critic"] = round(time.perf_counter() - stage_start, 1)
    progress_bar.progress(100)

    return {
        "topic": topic,
        "depth": depth,
        "search": search_text,
        "sources": reader_text,
        "research": combined_research,
        "report": report,
        "review": review,
        "stage_times": stage_times,
        "duration": round(time.perf_counter() - start_time, 1),
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
            AI Research Studio
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
    st.markdown(
        '<div style="font-size:.75rem;color:#c7b8d8;margin-top:.6rem;line-height:1.8">Questions, discrepancies, or feedback?<br><a href="mailto:par305065@gmail.com" style="color:#ffe6a1;text-decoration:none;font-weight:700">par305065@gmail.com</a></div>',
        unsafe_allow_html=True,
    )


# ============================================================
# EDITORIAL WEBSITE HEADER
# ============================================================

st.markdown(
    """
    <div class="announcement">YOUR PERSONAL AI RESEARCH STUDIO &nbsp; · &nbsp; CLARITY THROUGH CURIOSITY</div>
    <div class="site-nav">
      <div class="site-logo">RE<span>·</span>SEARCH</div>
      <div class="nav-links"><a href="#how-it-works">How it works</a><a href="#research">Research</a><a href="#sources">Sources</a><a href="#about">About</a></div>
      <a class="nav-contact" href="mailto:par305065@gmail.com" style="text-decoration:none">Contact ↗</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-content">
            <div class="hero-topline"><span class="hero-dot"></span> GOOD QUESTIONS DESERVE BETTER ANSWERS</div>
            <div class="hero-title">Research<br>with <span>intelligence.</span></div>
            <div class="hero-description">
                An AI-powered research workspace that searches the web, reads source material, synthesizes findings, and reviews the final report—so you can move from question to insight.
            </div>
            <div class="hero-bottom">
                <span class="hero-pill">✦ Multi-agent workflow</span>
                <span class="hero-pill">↗ Web-grounded research</span>
                <span class="hero-pill">◎ AI-assisted synthesis</span>
            </div>
            <div class="hero-note">SEARCH · READ · SYNTHESIZE · REFINE</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# AGENT CARDS
# ============================================================

st.markdown(
    '<div id="how-it-works" style="scroll-margin-top:24px"></div><div class="section-heading">How it <span>works</span></div>',
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
    '<div id="research" style="scroll-margin-top:24px"></div><div class="section-heading">Start your <span>research</span></div>',
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
            "Start Research",
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
        '<div id="sources" style="scroll-margin-top:24px"></div><div class="section-heading">Research results</div>',
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

    if result.get("stage_times"):
        with st.expander("Execution time by stage", expanded=False):
            timing_cols = st.columns(4)
            for col, stage_name in zip(timing_cols, ["Search", "Reader", "Writer", "Critic"]):
                col.metric(stage_name, f"{result['stage_times'].get(stage_name, 0)} sec")

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
            <div id="sources" style="scroll-margin-top:24px"></div><div class="section-heading">Your reports will appear here</div>
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
    <div id="about" style="scroll-margin-top:24px"></div><div class="footer">
        RESEARCH DESK &nbsp;·&nbsp; AI MULTI-AGENT RESEARCH STUDIO<br>
        CREATED BY PIYUSH ARYA<br>
        For discrepancies, feedback, or any other queries, contact
        <a href="mailto:par305065@gmail.com">par305065@gmail.com</a>
    </div>
    """,
    unsafe_allow_html=True,
)
