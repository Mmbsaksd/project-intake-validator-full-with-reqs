
import sys
from pathlib import Path

# Add current directory to path to allow relative imports
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from src.piv.graph.graph import build_graph
from src.piv.llm.azure_openai_client import AzureOpenAILLM

def run_pipeline(xlsx_path: str, prompts_dir: str = None):
    if prompts_dir is None:
        prompts_dir = Path(__file__).parent / "prompts"
    else:
        prompts_dir = Path(prompts_dir).resolve()
    
    load_dotenv()
    llm = AzureOpenAILLM()
    context = {"llm": llm, "prompts_dir": str(prompts_dir)}
    graph = build_graph(context)
    initial = {
        "source_path": str(Path(xlsx_path).resolve()),
        "document_text": "",
        "sections": {},
        "validation": {},
        "final_feedback": None,
    }
    out = graph.invoke(initial)
    print(out["final_feedback"])
    return out

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Project Intake Validator (Azure OpenAI)")
    parser.add_argument("xlsx_path")
    parser.add_argument("--prompts_dir", default=None)
    args = parser.parse_args()
    run_pipeline(args.xlsx_path, args.prompts_dir)
