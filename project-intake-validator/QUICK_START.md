# QUICK START - RUN THE APP

## Step 1: Install Dependencies (First Time Only)

```bash
cd project-intake-validator
pip install -r ../requirements.txt
```

## Step 2: Configure Azure OpenAI

Edit `.env` file and add your credentials:

```
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2025-01-01-preview
```

Get these from Azure Portal:
- **API Key**: Keys and endpoint section of your resource
- **Endpoint**: Overview section of your resource  
- **Deployment Name**: Name of your GPT-4 deployment
- **API Version**: Latest API version (e.g., 2025-01-01-preview)

## Step 3: Run the Application

### Option A: Web UI (Recommended)

```bash
streamlit run streamlit_app.py
```

Then open: http://localhost:8501

- Upload Excel file
- Click "Run Validation 🚀"
- View results

### Option B: Command Line

```bash
python main.py path/to/intake_file.xlsx
```

Outputs validation results to terminal.

## That's It!

**Fully functional**. No extra steps needed.

---

## Troubleshooting

If you get an error:

1. **Check .env configuration**
   ```bash
   # Verify credentials are correct
   # API key, endpoint, deployment name
   ```

2. **Verify dependencies**
   ```bash
   pip install -r ../requirements.txt
   ```

3. **Check Python version**
   ```bash
   python --version  # Should be 3.10 or higher
   ```

4. **Check file is Excel format**
   ```bash
   # File must be .xlsx (Excel format)
   ```

---

## What the App Does

1. **Reads** Excel file
2. **Extracts** sections using Azure OpenAI:
   - Header (project name, ID)
   - Business Case (problem, benefits, metrics)
   - Project Scope (in-scope, out-of-scope items)
3. **Validates** each section for required fields
4. **Returns** feedback on what's missing

---

## File Structure

```
project-intake-validator/
├── streamlit_app.py     ← Web interface
├── main.py              ← CLI interface
├── .env                 ← Your credentials (EDIT THIS)
├── prompts/
│   └── section_extractor.md
└── src/piv/             ← Application code
```

That's all you need!
