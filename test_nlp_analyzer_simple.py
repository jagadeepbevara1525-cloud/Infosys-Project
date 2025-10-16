"""
Simple test script for NLP Analyzer orchestrator (without full dependencies).
"""
import sys
from pathlib import Path

# Add App directory to path
sys.path.insert(0, str(Path(__file__).parent))


def test_imports():
    """Test that all necessary imports work."""
    print("\n=== Test: Imports ===")
    
    try:
        from services.nlp_analyzer import NLPAnalyzer
        print("✓ NLPAnalyzer imported successfully")
        
        from models.clause import Clause
        print("✓ Clause model imported successfully")
        
        from models.clause_analysis import ClauseAnalysis
        print("✓ ClauseAnalysis model imported successfully")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_class_structure():
    """Test that NLPAnalyzer has all required methods."""
    print("\n=== Test: Class Structure ===")
    
    try:
        from services.nlp_analyzer import NLPAnalyzer
        
        analyzer = NLPAnalyzer
        
        # Check for required methods
        required_methods = [
            'analyze_clause',
            'analyze_clauses',
            'get_low_confidence_clauses',
            'get_clauses_by_type',
            'set_confidence_threshold',
            'get_analysis_summary',
            '_create_fallback_analysis'
        ]
        
        for method_name in required_methods:
            if hasattr(analyzer, method_name):
                print(f"✓ Method '{method_name}' exists")
            else:
                print(f"✗ Method '{method_name}' missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Class structure test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_initialization():
    """Test NLPAnalyzer initialization."""
    print("\n=== Test: Initialization ===")
    
    try:
        from services.nlp_analyzer import NLPAnalyzer
        
        # Test default initialization
        analyzer = NLPAnalyzer()
        print(f"✓ Default initialization successful")
        print(f"  Confidence threshold: {analyzer.confidence_threshold}")
        
        # Test custom threshold
        analyzer2 = NLPAnalyzer(confidence_threshold=0.8)
        print(f"✓ Custom threshold initialization successful")
        print(f"  Confidence threshold: {analyzer2.confidence_threshold}")
        
        # Verify attributes
        assert hasattr(analyzer, 'classifier'), "Missing classifier attribute"
        assert hasattr(analyzer, 'embedding_generator'), "Missing embedding_generator attribute"
        assert hasattr(analyzer, 'confidence_threshold'), "Missing confidence_threshold attribute"
        print("✓ All required attributes present")
        
        return True
        
    except Exception as e:
        print(f"✗ Initialization test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_method_signatures():
    """Test that methods have correct signatures."""
    print("\n=== Test: Method Signatures ===")
    
    try:
        from services.nlp_analyzer import NLPAnalyzer
        import inspect
        
        analyzer = NLPAnalyzer()
        
        # Check analyze_clause signature
        sig = inspect.signature(analyzer.analyze_clause)
        params = list(sig.parameters.keys())
        assert 'clause' in params, "analyze_clause missing 'clause' parameter"
        print("✓ analyze_clause signature correct")
        
        # Check analyze_clauses signature
        sig = inspect.signature(analyzer.analyze_clauses)
        params = list(sig.parameters.keys())
        assert 'clauses' in params, "analyze_clauses missing 'clauses' parameter"
        assert 'batch_size' in params, "analyze_clauses missing 'batch_size' parameter"
        print("✓ analyze_clauses signature correct")
        
        # Check get_low_confidence_clauses signature
        sig = inspect.signature(analyzer.get_low_confidence_clauses)
        params = list(sig.parameters.keys())
        assert 'analyses' in params, "get_low_confidence_clauses missing 'analyses' parameter"
        print("✓ get_low_confidence_clauses signature correct")
        
        # Check get_clauses_by_type signature
        sig = inspect.signature(analyzer.get_clauses_by_type)
        params = list(sig.parameters.keys())
        assert 'analyses' in params, "get_clauses_by_type missing 'analyses' parameter"
        assert 'clause_type' in params, "get_clauses_by_type missing 'clause_type' parameter"
        print("✓ get_clauses_by_type signature correct")
        
        # Check set_confidence_threshold signature
        sig = inspect.signature(analyzer.set_confidence_threshold)
        params = list(sig.parameters.keys())
        assert 'threshold' in params, "set_confidence_threshold missing 'threshold' parameter"
        print("✓ set_confidence_threshold signature correct")
        
        # Check get_analysis_summary signature
        sig = inspect.signature(analyzer.get_analysis_summary)
        params = list(sig.parameters.keys())
        assert 'analyses' in params, "get_analysis_summary missing 'analyses' parameter"
        print("✓ get_analysis_summary signature correct")
        
        return True
        
    except Exception as e:
        print(f"✗ Method signature test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_docstrings():
    """Test that all methods have docstrings."""
    print("\n=== Test: Docstrings ===")
    
    try:
        from services.nlp_analyzer import NLPAnalyzer
        
        analyzer = NLPAnalyzer
        
        methods = [
            'analyze_clause',
            'analyze_clauses',
            'get_low_confidence_clauses',
            'get_clauses_by_type',
            'set_confidence_threshold',
            'get_analysis_summary'
        ]
        
        for method_name in methods:
            method = getattr(analyzer, method_name)
            if method.__doc__:
                print(f"✓ Method '{method_name}' has docstring")
            else:
                print(f"✗ Method '{method_name}' missing docstring")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Docstring test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing NLP Analyzer Orchestrator (Structure & Interface)")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Class Structure", test_class_structure),
        ("Initialization", test_initialization),
        ("Method Signatures", test_method_signatures),
        ("Docstrings", test_docstrings)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("Test Results Summary:")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("✗ SOME TESTS FAILED")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
