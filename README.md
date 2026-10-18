# Research Desk: Multi-Agent AI Research Assistant

Research Desk takes a topic and produces a structured, source-backed research report. Four cooperating AI agents handle the work: one searches the web, one reads the pages, one writes the report, and one reviews it. You can use it from a Streamlit web app or from the terminal.

<!-- Add a screenshot or GIF here, e.g. ![Research Desk UI](assets/demo.png) -->

## How it works

```
Topic ──► Search Agent ──► Reader Agent ──► Writer ──► Critic ──► Report + Review
          (Tavily)         (scrapes URLs)   (Gemini)   (Gemini)
```

| Stage | Component | What it does |
|-------|-----------|--------------|
| 1 | Search Agent | Uses the Tavily API to find relevant sources and keeps their URLs |
| 2 | Reader Agent | Scrapes the top pages and extracts facts, dates and evidence |
| 3 | Writer Chain | Writes a report: Introduction, Key Findings, Conclusion, Sources |
| 4 | Critic Chain | Scores the report out of 10 and lists strengths and improvements |

The prompts tell the agents not to invent sources or facts, and to say so when evidence is thin or conflicting.

## Features

- Four-stage multi-agent workflow built with LangChain and LangGraph
- Live web search (Tavily) and webpage scraping (BeautifulSoup)
- Streamlit interface with progress updates, session history and tabbed results (report, critic review, search results, source notes)
- Download the report, review and source notes
- Command-line mode that saves the result to `research_report.txt`

## Tech stack

Python, LangChain, LangGraph, Google Gemini (`langchain-google-genai`), Tavily, BeautifulSoup, Requests, Streamlit

## Project structure

```
.
├── agents.py          # LLM setup, search/reader agents, writer and critic chains
├── tools.py           # web_search (Tavily) and scrape_url tools
├── app.py             # Streamlit web app
├── main.py            # CLI version; saves output to research_report.txt
├── pipeline.py        # Simple step-by-step pipeline with printed output
├── requirements.txt   # Dependencies
└── .env               # API keys (not committed)
```

## Getting started

### 1. Clone and install

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Add your API keys

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

- Gemini key: https://aistudio.google.com/apikey
- Tavily key: https://tavily.com

### 3. Run it

**Web app**

```bash
streamlit run app.py
```

**Terminal**

```bash
python main.py
```

## Example

Enter a topic such as:

> Recent developments in AI agents, their practical applications and limitations

The app searches, reads the top sources, writes a structured report with a source list, and shows the critic's score and feedback.

## Limitations

- Report quality depends on the sources Tavily returns and on which pages can be scraped. Some sites block scraping or need JavaScript.
- Each scraped page is truncated to 3,000 characters, so very long articles are only partly read.
- The critic reviews the report text only. It does not re-check claims against the original sources.
- Session history in the web app is kept in memory and is lost on refresh.

## Possible improvements

- Cache searches and scraped pages
- Export reports to PDF or DOCX
- Let the critic's feedback trigger a rewrite loop
- Stream the report as it is written

## Author

**Piyush Arya**

## License

Add a license file (for example MIT) and state it here.
