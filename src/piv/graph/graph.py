
from langgraph.graph import StateGraph, END
from typing import Annotated
from langgraph.graph.message import add_messages
from ..io.excel_reader import read_workbook_text
from ..preprocessing.semantic_extractor import extract_sections_via_llm
from ..agents.header_agent import validate_header
from ..agents.business_case_agent import validate_business_case
from ..agents.problem_agent import validate_problem
from ..agents.scope_agent import validate_scope
from ..agents.expected_benefits_agent import validate_expected_benefits
from ..report import format_feedback

def build_graph(context):
    # Define state with proper channel handling for validation results
    def merge_validation(a, b):
        """Merge validation results from different nodes"""
        if a is None:
            return b
        if isinstance(a, dict) and isinstance(b, dict):
            a.update(b)
            return a
        return b

    g = StateGraph(dict)

    def node_read(state):
        txt = read_workbook_text(state["source_path"])
        state["document_text"] = txt
        return state

    def node_extract(state):
        sections = extract_sections_via_llm(state["document_text"], context["prompts_dir"], context["llm"])
        state["sections"] = sections
        return state

    def node_header(state):
        res = validate_header(state["sections"].get("header", {}))
        if "validation" not in state:
            state["validation"] = {}
        state["validation"]["header"] = res
        return state

    def node_business(state):
        res = validate_business_case(state["sections"].get("business_case", {}))
        if "validation" not in state:
            state["validation"] = {}
        state["validation"]["business_case"] = res
        return state

    def node_problem(state):
        res = validate_problem(state["sections"].get("problem_statement", {}))
        if "validation" not in state:
            state["validation"] = {}
        state["validation"]["problem_statement"] = res
        return state

    def node_scope(state):
        res = validate_scope(state["sections"].get("project_scope", {}))
        if "validation" not in state:
            state["validation"] = {}
        state["validation"]["project_scope"] = res
        return state

    def node_benefits(state):
        res = validate_expected_benefits(state["sections"].get("expected_benefits", {}))
        if "validation" not in state:
            state["validation"] = {}
        state["validation"]["expected_benefits"] = res
        return state

    def node_format(state):
        fb = format_feedback(state.get("validation", {}))
        state["final_feedback"] = fb
        return state

    g.add_node("read", node_read)
    g.add_node("extract", node_extract)
    g.add_node("header", node_header)
    g.add_node("business", node_business)
    g.add_node("problem", node_problem)
    g.add_node("scope", node_scope)
    g.add_node("benefits", node_benefits)
    g.add_node("format", node_format)

    g.set_entry_point("read")
    g.add_edge("read", "extract")
    # Make validation nodes sequential instead of parallel
    g.add_edge("extract", "header")
    g.add_edge("header", "business")
    g.add_edge("business", "problem")
    g.add_edge("problem", "scope")
    g.add_edge("scope", "benefits")
    g.add_edge("benefits", "format")
    g.add_edge("format", END)

    return g.compile()
