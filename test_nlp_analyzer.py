"""
Test script for NLP Analyzer orchestrator.
"""
import sys
from pathlib import Path

# Add App directory to path
sys.path.insert(0, str(Path(__file__).parent))

from services.nlp_analyzer import NLPAnalyzer
from models.clause import Clause


def test_single_clause_analysis():
    """Test analyzing a single clause."""
    print("\n=== Test 1: Single Clause Analysis ===")
    
    analyzer = NLPAnalyzer(confidence_threshold=0.75)
    
    clause = Clause(
        clause_id="test_001",
        text="The processor shall process personal data only on documented instructions from the controller, including with regard to transfers of personal data to a third country or an international organisation.",
        start_position=0,
        end_position=200,
        section_number="5.1",
        heading="Data Processing"
    )
    
    analysis = analyzer.analyze_clause(clause)
    
    print(f"Clause ID: {analysis.clause_id}")
    print(f"Clause Type: {analysis.clause_type}")
    print(f"Confidence: {analysis.confidence_score:.2f}")
    print(f"Alternative Types: {analysis.alternative_types[:3]}")
    print(f"Embedding Shape: {analysis.embeddings.shape if analysis.embeddings is not None else 'None'}")
    
    assert analysis.clause_id == "test_001"
    assert analysis.clause_type in ["Data Processing", "Other"]
    assert 0.0 <= analysis.confidence_score <= 1.0
    assert analysis.embeddings is not None
    
    print("✓ Single clause analysis test passed")


def test_batch_clause_analysis():
    """Test analyzing multiple clauses in batch."""
    print("\n=== Test 2: Batch Clause Analysis ===")
    
    analyzer = NLPAnalyzer(confidence_threshold=0.75)
    
    clauses = [
        Clause(
            clause_id="test_001",
            text="The processor shall process personal data only on documented instructions from the controller.",
            start_position=0,
            end_position=100,
            section_number="5.1"
        ),
        Clause(
            clause_id="test_002",
            text="The processor shall not engage another processor without prior specific or general written authorisation of the controller.",
            start_position=100,
            end_position=220,
            section_number="5.2"
        ),
        Clause(
            clause_id="test_003",
            text="The processor shall notify the controller without undue delay after becoming aware of a personal data breach.",
            start_position=220,
            end_position=330,
            section_number="5.3"
        ),
        Clause(
            clause_id="test_004",
            text="The data subject shall have the right to obtain from the controller confirmation as to whether or not personal data concerning him or her are being processed.",
            start_position=330,
            end_position=490,
            section_number="5.4"
        ),
        Clause(
            clause_id="test_005",
            text="The processor shall implement appropriate technical and organizational measures to ensure a level of security appropriate to the risk.",
            start_position=490,
            end_position=620,
            section_number="5.5"
        )
    ]
    
    analyses = analyzer.analyze_clauses(clauses, batch_size=3)
    
    print(f"Total clauses analyzed: {len(analyses)}")
    
    for analysis in analyses:
        print(f"\nClause {analysis.clause_id}:")
        print(f"  Type: {analysis.clause_type}")
        print(f"  Confidence: {analysis.confidence_score:.2f}")
        print(f"  Has Embedding: {analysis.embeddings is not None}")
    
    assert len(analyses) == 5
    assert all(a.clause_id.startswith("test_") for a in analyses)
    assert all(0.0 <= a.confidence_score <= 1.0 for a in analyses)
    
    print("\n✓ Batch clause analysis test passed")


