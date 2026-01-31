#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from dotenv import load_dotenv
load_dotenv()
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
from src.piv.llm.azure_openai_client import AzureOpenAILLM
from src.piv.graph.graph import build_graph

print('Initializing LLM...')
llm = AzureOpenAILLM()
print('Building graph...')
PROMPTS_DIR = Path(__file__).parent / 'prompts'
context = {'llm': llm, 'prompts_dir': str(PROMPTS_DIR)}
graph = build_graph(context)
print('Graph built')

excel_path = Path(__file__).parent / 'tests' / 'sample_intake.xlsx'
if not excel_path.exists():
    print('Sample file missing:', excel_path)
    sys.exit(1)

initial = {
    'source_path': str(excel_path.resolve()),
    'document_text': '',
    'sections': {},
    'validation': {},
    'final_feedback': None,
}
print('Invoking graph...')
res = graph.invoke(initial)
print('\n--- FINAL FEEDBACK ---')
print(res.get('final_feedback'))
print('\n--- SECTIONS ---')
import json
print(json.dumps(res.get('sections', {}), indent=2))
