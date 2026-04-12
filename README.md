# LEX — Indian Law Query Assistant & Document Generator

A powerful AI-driven legal assistant for searching, interpreting Indian law, and **generating court-ready legal documents** (PDFs). Built with CrewAI's multi-agent architecture, it covers 23+ legal domains with automatic query routing, section-level citations, Supreme Court case references, and automated document generation from 16 LaTeX templates.

## ✨ Key Features

- 🏛️ **23+ Legal Domains** — From Constitution to Bankruptcy, all major Indian laws covered
- 🤖 **Intelligent Query Routing** — Router agent auto-classifies questions to the right specialist
- 📚 **Comprehensive Legal Database** — Indian legal codes, acts, and 23M+ Supreme Court case data
- ⚖️ **Section-Level Citations** — Precise article/section references with case law support
- 📄 **Automated Document Generation** — 16 professional LaTeX templates compiled to PDF
- 💬 **Interactive CLI** — Terminal-based Q&A with document generation
- 🌐 **Modern Web Interface** — Rich chat UI with dark mode, auto-expanding input, and PDF download
- 🔑 **5 Distributed API Keys** — Separate keys for routing, laws, Supreme Court, retry, and docs

## Architecture

```
User Query
    │
    ▼
┌──────────────────┐
│   Router Agent   │ ← GROQ_KEY_ROUTER
│  (Classification)│
└────────┬─────────┘
         │ Routes to 1 of 23 specialists
         ▼
┌──────────────────┐
│ Specialist Agent │ ← GROQ_KEY_LAWS / GROQ_KEY_SC / GROQ_KEY_RETRY
│ (IPC/CPC/CrPC…) │
└────────┬─────────┘
         │ Returns answer + category
         ▼
┌──────────────────┐      ┌──────────────────┐
│   User chooses   │─Yes─▶│  Doc Generator   │ ← GROQ_KEY_DOCS
│  "Generate Doc"  │      │ (JSON → LaTeX →  │
└──────────────────┘      │   pdflatex → PDF)│
                          └──────────────────┘
```

### Document Generation Pipeline

```
Template (*.tex)  →  Extract XXFIELDXX placeholders
                            │
User Query + AI Response  → LLM extracts field values as JSON
                            │
Python str.replace()      → Filled LaTeX source
                            │
pdflatex (MiKTeX)         → Final PDF
```

> **Key design**: The LLM **never touches LaTeX syntax**. It only outputs a JSON dict of field values. Python does the mechanical replacement, preventing template corruption.

## Legal Domains Covered

| Domain | Agent | JSON Data | Template |
|--------|-------|-----------|----------|
| Indian Constitution | Constitution Agent | `const.json` | `8.tex` (Child Custody) |
| Indian Penal Code (IPC) | IPC Agent | `ipc.json` | `1.tex` (Bail Petition) |
| Civil Procedure Code (CPC) | CPC Agent | `cpc.json` | `2.tex` (Civil Suit Plaint) |
| Criminal Procedure Code (CrPC) | CrPC Agent | `crpc.json` | `0.tex` (Anticipatory Bail) |
| Divorce Law | Divorce Agent | `div.json` | `6.tex` (Divorce Petition) |
| Environmental Law | Environment Agent | `environ.json` | `2.tex` (General Plaint) |
| Marriage Law | Marriage Agent | `mar.json` | `7.tex` (Maintenance u/s 125) |
| Motor Vehicle Act | MVA Agent | `mva.json` | `10.tex` (Accident Claim) |
| Evidence Act | Evidence Agent | `evid.json` | `3.tex` (FIR Proforma) |
| Administrative Law | Administrative Agent | `adm.json` | `2.tex` (General Plaint) |
| Banking Regulation | Banking Agent | `banking.json` | `9.tex` (Consumer Complaint) |
| Bankruptcy/Insolvency | Bankruptcy Agent | `bankruptcy.json` | `13.tex` (IBC Application) |
| Company Law | Company Law Agent | `cl.json` | `12.tex` (Mismanagement) |
| Copyright Law | Copyright Agent | `Copyright.json` | `14.tex` (IP Infringement) |
| Corporate Practice | Corporate Agent | `cpc.json` | `5.tex` (Breach of Contract) |
| Design Law | Design Agent | `design.json` | `14.tex` (IP Infringement) |
| Human Rights | Human Rights Agent | `human_rights.json` | `15.tex` (Writ Petition) |
| Information Technology | IT Agent | `it.json` | `2.tex` (General Plaint) |
| Minimum Wages Act | Min. Wages Agent | `MinimumWagesact.json` | `11.tex` (Labour Complaint) |
| Patent Law | Patent Agent | `patent.json` | `14.tex` (IP Infringement) |
| Property Law | Property Agent | `prop.json` | `4.tex` (Partition Suit) |
| Tax Law | Tax Agent | `tax.json` | `2.tex` (General Plaint) |
| Trademark Law | Trademark Agent | `trademarks.json` | `14.tex` (IP Infringement) |
| Supreme Court Cases | SC Search Tool | `supreme_court_cases.json` | — |

