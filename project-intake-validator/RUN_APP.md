# RUN THE APP - 3 SIMPLE STEPS

## Step 1: Install Dependencies (First Time Only)

```
pip install -r ../requirements.txt
```

✅ Already done! (as shown in terminal output)

---

## Step 2: Configure Your Azure Credentials

Edit the `.env` file and replace with your actual values:

```
AZURE_OPENAI_API_KEY=your_api_key_from_azure
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2025-01-01-preview
```

**Where to get these:**
- Go to Azure Portal → Your OpenAI Resource
- Click "Keys and endpoint"
- Copy your API Key (Key 1 or Key 2)
- Copy your Endpoint URL
- Use your model deployment name

---

## Step 3: Run the App

### Web Interface (Recommended)
```
streamlit run streamlit_app.py
```

Then:
1. Browser opens to `http://localhost:8501`
2. Upload your Excel file (.xlsx)
3. Click "Run Validation 🚀"
4. View results

### Command Line
```
python main.py path/to/your_file.xlsx
```

Outputs results to console.

---

## That's It!

The app is ready. Just configure .env and run one command.

**Files you'll need:**
- streamlit_app.py (web app)
- main.py (CLI app)
- .env (your credentials)
- src/piv/ (application code)
- prompts/ (extraction templates)

**You can delete everything else if you want minimal:**
- check_setup.py
- test_setup.py
- run_app.py
- All the .md/.txt documentation files (except this guide)

---

## Troubleshooting

**Error: "API key not set"**
→ Check .env file has real credentials (not placeholder text)

**Error: "Module not found"**
→ Run: `pip install -r ../requirements.txt`

**Error: "Connection failed"**
→ Verify API key is correct, endpoint URL is correct

**Error: "File not found"**
→ Use full path to Excel file, check file format is .xlsx

---

Done! ✅
