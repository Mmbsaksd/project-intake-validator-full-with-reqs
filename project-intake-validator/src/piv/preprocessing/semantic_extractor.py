
from ..llm.prompts import load_prompt

def extract_sections_via_llm(text, prompts_dir, llm):
    prompt = load_prompt(f"{prompts_dir}/section_extractor.md")
    payload = prompt.replace("{DOCUMENT_TEXT}", text)
    return llm.complete_json("", payload)
