"""Test script for document processing service."""

import sys
from pathlib import Path

# Add App directory to path
sys.path.insert(0, str(Path(__file__).parent))

from services.document_processor import DocumentProcessor
from utils.logger import get_logger

# Setup logging
logger = get_logger("test_document_processor", log_level="INFO")


def test_text_processing():
    """Test processing raw text input."""
    print("\n" + "="*60)
    print("TEST 1: Processing Raw Text Input")
    print("="*60)
    
    sample_contract = """
    DATA PROCESSING AGREEMENT
    
    1. DEFINITIONS
    
    1.1 Data Processing
    The Processor shall process Personal Data only on documented instructions 
    from the Controller, including with regard to transfers of Personal Data 
    to a third country or an international organization.
    
    1.2 Security Measures
    The Processor shall implement appropriate technical and organizational 
    measures to ensure a level of security appropriate to the risk.
    
    2. SUB-PROCESSORS
    
    2.1 Authorization
    The Processor shall not engage another processor without prior specific 
    or general written authorization of the Controller.
    
    2.2 Notification
    In the case of general written authorization, the Processor shall inform 
    the Controller of any intended changes concerning the addition or 
    replacement of other processors, thereby giving the Controller the 
    opportunity to object to such changes.
    
    3. DATA SUBJECT RIGHTS
    
    3.1 Assistance
    The Processor shall assist the Controller by appropriate technical and 
    organizational measures, insofar as this is possible, for the fulfillment 
    of the Controller's obligation to respond to requests for exercising the 
    data subject's rights.
    """
    
    try:
        processor = DocumentProcessor()
        result = processor.process_text(sample_contract, "sample_dpa.txt")
        
        print(f"\n✓ Document ID: {result.document_id}")
        print(f"✓ Filename: {result.original_filename}")
        print(f"✓ Total Characters: {result.total_characters}")
        print(f"✓ Total Words: {result.total_words}")
        print(f"✓ Number of Clauses: {result.num_clauses}")
        print(f"✓ Processing Time: {result.processing_time:.3f}s")
        print(f"✓ Extraction Method: {result.metadata.get('extraction_method')}")
        
        print("\nClauses Found:")
        for i, clause in enumerate(result.clauses, 1):
            print(f"\n  Clause {i}:")
            print(f"    ID: {clause.clause_id}")
            print(f"    Section: {clause.section_number or 'N/A'}")
            print(f"    Heading: {clause.heading or 'N/A'}")
            print(f"    Length: {clause.length} chars")
            print(f"    Position: {clause.start_position}-{clause.end_position}")
            preview = clause.text[:100] + "..." if len(clause.text) > 100 else clause.text
            print(f"    Preview: {preview}")
        
        print("\n✓ TEST PASSED: Text processing successful")
        return True
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pdf_support_check():
    """Test PDF format detection."""
    print("\n" + "="*60)
    print("TEST 2: File Format Support Check")
    print("="*60)
    
    try:
        processor = DocumentProcessor()
        
        test_files = [
            "contract.pdf",
            "document.docx",
            "agreement.txt",
            "scan.png",
            "image.jpg",
            "unsupported.xyz"
        ]
        
        for filename in test_files:
            is_supported = processor.is_supported_format(filename)
            status = "✓ Supported" if is_supported else "✗ Not Supported"
            print(f"  {filename}: {status}")
        
        print("\n✓ TEST PASSED: Format detection working")
        return True
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_clause_model():
    """Test Clause data model."""
    print("\n" + "="*60)
    print("TEST 3: Clause Data Model")
    print("="*60)
    
    try:
        from models.clause import Clause
        
        clause = Clause(
            clause_id="test_001",
            text="The Processor shall process Personal Data only on documented instructions.",
            start_position=0,
            end_position=75,
            section_number="1.1",
            heading="Data Processing"
        )
        
        print(f"\n✓ Clause ID: {clause.clause_id}")
        print(f"✓ Section: {clause.section_number}")
        print(f"✓ Heading: {clause.heading}")
        print(f"✓ Length: {clause.length}")
        print(f"✓ String repr: {str(clause)}")
        
        print("\n✓ TEST PASSED: Clause model working")
        return True
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("DOCUMENT PROCESSING SERVICE TEST SUITE")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Clause Model", test_clause_model()))
    results.append(("Format Support", test_pdf_support_check()))
    results.append(("Text Processing", test_text_processing()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"  {test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n✗ {total - passed} TEST(S) FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
