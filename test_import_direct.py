import sys
sys.path.insert(0, '.')

# Try direct file execution
with open('services/nlp_analyzer.py', 'r') as f:
    code = f.read()
    print(f"File has {len(code)} characters")
    print(f"File has {code.count('class NLPAnalyzer')} occurrences of 'class NLPAnalyzer'")
    
# Try importing
try:
    import services.nlp_analyzer as nlp_mod
    print(f"Module attributes: {[x for x in dir(nlp_mod) if not x.startswith('_')]}")
    if hasattr(nlp_mod, 'NLPAnalyzer'):
        print("✓ NLPAnalyzer class found!")
    else:
        print("✗ NLPAnalyzer class NOT found")
        print(f"Available: {dir(nlp_mod)}")
except Exception as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
