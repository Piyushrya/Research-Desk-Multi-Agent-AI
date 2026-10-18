# Research Desk: Multi-Agent AI Research Assistant

Research Desk is an AI-powered research assistant that transforms a topic into a structured research report using four AI stages: Search, Reader, Writer, and Critic.

Built with Python, LangChain, Google Gemini, Tavily, and Streamlit, it automates web research, content extraction, report generation, and quality review.

## Features

- **Multi-Agent Workflow:** Four stages collaborate to research and review a topic.
- **Web Search:** Finds relevant sources using Tavily.
- **Content Extraction:** Retrieves webpage content using Requests and BeautifulSoup.
- **AI Report Generation:** Creates structured reports with key findings and sources.
- **Critic Review:** Evaluates reports and suggests improvements.
- **Streamlit Dashboard:** Displays progress, results, and research history.
- **Downloads:** Export reports, reviews, search results, and source notes.
- **CLI Support:** Run research from the terminal.

## How It Works

```text
Research Topic
      |
      v
Search Agent (Tavily)
      |
      v
Reader Agent (Web Scraping)
      |
      v
Writer (Google Gemini)
      |
      v
Critic (Google Gemini)
      |
      v
Research Report + Review
```

| Stage | Responsibility |
|---|---|
| Search | Finds relevant web sources. |
| Reader | Extracts webpage content. |
| Writer | Generates the research report. |
| Critic | Reviews the report and suggests improvements. |

AI-generated information should be checked against the original sources.

## Technology Stack

- Python
- LangChain
- Google Gemini
- Tavily Search API
- Requests and BeautifulSoup
- Streamlit
- python-dotenv

## Project Structure

```text
multi-agent-ai/
├── app.py              # Streamlit application
├── agents.py           # AI agents and report chains
├── tools.py            # Search and scraping tools
├── main.py             # CLI workflow
├── pipeline.py         # Alternative research pipeline
├── requirements.txt    # Dependencies
├── .env                # Local API credentials
├── .gitignore          # Excluded files
└── README.md           # Documentation
```

## Getting Started

### Prerequisites

- Python 3.10 or a compatible version
- Google Gemini API key
- Tavily API key

### 1. Set Up a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

Ensure your dependency file is named `requirements.txt`.

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Get your keys from:

- [Google AI Studio](https://aistudio.google.com/apikey)
- [Tavily](https://tavily.com)


### 4. Run the Application

Start the Streamlit dashboard:

```bash
python -m streamlit run app.py
```

Alternatively, run the command-line workflow:

```bash
python main.py
```

The CLI workflow saves its output to `research_report.txt`.

## Limitations

- Results depend on source quality and AI-generated content.
- Some websites may block automated scraping.
- Webpage extraction is limited to 3,000 characters per page.
- The critic does not independently verify every claim.
- Research history is temporary and not stored in a database.

## Future Improvements

- Improve source verification and citations.
- Add persistent research history.
- Support PDF and DOCX exports.
- Introduce automated testing and report revision.

## Author

**Piyush Arya**

## License

No license has been specified. Add a `LICENSE` file if you decide to publish the project under an open-source license.