## Project Structure

```
Legal/
├── main.py                     # CLI entry point (interactive + single-query)
├── app.py                      # Flask web server (API + UI)
├── style2.html                 # Web chat UI (LEX — Legal AI)
├── crew.py                     # CrewAI crew config, routing, key distribution
├── agents.py                   # 23+ agent definitions
├── tasks.py                    # Task definitions for each specialist
├── tools.py                    # Custom JSON search tools per domain
│
├── doc_generator.py            # Document generation engine
│   ├── Template reading        #   Reads .tex files
│   ├── Placeholder extraction  #   Finds XXFIELDXX markers
│   ├── LLM JSON extraction     #   Gets field values from AI
│   ├── LaTeX escaping          #   Sanitizes special characters
│   └── PDF compilation         #   Runs pdflatex (MiKTeX)
│
├── latex-templates/            # 16 LaTeX document templates
│   ├── 0.tex                   #   CrPC Anticipatory Bail Application
│   ├── 1.tex                   #   IPC Bail Petition
│   ├── 2.tex                   #   CPC Civil Suit Plaint
│   ├── 3.tex                   #   FIR Proforma (Evidence Act)
│   ├── 4.tex                   #   Property Partition Suit
│   ├── 5.tex                   #   Breach of Contract Suit
│   ├── 6.tex                   #   Divorce Petition (Hindu Marriage Act)
│   ├── 7.tex                   #   Maintenance Application (u/s 125 CrPC)
│   ├── 8.tex                   #   Child Custody Petition
│   ├── 9.tex                   #   Consumer Complaint (Banking)
│   ├── 10.tex                  #   Motor Accident Compensation (MACT)
│   ├── 11.tex                  #   Labour / Minimum Wages Complaint
│   ├── 12.tex                  #   Corporate Mismanagement (Companies Act)
│   ├── 13.tex                  #   Insolvency Application (IBC 2016)
│   ├── 14.tex                  #   IP Infringement (TM/Patent/Copyright)
│   └── 15.tex                  #   Human Rights / Writ Petition
│
├── generated_docs/             # Output folder for generated PDFs
├── legal-data-extractor/       # Scripts to build/update SC case dataset
│
├── *.json                      # Legal data files (23 JSON databases)
├── supreme_court_cases.json    # 23MB Supreme Court case summaries
├── .env                        # API keys (not tracked in git)
├── pyproject.toml              # Project metadata and dependencies
├── requirements.txt            # Python package requirements
└── .gitignore
```

## Installation

### Prerequisites

- **Python 3.10+**
- **MiKTeX** (for `pdflatex` — required for document generation)
  - Download: https://miktex.org/download
  - During install, enable "Install missing packages on-the-fly"
- **pip** or **uv** package manager

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dheeraj-blip/Legal-ai.git
   cd Legal-ai
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   Or using uv:
   ```bash
   uv sync
   ```

4. **Configure API keys** — Create a `.env` file:
   ```env
   OPENAI_API_BASE=https://api.groq.com/openai/v1
   OPENAI_MODEL_NAME=llama-3.3-70b-versatile

   # 5 separate Groq API keys to distribute load
   GROQ_KEY_ROUTER=gsk_your_router_key_here
   GROQ_KEY_LAWS=gsk_your_laws_key_here
   GROQ_KEY_SC=gsk_your_supreme_court_key_here
   GROQ_KEY_RETRY=gsk_your_retry_key_here
   GROQ_KEY_DOCS=gsk_your_docs_key_here

   CREWAI_TRACING_DISABLED=true
   CREWAI_TELEMETRY_DISABLED=true
   ```

### API Key Distribution

| Key | Used By | Purpose |
|-----|---------|---------|
| `GROQ_KEY_ROUTER` | Router Agent | Query classification |
| `GROQ_KEY_LAWS` | Law Specialist Agents | Legal Q&A responses |
| `GROQ_KEY_SC` | Supreme Court Tool | Case law search |
| `GROQ_KEY_RETRY` | Failover / backup | Retry on rate limits |
| `GROQ_KEY_DOCS` | Document Generator | Extracting JSON field data for templates |

