#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from dotenv import load_dotenv
load_dotenv()
from src.piv.llm.azure_openai_client import AzureOpenAILLM
from src.piv.graph.graph import build_graph

print('Initializing LLM...')
llm = AzureOpenAILLM()
print('Building graph...')
context = {'llm': llm, 'prompts_dir': 'prompts'}
graph = build_graph(context)
print('Graph built')

excel_path = Path(r'C:\Users\mohammed.a\Desktop\sample_test.xlsx')
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