def test_low_confidence_filtering():
    """Test filtering low confidence clauses."""
    print("\n=== Test 3: Low Confidence Filtering ===")
    
    analyzer = NLPAnalyzer(confidence_threshold=0.75)
    
    clauses = [
        Clause(
            clause_id="test_001",
            text="The processor shall process personal data only on documented instructions.",
            start_position=0,
            end_position=100
        ),
        Clause(
            clause_id="test_002",
            text="This is an ambiguous clause with unclear meaning and purpose.",
            start_position=100,
            end_position=200
        ),
        Clause(
            clause_id="test_003",
            text="Random text that doesn't match any specific clause type clearly.",
            start_position=200,
            end_position=300
        )
    ]
    
    analyses = analyzer.analyze_clauses(clauses)
    low_confidence = analyzer.get_low_confidence_clauses(analyses)
    
    print(f"Total clauses: {len(analyses)}")
    print(f"Low confidence clauses: {len(low_confidence)}")
    
    for analysis in low_confidence:
        print(f"  Clause {analysis.clause_id}: confidence={analysis.confidence_score:.2f}")
    
    assert all(a.confidence_score < 0.75 for a in low_confidence)
    
    print("✓ Low confidence filtering test passed")


def test_clause_type_filtering():
    """Test filtering clauses by type."""
    print("\n=== Test 4: Clause Type Filtering ===")
    
    analyzer = NLPAnalyzer()
    
    clauses = [
        Clause(
            clause_id="test_001",
            text="The processor shall process personal data only on documented instructions from the controller.",
            start_position=0,
            end_position=100
        ),
        Clause(
            clause_id="test_002",
            text="The processor shall notify the controller without undue delay after becoming aware of a personal data breach.",
            start_position=100,
            end_position=200
        ),
        Clause(
            clause_id="test_003",
            text="The processor shall implement appropriate technical and organizational security measures.",
            start_position=200,
            end_position=300
        )
    ]
    
    analyses = analyzer.analyze_clauses(clauses)
    
    # Get all unique clause types
    clause_types = set(a.clause_type for a in analyses)
    print(f"Unique clause types found: {clause_types}")
    
    # Filter by each type
    for clause_type in clause_types:
        filtered = analyzer.get_clauses_by_type(analyses, clause_type)
        print(f"  {clause_type}: {len(filtered)} clauses")
        assert all(a.clause_type == clause_type for a in filtered)
    
    print("✓ Clause type filtering test passed")


def test_analysis_summary():
    """Test getting analysis summary statistics."""
    print("\n=== Test 5: Analysis Summary ===")
    
    analyzer = NLPAnalyzer(confidence_threshold=0.75)
    
    clauses = [
        Clause(
            clause_id=f"test_{i:03d}",
            text=f"Sample clause text number {i} for testing purposes.",
            start_position=i * 100,
            end_position=(i + 1) * 100
        )
        for i in range(10)
    ]
    
    analyses = analyzer.analyze_clauses(clauses)
    summary = analyzer.get_analysis_summary(analyses)
    
    print(f"Summary Statistics:")
    print(f"  Total Clauses: {summary['total_clauses']}")
    print(f"  Average Confidence: {summary['avg_confidence']:.3f}")
    print(f"  Low Confidence Count: {summary['low_confidence_count']}")
    print(f"  Clause Type Distribution:")
    for clause_type, count in summary['clause_type_distribution'].items():
        print(f"    {clause_type}: {count}")
    
    assert summary['total_clauses'] == 10
    assert 0.0 <= summary['avg_confidence'] <= 1.0
    assert summary['low_confidence_count'] >= 0
    assert sum(summary['clause_type_distribution'].values()) == 10
    
    print("✓ Analysis summary test passed")


def test_error_handling():
    """Test error handling with invalid input."""
    print("\n=== Test 6: Error Handling ===")
    
    analyzer = NLPAnalyzer()
    
    # Test with empty list
    analyses = analyzer.analyze_clauses([])
    assert len(analyses) == 0
    print("✓ Empty list handled correctly")
    
    # Test summary with empty list
    summary = analyzer.get_analysis_summary([])
    assert summary['total_clauses'] == 0
    print("✓ Empty summary handled correctly")
    
    # Test confidence threshold validation
    try:
        analyzer.set_confidence_threshold(1.5)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Invalid threshold rejected correctly")
    
    print("✓ Error handling test passed")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing NLP Analyzer Orchestrator")
    print("=" * 60)
    
    try:
        test_single_clause_analysis()
        test_batch_clause_analysis()
        test_low_confidence_filtering()
        test_clause_type_filtering()
        test_analysis_summary()
        test_error_handling()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
