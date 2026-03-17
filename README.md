# Indian Law Query Assistant

A powerful AI-driven query system for searching and interpreting Indian legal documents using CrewAI. This assistant leverages multi-agent systems to provide accurate, well-referenced answers across various domains of Indian law.

## Overview

The Indian Law Query Assistant uses CrewAI's multi-agent architecture to handle complex legal queries. A router agent automatically classifies user questions and directs them to the appropriate legal specialist agent, which searches through comprehensive JSON databases of Indian laws and codes.

**Key Features:**
- 🏛️ Multi-domain legal expertise (23+ legal areas)
- 🤖 AI-powered query routing and responses
- 📚 Comprehensive coverage of Indian legal codes and acts
- ⚖️ Accurate section/article-level citations
- 💬 Interactive and command-line interfaces
- 🌐 Flask-based web API capabilities

## Legal Domains Covered

| Domain | JSON File | Coverage |
|--------|-----------|----------|
| Indian Constitution | `const.json` | Constitutional articles and provisions |
| Indian Penal Code | `ipc.json` | Criminal offenses and penalties |
| Civil Procedure Code | `cpc.json` | Civil litigation procedures |
| Criminal Procedure Code | `crpc.json` | Criminal procedures |
| Divorce Law | `div.json` | Marriage dissolution and related matters |
| Environmental Law | `environ.json` | Environmental protection regulations |
| Marriage Law | `mar.json` | Marriage rights and regulations |
| Motor Vehicle Act | `mva.json` | Vehicle-related regulations |
| Evidence Act | `evid.json` | Rules of evidence in legal proceedings |
| Administrative Law | `adm.json` | Administrative procedures |
| Banking Regulation | `banking.json` | Banking sector regulations |
| Bankruptcy Law | `bankruptcy.json` | Insolvency and bankruptcy proceedings |
| Company Law | `cl.json` | Corporate governance and regulations |
| Copyright Law | `Copyright.json` | Intellectual property - copyrights |
| Corporate Practice | `cpc.json` | Corporate legal practices |
| Design Law | `design.json` | Design protection and registration |
| Human Rights | `human_rights.json` | Fundamental rights and protections |
| Information Technology | `it.json` | IT regulations and cyber laws |
| Minimum Wages Act | `MinimumWagesact.json` | Wage protection regulations |
| Patent Law | `patent.json` | Intellectual property - patents |
| Property Law | `prop.json` | Real and personal property rights |
| Tax Law | `tax.json` | Income tax and taxation regulations |
| Trademark Law | `trademarks.json` | Trademark protection and registration |

## Project Structure

```
legal/
├── main.py                 # Entry point (interactive and CLI modes)
├── agents.py              # Agent definitions for all legal domains
├── crew.py                # CrewAI crew configuration and orchestration
├── tasks.py               # Task definitions for each specialist
├── tools.py               # Custom search tools for each legal domain
├── pyproject.toml         # Project metadata and dependencies
├── requirements.txt       # Python package requirements
├── *.json                 # Legal data files (constitution, codes, acts)
├── style2.html            # HTML styling for web interface
└── .env                   # Environment configuration (not tracked)
```

## Installation

### Requirements
- Python 3.10 or higher
- pip or uv package manager

### Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd ~/Desktop/Legal
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or using uv:
   ```bash
   uv pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file with necessary API keys (if using external LLM services):
   ```
   OPENAI_API_KEY=your_key_here
   ```

## Usage

### Interactive Mode

Run the assistant in interactive mode to ask multiple questions:

```bash
python main.py
```

This launches an interactive CLI where you can enter questions continuously. Type `quit` or `exit` to exit.

### Single Query Mode

Ask a single question directly from the command line:

```bash
python main.py "What are the fundamental rights under the Indian Constitution?"
```

### Available Commands

- **Interactive**: `python main.py` - Start interactive mode
- **Single Query**: `python main.py "your question"` - Direct query
- **Start Script**: `start` - Uses the entry point defined in pyproject.toml

## How It Works

### Architecture

1. **Query Input**: User submits a legal question
2. **Router Agent**: Classifies the query into appropriate legal domain(s)
3. **Specialist Agents**: Selected agents search their respective legal databases
4. **Search Tools**: Custom tools perform keyword matching against JSON data
5. **Response Generation**: Agents synthesize findings with citations
6. **Output**: Formatted response with article/section references

### Agent Types

- **Router Agent**: Determines which legal domain(s) the query relates to
- **Specialist Agents**: Expert agents for each legal domain (23+ agents)
  - Constitution Expert
  - IPC Expert
  - CPC Expert
  - CRPC Expert
  - Divorce Law Expert
  - And 18+ more domain specialists

### Search Mechanism

Each legal domain has:
- A JSON file with structured legal information
- A custom `SearchTool` class that performs keyword-based search
- Caching mechanism for performance optimization

## Dependencies

### Core
- **crewai** - Multi-agent framework
- **crewai-tools** - Pre-built tools for CrewAI

### Web Server (Optional)
- **flask** >= 3.1.3 - Web framework
- **flask-cors** >= 6.0.2 - Cross-origin resource sharing

### Utilities
- **python-dotenv** - Environment variable management

## Configuration

### Environment Variables
- `CREWAI_INTERACTIVE_MODE` - Set to "false" for non-interactive execution
- `CREWAI_DISABLE_TELEMETRY` - Set to "true" to opt-out of telemetry
- `OPENAI_API_KEY` - API key for LLM services (if applicable)

### CrewAI Settings
Agents are configured with:
- `max_iter=3` - Maximum iterations per agent
- `verbose=False` - Suppress verbose output
- Custom backstories and goals

## Example Queries

```bash
# Constitutional questions
python main.py "What are the Fundamental Rights in India?"
python main.py "Explain Article 14 of the Indian Constitution"

# Criminal law questions
python main.py "What is the punishment for theft under IPC?"
python main.py "What constitutes an offense under Section 420 IPC?"

# Civil matters
python main.py "What is the procedure for filing a divorce?"
python main.py "Explain the grounds for divorce under Indian law"

# IP and commerce
python main.py "How do I register a trademark in India?"
python main.py "What are the copyright protections available?"

# Labor and employment
python main.py "What is the minimum wage in India?"
```

## API Reference

### Main Entry Point
- `main()` - Handles CLI argument parsing and mode selection

### Crew Functions (crew.py)
- `run_query(user_query: str) -> str` - Process a query and return response

### Agent Creation (agents.py)
Each agent follows the pattern: `create_[domain]_agent() -> Agent`

Examples:
- `create_constitution_agent()`
- `create_ipc_agent()`
- `create_router_agent()`

### Task Creation (tasks.py)
Each task follows the pattern: `create_[domain]_query_task(agent, query) -> Task`

### Search Tools (tools.py)
Each domain has a corresponding search tool:
- `ConstitutionSearchTool`
- `IPCSearchTool`
- `CPCSearchTool`
- And 20+ more search tools

## Output Format

Responses include:
- Direct answers to legal questions
- Specific article/section numbers and citations
- Relevant legal context and explanations
- Clear, accessible language

Example:
```
=============================================================
  Question: What does Article 14 of the Constitution say?
=============================================================

  ANSWER
=============================================================
Article 14 establishes the principle of equality before the law...
[Cited Article 14 - Equality before law]
```

## Development

### Adding a New Legal Domain

1. Create a new JSON file with legal data (e.g., `newtopic.json`)
2. Create a search tool in `tools.py` (e.g., `NewTopicSearchTool`)
3. Create an agent in `agents.py` (e.g., `create_new_topic_agent()`)
4. Create a task in `tasks.py` (e.g., `create_new_topic_query_task()`)
5. Add to router logic in `crew.py`

### Testing

Run specific queries to validate functionality:
```bash
python main.py "test query"
```

## Performance Considerations

- **Caching**: Search tools cache JSON data in memory for performance
- **Agent Iterations**: Limited to 3 iterations per agent to control execution time
- **Telemetry**: Disabled by default to reduce overhead

## Troubleshooting

### Common Issues

1. **Module Import Error**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **JSON File Not Found**: Verify JSON files are in the project directory

3. **API Key Issues**: Check `.env` file for proper API key configuration

4. **No Results**: Try rephrasing your query with different keywords

## Contributing

Improvements welcome! Consider:
- Expanding legal domain coverage
- Adding more law resources
- Improving search algorithms
- Enhancing response formatting
- Adding test cases

## License

[Add your license information here]

## Support

For questions or issues about this project, please refer to the inline code documentation or contact the project maintainer.

---

**Last Updated**: March 2026

**Technology Stack**: Python 3.10+, CrewAI, Flask, JSON

**Status**: Active Development
