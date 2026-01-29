
# Project Intake Validator

Automated document validation system using Azure OpenAI and LangGraph to extract and validate project intake information from Excel spreadsheets.

## Features

- **Automated Extraction**: Azure OpenAI intelligently extracts project information sections
- **Multi-Level Validation**: Validates Header, Business Case, and Project Scope
- **Real-time Feedback**: Immediate validation results via Streamlit UI
- **Excel Support**: Processes .xlsx files
- **LangGraph Workflow**: Orchestrates validation pipeline

## Quick Start

### Prerequisites
- Python 3.10+
- Azure OpenAI account with GPT-4 deployment
- `.env` file with credentials

### Installation

```bash
cd project-intake-validator
pip install -r ../requirements.txt
```

### Configuration

Edit `.env` with your Azure OpenAI credentials:

```
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2025-01-01-preview
```

### Run the App

**Web UI (Recommended):**
```bash
python -m streamlit run streamlit_app.py
```
Opens at `http://localhost:8501`

**CLI (Batch Processing):**
```bash
python main.py path/to/your_file.xlsx
```

## Project Structure

```
project-intake-validator/
├── streamlit_app.py          # Web UI application
├── main.py                   # CLI batch processing
├── README.md                 # This file
├── .env                      # Configuration (create from .env.example)
├── prompts/
│   └── section_extractor.md  # LLM extraction prompt
├── src/piv/
│   ├── agents/               # Validation agents (header, business_case, scope)
│   ├── io/                   # Excel file reader
│   ├── llm/                  # Azure OpenAI client & prompts
│   ├── preprocessing/        # Semantic extraction
│   ├── graph/                # LangGraph workflow
│   └── report.py             # Feedback formatting
└── tests/                    # Test files
```

## How It Works

1. **Read**: Extracts text from Excel file
2. **Extract**: Uses LLM to structure sections (Header, Business Case, Scope)
3. **Validate**: Three agents validate each section for required fields
4. **Report**: Generates comprehensive feedback with findings

## Required Fields by Section

- **Header**: Project Name, Project ID
- **Business Case**: Problem Statement, Expected Benefits, Key Metric
- **Project Scope**: In Scope, Out of Scope

## Output

Validation feedback listing any missing or invalid fields:
```
- [header] Project Name: Missing
- [business_case] Expected Benefits: Missing
```
