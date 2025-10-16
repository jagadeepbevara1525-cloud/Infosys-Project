"""
Test script to verify Streamlit integration components.
This tests the service initialization and basic functionality.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_service_imports():
    """Test that all services can be imported."""
    print("Testing service imports...")
    
    try:
        from services.document_processor import DocumentProcessor
        from services.nlp_analyzer import NLPAnalyzer
        from services.compliance_checker import ComplianceChecker
        from services.recommendation_engine import RecommendationEngine
        print("✅ All services imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_service_initialization():
    """Test that all services can be initialized."""
    print("\nTesting service initialization...")
    
    try:
        from services.document_processor import DocumentProcessor
        from services.nlp_analyzer import NLPAnalyzer
        from services.compliance_checker import ComplianceChecker
        from services.recommendation_engine import RecommendationEngine
        
        # Initialize services
        doc_processor = DocumentProcessor()
        print("✅ DocumentProcessor initialized")
        
        nlp_analyzer = NLPAnalyzer()
        print("✅ NLPAnalyzer initialized")
        
        compliance_checker = ComplianceChecker()
        print("✅ ComplianceChecker initialized")
        
        rec_engine = RecommendationEngine(use_llama=False)
        print("✅ RecommendationEngine initialized")
        
        return True
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_document_processing():
    """Test document processing with sample text."""
    print("\nTesting document processing...")
    
    try:
        from services.document_processor import DocumentProcessor
        
        doc_processor = DocumentProcessor()
        
        # Sample contract text
        sample_text = """
        DATA PROCESSING AGREEMENT
        
        1. Data Processing Terms
        The Processor shall process Personal Data only on documented instructions from the Controller.
        
        2. Security Measures
        The Processor shall implement appropriate technical and organizational measures to ensure
        a level of security appropriate to the risk.
        
        3. Sub-processor Authorization
        The Processor shall not engage another processor without prior written authorization from
        the Controller.
        
        4. Data Subject Rights
        The Processor shall assist the Controller in responding to requests for exercising the
        data subject's rights.
        
        5. Breach Notification
        The Processor shall notify the Controller without undue delay after becoming aware of a
        personal data breach.
        """
        
        processed_doc = doc_processor.process_text(sample_text, "test_contract.txt")
        
        print(f"✅ Document processed successfully")
        print(f"   - Document ID: {processed_doc.document_id}")
        print(f"   - Clauses: {processed_doc.num_clauses}")
        print(f"   - Words: {processed_doc.total_words}")
        print(f"   - Processing time: {processed_doc.processing_time:.2f}s")
        
        return True, processed_doc
    except Exception as e:
        print(f"❌ Document processing failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_nlp_analysis(processed_doc):
    """Test NLP analysis on processed document."""
    print("\nTesting NLP analysis...")
    
    try:
        from services.nlp_analyzer import NLPAnalyzer
        
        nlp_analyzer = NLPAnalyzer()
        
        # Analyze clauses
        clause_analyses = nlp_analyzer.analyze_clauses(processed_doc.clauses)
        
        print(f"✅ NLP analysis completed")
        print(f"   - Clauses analyzed: {len(clause_analyses)}")
        
        # Show sample results
        if clause_analyses:
            sample = clause_analyses[0]
            print(f"   - Sample clause type: {sample.clause_type}")
            print(f"   - Sample confidence: {sample.confidence_score:.2f}")
        
        return True, clause_analyses
    except Exception as e:
        print(f"❌ NLP analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_compliance_checking(clause_analyses):
    """Test compliance checking."""
    print("\nTesting compliance checking...")
    
    try:
        from services.compliance_checker import ComplianceChecker
        
        compliance_checker = ComplianceChecker()
        
        # Check compliance
        frameworks = ['GDPR', 'HIPAA']
        compliance_report = compliance_checker.check_compliance(
            clause_analyses,
            frameworks,
            "test_document"
        )
        
        print(f"✅ Compliance checking completed")
        print(f"   - Overall score: {compliance_report.overall_score:.2f}")
        print(f"   - High risk items: {compliance_report.summary.high_risk_count}")
        print(f"   - Missing requirements: {len(compliance_report.missing_requirements)}")
        
        return True, compliance_report
    except Exception as e:
        print(f"❌ Compliance checking failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_recommendation_generation(compliance_report):
    """Test recommendation generation."""
    print("\nTesting recommendation generation...")
    
    try:
        from services.recommendation_engine import RecommendationEngine
        
        rec_engine = RecommendationEngine(use_llama=False)
        
        # Generate recommendations
        recommendations = rec_engine.generate_recommendations(compliance_report)
        
        print(f"✅ Recommendation generation completed")
        print(f"   - Recommendations generated: {len(recommendations)}")
        
        # Show sample recommendation
        if recommendations:
            sample = recommendations[0]
            print(f"   - Sample action: {sample.action_type.value}")
            print(f"   - Sample priority: {sample.priority}")
        
        return True
    except Exception as e:
        print(f"❌ Recommendation generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("STREAMLIT INTEGRATION TEST SUITE")
    print("=" * 60)
    
    results = []
    
    # Test 1: Imports
    results.append(("Service Imports", test_service_imports()))
    
    # Test 2: Initialization
    results.append(("Service Initialization", test_service_initialization()))
    
    # Test 3: Document Processing
    success, processed_doc = test_document_processing()
    results.append(("Document Processing", success))
    
    if success and processed_doc:
        # Test 4: NLP Analysis
        success, clause_analyses = test_nlp_analysis(processed_doc)
        results.append(("NLP Analysis", success))
        
        if success and clause_analyses:
            # Test 5: Compliance Checking
            success, compliance_report = test_compliance_checking(clause_analyses)
            results.append(("Compliance Checking", success))
            
            if success and compliance_report:
                # Test 6: Recommendation Generation
                success = test_recommendation_generation(compliance_report)
                results.append(("Recommendation Generation", success))
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Integration is working correctly.")
        return 0
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
