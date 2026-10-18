# Research Desk: Multi-Agent AI Research Assistant

Research Desk is an AI-powered research assistant that transforms a topic into a structured, source-backed research report. It uses four cooperating AI stages: Search, Reader, Writer, and Critic.

Built with Python, LangChain, Google Gemini, Tavily, and Streamlit, the project automates web research, webpage extraction, report generation, and quality review through an interactive web application or command-line workflow.

**Live Demo:** [Research Desk](https://multi-agent-ai-v5erfwsyrbxzcvyxfehxyk.streamlit.app/)

**GitHub Repository:** [multi-agent-ai](https://github.com/piyushrya/multi-agent-ai)

## Features

- **Multi-Agent Research Workflow:** Four stages work together to search, read, write, and review research.
- **Web Search:** Uses the Tavily API to discover relevant sources.
- **Webpage Extraction:** Uses Requests and BeautifulSoup to extract readable content from webpages.
- **Structured Reports:** Generates reports with an introduction, key findings, conclusion, and sources.
- **AI-Powered Critic:** Reviews the report and provides a score, strengths, areas for improvement, and a verdict.
- **Interactive Dashboard:** Built with Streamlit, featuring progress updates, research history, and tabbed results.
- **Downloadable Results:** Download the final report, critic review, search results, and extracted source notes.
- **Command-Line Interface:** Run research from the terminal and save the output to `research_report.txt`.

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
Research Report + Quality Review
      |
      v
Streamlit Dashboard / Command Line
```

| Stage | Component | Responsibility |
|---|---|---|
| 1 | Search Agent | Finds relevant web sources and collects search results. |
| 2 | Reader Agent | Extracts useful information from selected webpages. |
| 3 | Writer | Generates a structured research report from the collected information. |
| 4 | Critic | Reviews the report and identifies strengths and areas for improvement. |

The prompts encourage the agents to avoid inventing facts or sources and to acknowledge insufficient evidence. AI-generated information should still be verified against the original sources.

## Technology Stack

- **Programming Language:** Python
- **Large Language Model:** Google Gemini
- **AI Agent Framework:** LangChain
- **Web Search:** Tavily Search API
- **Web Scraping:** Requests and BeautifulSoup
- **Frontend:** Streamlit
- **Environment Variables:** python-dotenv
- **Version Control:** Git and GitHub
- **Deployment:** Streamlit Community Cloud

## Project Structure

```text
multi-agent-ai/
├── app.py              # Streamlit web application
├── agents.py           # Agent setup, writer and critic chains
├── tools.py            # Web search and webpage scraping tools
├── main.py             # Command-line research workflow
├── pipeline.py         # Alternative research pipeline
├── requirements.txt    # Project dependencies
├── .env                # Local API keys (not committed)
├── .gitignore          # Files excluded from Git
└── README.md           # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.10 or a compatible version supported by the dependencies
- Google Gemini API key
- Tavily API key
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/piyushrya/multi-agent-ai.git
cd multi-agent-ai
```

### 2. Create a Virtual Environment

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

### 3. Install Dependencies

Make sure the dependency file is named `requirements.txt`.

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file in the project root and add your own API credentials:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Get your API keys here:

- Google Gemini: https://aistudio.google.com/apikey
- Tavily: https://tavily.com

**Security:** Never upload your real API keys to GitHub or share them publicly. Keep `.env` in your `.gitignore` file.

### 5. Run the Streamlit Application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

`http://localhost:8501`

### 6. Run the Command-Line Application

To run research from the terminal:

```bash
python main.py
```

Enter your research topic when prompted. The workflow generates a report and critic review and saves the output to `research_report.txt`.

## How to Use

1. Open the Research Desk application.
2. Enter the topic you want to research.
3. Select a research depth from the available options.
4. Start the research workflow.
5. Follow the progress through the four stages.
6. View the final report, critic review, search results, and extracted source content.
7. Download the results for future reference.

## Live Demo

Try the deployed application:

**[Launch Research Desk](https://multi-agent-ai-v5erfwsyrbxzcvyxfehxyk.streamlit.app/)**

The application is deployed using Streamlit Community Cloud.

## Limitations

- Research quality depends on the available web sources and AI-generated content.
- Some websites may block automated requests or require JavaScript.
- Extracted webpage content is limited to the first 3,000 characters per page.
- The critic reviews the generated report but does not independently verify every claim against original sources.
- Research history is stored in Streamlit session state and is not permanently saved to a database.
- API rate limits, network issues, or service interruptions may affect execution.

## Future Improvements

- Add more reliable source verification and claim-level citations.
- Introduce automated tests and research-quality benchmarks.
- Improve webpage extraction and URL validation.
- Add persistent storage for research history.
- Support PDF and DOCX report exports.
- Implement an optional report-revision cycle based on critic feedback.
- Add research caching to reduce repeated API calls.

## Author

**Piyush Arya**

GitHub: [@piyushrya](https://github.com/piyushrya)

## License

No license has been specified yet. Add a `LICENSE` file if you intend to distribute the project under a particular open-source license.