## Usage

### CLI — Interactive Mode

```bash
python main.py
# or
uv run python main.py
```

Ask questions continuously. After each AI response, you'll be prompted:
```
📄 Generate legal document? (y/n): y
✅ Document saved to: generated_docs/legal_doc_abc123.pdf
```

### CLI — Single Query

```bash
python main.py "What is the punishment for theft under IPC?"
```

### Web Interface

```bash
# Development
python app.py

# Production
waitress-serve --threads=4 --port=5000 app:app
```

Open `http://localhost:5000` — use the LEX chat UI. After each AI response, click **"Generate Document"** to download the PDF.

## Example Prompts

### Quick Questions (no document needed)
```
What are the Fundamental Rights under the Indian Constitution?
What constitutes an offense under Section 420 IPC?
How do I register a trademark in India?
What is the minimum wage in Delhi for semi-skilled workers?
```

### Document-Ready Prompts (include all details for PDF generation)
```
I need to file an anticipatory bail application. Petitioner: Rajesh Kumar Singh,
son of Late Shri Mahendra Singh, resident of 45-B, Sector 22, Dwarka, New Delhi
- 110075. FIR Number is 245/2026, PS Cr. No. 112/2026, registered at Hauz Khas
Police Station, New Delhi. Respondent: State of NCT of Delhi through SHO, Police
Station Hauz Khas. The alleged offence is under Section 420 (Cheating) of the
Indian Penal Code. My advocate is Mr. Sanjay Mehta, Bar Council enrollment
D/1234/2015. Today's date is 12th April 2026. Verification at New Delhi.
```

> **Tip**: The more specific details (names, dates, addresses, amounts) you include in your prompt, the more complete the generated PDF will be.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serves the web chat UI |
| `POST` | `/api/chat` | Send a legal query, get AI response + category |
| `POST` | `/api/generate-doc` | Generate PDF from query + response + category |

### POST `/api/chat`
```json
{ "query": "What is Section 420 IPC?" }
```
Response:
```json
{
  "response": "Section 420 of the IPC deals with cheating...",
  "category": "IPC",
  "disclaimer": true
}
```

### POST `/api/generate-doc`
```json
{
  "query": "I need a bail petition...",
  "response": "Based on the details provided...",
  "category": "CRPC"
}
```
Response: PDF file download

## Dependencies

### Core
- **crewai** — Multi-agent orchestration framework
- **crewai-tools** — Pre-built tools for CrewAI

### Web
- **flask** >= 3.1.3 — Web framework
- **flask-cors** >= 6.0.2 — CORS support
- **waitress** — Production WSGI server

### Document Generation
- **MiKTeX** (external) — LaTeX distribution with `pdflatex`

### Utilities
- **python-dotenv** — Environment variable management

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `pdflatex not found` | Install MiKTeX and add to PATH |
| `GROQ API key not found` | Check `.env` file has `GROQ_KEY_DOCS` set |
| `Rate limit exceeded` | Use separate API keys per component |
| `Template not found` | Ensure `latex-templates/` directory exists with `.tex` files |
| `Missing packages` in LaTeX | Run MiKTeX Console → Tasks → Refresh FNDB, then recompile |
| Input box not expanding | Clear browser cache, refresh `localhost:5000` |

## Development

### Adding a New Legal Domain

1. Create a JSON file with legal data (e.g., `newtopic.json`)
2. Create a search tool in `tools.py` (e.g., `NewTopicSearchTool`)
3. Create an agent in `agents.py` (e.g., `create_new_topic_agent()`)
4. Create a task in `tasks.py` (e.g., `create_new_topic_query_task()`)
5. Add routing in `crew.py` (`_resolve_category` + `_RUNNERS` dict)

### Adding a New Document Template

1. Create a `.tex` file in `latex-templates/` with `XXFIELDXX` placeholders
2. Map the category to the template in `doc_generator.py` → `CASE_TEMPLATE_MAP`
3. Test compilation: replace all placeholders with "Sample Text" and run `pdflatex`

### Placeholder Format

Templates use `XXFIELDXX` delimiters (not `{{}}` or `<<>>` which conflict with LaTeX):
```latex
\fillline{XXFIELDXXCOURT_NAMEXXFIELDXX}
```
The Python generator extracts field names via regex, sends them to the LLM, gets JSON back, and does `str.replace()`.

---

**Last Updated**: April 2026

**Technology Stack**: Python 3.10+ · CrewAI · Flask · LaTeX (MiKTeX) · Groq LLM (Llama 3.3 70B)

**Status**: Active Development
