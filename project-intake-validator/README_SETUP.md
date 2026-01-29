# Project Intake Validator

A comprehensive document validation system that uses Azure OpenAI and LangGraph to automatically extract and validate project intake information from Excel spreadsheets.

## Features

- **Automated Section Extraction**: Uses Azure OpenAI to intelligently extract project information sections
- **Multi-Level Validation**: Validates Header, Business Case, and Project Scope sections
- **Real-time Feedback**: Provides immediate validation results through Streamlit UI
- **Flexible Input**: Accepts Excel files (.xlsx format)
- **LangGraph Integration**: Uses LangGraph for orchestrating validation workflows

## Project Structure

```
project-intake-validator/
├── streamlit_app.py           # Main Streamlit UI application
├── main.py                    # CLI entry point for batch processing
├── check_setup.py             # Pre-flight validation script
├── test_setup.py              # Comprehensive setup tests
├── .env                       # Environment configuration (edit with your credentials)
├── prompts/
│   └── section_extractor.md   # LLM prompt for section extraction
├── src/
│   └── piv/
│       ├── agents/            # Validation agents for each section
│       │   ├── base.py        # Base validation models (ValidationIssue, ValidationResult)
│       │   ├── header_agent.py
│       │   ├── business_case_agent.py
│       │   └── scope_agent.py
│       ├── io/                # Input/Output handlers
│       │   └── excel_reader.py
│       ├── llm/               # LLM integration
│       │   ├── azure_openai_client.py
│       │   └── prompts.py
│       ├── preprocessing/     # Data preprocessing
│       │   └── semantic_extractor.py
│       ├── graph/             # Workflow orchestration
│       │   └── graph.py       # LangGraph workflow definition
│       └── report.py          # Report formatting
└── tests/
    └── test_basic.py
```

## Setup Instructions

### 1. Prerequisites

- Python 3.10 or higher
- Azure OpenAI account with deployed model
- pip or conda package manager

### 2. Installation

```bash
# Navigate to project directory
cd project-intake-validator

# Install dependencies
pip install -r ../requirements.txt
```

### 3. Configuration

Edit the `.env` file with your Azure OpenAI credentials:

```bash
# .env file configuration
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o  # or your deployment name
AZURE_OPENAI_API_VERSION=2025-01-01-preview
```

### 4. Verify Setup

Run the pre-flight check script:

```bash
python check_setup.py
```

This will verify:
- Python environment
- All imports working
- Environment variables configured
- Required files present

## Usage

### Web Interface (Recommended)

```bash
streamlit run streamlit_app.py
```

Then:
1. Open your browser to `http://localhost:8501`
2. Upload an Excel intake file
3. Click "Run Validation 🚀"
4. Review results including:
   - Final Feedback
   - Extracted Sections
   - Validation Details

### Command Line Interface

```bash
python main.py path/to/intake_file.xlsx
```

Optional: Specify custom prompts directory
```bash
python main.py path/to/intake_file.xlsx --prompts_dir ./custom_prompts
```

## Validation Flow

The application follows this workflow:

1. **Read**: Load Excel file and extract text content
2. **Extract**: Use Azure OpenAI to intelligently extract sections:
   - Header information (project name, ID, etc.)
   - Business case details (problem, benefits, metrics)
   - Project scope (in-scope, out-of-scope items)
3. **Validate**: Check each section against requirements:
   - Header: Project Name must be present
   - Business Case: Problem Statement, Expected Benefits, Key Metrics
   - Project Scope: In Scope and Out of Scope sections
4. **Format**: Generate human-readable feedback report

## Validation Rules

### Header Section
- ✓ Project Name is required

### Business Case Section
- ✓ Problem Statement is required
- ✓ Expected Benefits is required
- ✓ Key Metric is required

### Project Scope Section
- ✓ In Scope section is required
- ✓ Out of Scope section is required

## Testing

Run the comprehensive test suite:

```bash
python test_setup.py
```

This validates:
- All imports
- Pydantic models (Validation Issue/Result)
- Prompt file loading
- Agent validation functions
- Report formatting

## Troubleshooting

### Import Errors
- Ensure all `__init__.py` files exist in package directories
- Verify Python path includes project directory
- Run `python test_setup.py` to diagnose

### Azure OpenAI Connection Issues
- Verify `.env` file has correct credentials
- Check Azure Portal for correct endpoint URL
- Ensure deployment name matches your model deployment
- Verify API key has not expired

### Excel File Issues
- Ensure file is in `.xlsx` format
- File should contain extractable text content
- Supported content: merged cells, multiple sheets, text and numbers

### Streamlit Issues
- Clear browser cache if UI not updating
- Check console for detailed error messages
- Verify port 8501 is not in use

## Architecture Notes

### Technologies Used
- **Streamlit**: Web framework for data applications
- **LangGraph**: Orchestration framework for LLM workflows
- **Azure OpenAI**: GPT-4 powered extraction and analysis
- **Pydantic v2**: Data validation and serialization
- **Pandas**: Excel file processing
- **LangChain**: LLM integrations

### Key Components

**Agents**: Modular validation agents for each document section
- Each agent validates specific required fields
- Returns structured ValidationResult with issues list
- Issues include field name, severity, and description

**Graph**: LangGraph-based workflow orchestration
- Multi-node DAG processing pipeline
- Parallel validation of independent sections
- Structured state management

**LLM Integration**: Azure OpenAI client wrapper
- JSON mode output for structured extraction
- Temperature 0 for deterministic results
- Configurable deployment and API version

## Development

### Adding New Validation Rules

Edit agents in `src/piv/agents/`:
```python
def validate_section(section):
    f = section.get("fields", {})
    issues = []
    if not (f.get("FieldName") or "").strip():
        issues.append(ValidationIssue(
            field="FieldName",
            severity="ERROR",
            description="FieldName is required"
        ))
    return ValidationResult(passed=len(issues)==0, issues=issues)
```

### Modifying Extraction Prompts

Edit `prompts/section_extractor.md`:
- Keep `{DOCUMENT_TEXT}` placeholder for document content
- Update extraction instructions as needed
- Test with `python test_setup.py`

## License

Proprietary - All rights reserved

## Support

For issues or questions:
1. Run `python check_setup.py` to validate setup
2. Check troubleshooting section above
3. Review error messages in console output
4. Verify Azure OpenAI credentials and quota limits
