#!/usr/bin/env python3
"""
Setup validation script to test all imports and basic functionality
"""
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test all critical imports"""
    print("Testing imports...")
    try:
        from src.piv.agents.base import ValidationResult, ValidationIssue
        print("✓ Agents (base)")
        
        from src.piv.agents.header_agent import validate_header
        print("✓ Header agent")
        
        from src.piv.agents.business_case_agent import validate_business_case
        print("✓ Business case agent")
        
        from src.piv.agents.scope_agent import validate_scope
        print("✓ Scope agent")
        
        from src.piv.report import format_feedback
        print("✓ Report formatter")
        
        from src.piv.io.excel_reader import read_workbook_text
        print("✓ Excel reader")
        
        from src.piv.preprocessing.semantic_extractor import extract_sections_via_llm
        print("✓ Semantic extractor")
        
        from src.piv.llm.azure_openai_client import AzureOpenAILLM
        print("✓ Azure OpenAI client")
        
        from src.piv.llm.prompts import load_prompt
        print("✓ Prompts loader")
        
        from src.piv.graph.graph import build_graph
        print("✓ Graph builder")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_validation_models():
    """Test Pydantic models"""
    print("\nTesting validation models...")
    try:
        from src.piv.agents.base import ValidationResult, ValidationIssue
        
        # Test creating an issue
        issue = ValidationIssue(field="test", severity="ERROR", description="Test issue")
        print(f"✓ Created ValidationIssue: {issue}")
        
        # Test creating a result
        result = ValidationResult(passed=False, issues=[issue])
        print(f"✓ Created ValidationResult: passed={result.passed}")
        
        # Test model_dump (Pydantic v2)
        dumped = result.model_dump()
        print(f"✓ model_dump() works: {type(dumped)}")
        
        return True
    except Exception as e:
        print(f"✗ Model test failed: {e}")
        return False

def test_prompts():
    """Test prompt file loading"""
    print("\nTesting prompt loading...")
    try:
        from src.piv.llm.prompts import load_prompt
        prompt_path = Path(__file__).parent / "prompts" / "section_extractor.md"
        
        if not prompt_path.exists():
            print(f"✗ Prompt file not found: {prompt_path}")
            return False
        
        prompt = load_prompt(str(prompt_path))
        if prompt and len(prompt) > 0:
            print(f"✓ Loaded prompt ({len(prompt)} chars)")
            return True
        else:
            print("✗ Prompt is empty")
            return False
    except Exception as e:
        print(f"✗ Prompt loading failed: {e}")
        return False

def test_agents():
    """Test agent validation functions"""
    print("\nTesting agents...")
    try:
        from src.piv.agents.header_agent import validate_header
        from src.piv.agents.business_case_agent import validate_business_case
        from src.piv.agents.scope_agent import validate_scope
        
        # Test with empty sections
        empty_section = {"fields": {}}
        
        header_result = validate_header(empty_section)
        print(f"✓ Header validation: passed={header_result.passed}, issues={len(header_result.issues)}")
        
        business_result = validate_business_case(empty_section)
        print(f"✓ Business case validation: passed={business_result.passed}, issues={len(business_result.issues)}")
        
        scope_result = validate_scope(empty_section)
        print(f"✓ Scope validation: passed={scope_result.passed}, issues={len(scope_result.issues)}")
        
        return True
    except Exception as e:
        print(f"✗ Agent test failed: {e}")
        return False

def test_formatting():
    """Test report formatting"""
    print("\nTesting report formatting...")
    try:
        from src.piv.agents.base import ValidationResult, ValidationIssue
        from src.piv.report import format_feedback
        
        validation = {
            "header": ValidationResult(passed=True, issues=[]),
            "business_case": ValidationResult(
                passed=False, 
                issues=[ValidationIssue(field="Problem", severity="ERROR", description="Missing")]
            )
        }
        
        feedback = format_feedback(validation)
        print(f"✓ Formatted feedback ({len(feedback)} chars)")
        if "Feedback" in feedback:
            print("✓ Feedback contains expected content")
            return True
        else:
            print("✗ Feedback missing expected content")
            return False
    except Exception as e:
        print(f"✗ Formatting test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Project Intake Validator - Setup Test")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_validation_models,
        test_prompts,
        test_agents,
        test_formatting,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"\n✗ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if all(results):
        print("✓ All tests passed! App should run correctly.")
        return 0
    else:
        print("✗ Some tests failed. Check output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
