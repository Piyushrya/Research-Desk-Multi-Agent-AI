# Research Desk: Multi-Agent AI Research Assistant

Research Desk is an AI-powered research assistant that transforms a topic into a structured, source-backed report using four AI stages: Search, Reader, Writer, and Critic.

Built with Python, LangChain, Google Gemini, Tavily, and Streamlit, it automates web research, content extraction, report generation, and quality review.

## Features

- **Multi-Agent Workflow:** Four stages handle search, reading, writing, and review.
- **Web Research:** Finds sources using Tavily and extracts content with BeautifulSoup.
- **Report Generation:** Creates structured reports with key findings and sources.
- **AI Review:** Evaluates reports and suggests improvements.
- **Streamlit Dashboard:** Displays progress, research history, and results.
- **Export Results:** Download reports, reviews, search results, and source notes.
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
| Reader | Extracts useful webpage content. |
| Writer | Generates the research report. |
| Critic | Reviews quality and suggests improvements. |

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
├── app.py              # Streamlit web application
├── agents.py           # AI agents and report generation
├── tools.py            # Search and scraping tools
├── main.py             # Command-line workflow
├── pipeline.py         # Alternative research pipeline
├── requirements.txt    # Dependencies
├── .env                # API keys (not committed)
├── .gitignore          # Git exclusions
└── README.md           # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.10 or a compatible version
- Google Gemini API key
- Tavily API key
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/piyushrya/multi-agent-ai.git
cd multi-agent-ai
```

### 2. Create a Virtual Environment

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Get your keys from [Google AI Studio](https://aistudio.google.com/apikey) and [Tavily](https://tavily.com).

**Security:** Never commit real API keys to GitHub. Add `.env` to `.gitignore`.

### 5. Run the Application

Start the Streamlit dashboard:

```bash
python -m streamlit run app.py
```

To run the command-line workflow instead:

```bash
python main.py
```

The CLI workflow saves its output to `research_report.txt`.

## How to Use

1. Enter a research topic.
2. Select the research depth.
3. Start the workflow.
4. Review the generated report, critic feedback, and sources.
5. Download the results.

## Limitations

- Results depend on source quality and AI-generated content.
- Some websites may block scraping.
- The critic does not independently verify every claim.

## Future Improvements

- Improve source verification and citations.
- Add persistent research history.
- Support PDF and DOCX exports.
- Add automated testing and report revision.

## Author

**Piyush Arya**

## License

No license has been specified yet. Add a `LICENSE` file if you choose to distribute the project under an open-source license.
