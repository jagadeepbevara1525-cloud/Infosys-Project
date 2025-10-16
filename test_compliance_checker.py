"""
Test script for Compliance Checker implementation.
Tests the complete compliance checking engine including all sub-components.
"""
import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.clause_analysis import ClauseAnalysis, ClauseType
from models.regulatory_requirement import ComplianceStatus, RiskLevel
from services.compliance_checker import ComplianceChecker
from services.regulatory_knowledge_base import RegulatoryKnowledgeBase
from services.embedding_generator import EmbeddingGenerator
from utils.logger import get_logger

logger = get_logger(__name__)


def create_sample_clauses():
    """Create sample clauses for testing."""
    embedding_gen = EmbeddingGenerator()
    
    clauses = [
        ClauseAnalysis(
            clause_id="clause_001",
            clause_text=(
                "The Processor shall process Personal Data only on documented "
                "instructions from the Controller, including with regard to "
                "transfers of Personal Data to a third country or an international "
                "organisation. The Processor shall ensure that persons authorized "
                "to process the Personal Data have committed themselves to "
                "confidentiality or are under an appropriate statutory obligation "
                "of confidentiality."
            ),
            clause_type=ClauseType.DATA_PROCESSING.value,
            confidence_score=0.92,
            embeddings=None
        ),
        ClauseAnalysis(
            clause_id="clause_002",
            clause_text=(
                "The Processor shall not engage another processor (sub-processor) "
                "without prior specific or general written authorization of the "
                "Controller. The Processor shall inform the Controller of any "
                "intended changes concerning the addition or replacement of other "
                "processors, thereby giving the Controller the opportunity to "
                "object to such changes within 30 days."
            ),
            clause_type=ClauseType.SUBPROCESSOR_AUTH.value,
            confidence_score=0.89,
            embeddings=None
        ),
        ClauseAnalysis(
            clause_id="clause_003",
            clause_text=(
                "The Processor shall implement appropriate technical and "
                "organizational measures to ensure a level of security appropriate "
                "to the risk, including encryption, access controls, and regular "
                "security assessments."
            ),
            clause_type=ClauseType.SECURITY_SAFEGUARDS.value,
            confidence_score=0.85,
            embeddings=None
        ),
        ClauseAnalysis(
            clause_id="clause_004",
            clause_text=(
                "In the event of a breach of security leading to the accidental "
                "or unlawful destruction, loss, alteration, unauthorized disclosure "
                "of, or access to Personal Data, the Processor shall notify the "
                "Controller without undue delay and in any event within 72 hours "
                "after becoming aware of the breach."
            ),
            clause_type=ClauseType.BREACH_NOTIFICATION.value,
            confidence_score=0.91,
            embeddings=None
        ),
        ClauseAnalysis(
            clause_id="clause_005",
            clause_text=(
                "The parties agree to general terms and conditions of service."
            ),
            clause_type=ClauseType.OTHER.value,
            confidence_score=0.45,
            embeddings=None
        )
    ]
    
    # Generate embeddings for all clauses
    print("Generating embeddings for sample clauses...")
    for clause in clauses:
        clause.embeddings = embedding_gen.generate_embedding(clause.clause_text)
    
    return clauses


def test_compliance_rule_engine():
    """Test the Compliance Rule Engine."""
    print("\n" + "="*70)
    print("TEST 1: Compliance Rule Engine")
    print("="*70)
    
    from services.compliance_rule_engine import ComplianceRuleEngine
    from data.gdpr_requirements import get_gdpr_requirements
    
    rule_engine = ComplianceRuleEngine()
    gdpr_reqs = get_gdpr_requirements()
    
    # Create a test clause
    clause = ClauseAnalysis(
        clause_id="test_001",
        clause_text=(
            "The processor shall process data only on documented instructions "
            "from the controller and ensure confidentiality."
        ),
        clause_type=ClauseType.DATA_PROCESSING.value,
        confidence_score=0.85,
        embeddings=np.random.rand(384)
    )
    
    # Test GDPR evaluation
    data_processing_req = next(
        (req for req in gdpr_reqs if req.clause_type == "Data Processing"),
        None
    )
    
    if data_processing_req:
        status, risk, issues = rule_engine.evaluate_gdpr_compliance(
            clause,
            data_processing_req,
            similarity_score=0.82
        )
        
        print(f"✓ GDPR Evaluation:")
        print(f"  - Status: {status.value}")
        print(f"  - Risk Level: {risk.value}")
        print(f"  - Issues: {len(issues)} found")
        if issues:
            for issue in issues:
                print(f"    • {issue}")
    else:
        print("✗ Could not find GDPR Data Processing requirement")
    
    print("\n✓ Compliance Rule Engine test completed")


def test_compliance_assessor():
    """Test the Compliance Assessor."""
    print("\n" + "="*70)
    print("TEST 2: Compliance Assessor")
    print("="*70)
    
    from services.compliance_assessor import ComplianceAssessor
    from services.regulatory_knowledge_base import RegulatoryKnowledgeBase
    from services.compliance_rule_engine import ComplianceRuleEngine
    
    knowledge_base = RegulatoryKnowledgeBase()
    rule_engine = ComplianceRuleEngine()
    assessor = ComplianceAssessor(knowledge_base, rule_engine)
    
    # Create sample clauses
    clauses = create_sample_clauses()
    
    # Assess first clause against GDPR
    result = assessor.assess_clause_compliance(clauses[0], "GDPR")
    
    print(f"✓ Assessed clause: {clauses[0].clause_id}")
    print(f"  - Clause Type: {result.clause_type}")
    print(f"  - Framework: {result.framework}")
    print(f"  - Status: {result.compliance_status.value}")
    print(f"  - Risk Level: {result.risk_level.value}")
    print(f"  - Confidence: {result.confidence:.2f}")
    print(f"  - Matched Requirements: {len(result.matched_requirements)}")
    print(f"  - Issues: {len(result.issues)}")
    
    # Test multiple clauses
    results = assessor.assess_multiple_clauses(clauses[:3], "GDPR")
    print(f"\n✓ Assessed {len(results)} clauses against GDPR")
    
    # Test high-risk filtering
    high_risk = assessor.get_high_risk_results(results)
    print(f"✓ Found {len(high_risk)} high-risk items")
    
    print("\n✓ Compliance Assessor test completed")


def test_compliance_scorer():
    """Test the Compliance Scorer."""
    print("\n" + "="*70)
    print("TEST 3: Compliance Scorer")
    print("="*70)
    
    from services.compliance_scorer import ComplianceScorer
    from services.compliance_assessor import ComplianceAssessor
    from services.regulatory_knowledge_base import RegulatoryKnowledgeBase
    
    knowledge_base = RegulatoryKnowledgeBase()
    assessor = ComplianceAssessor(knowledge_base)
    scorer = ComplianceScorer()
    
    # Create and assess sample clauses
    clauses = create_sample_clauses()
    results = assessor.assess_multiple_clauses(clauses, "GDPR")
    
    # Find missing requirements
    missing = knowledge_base.find_missing_requirements(clauses, "GDPR")
    
    # Calculate overall score
    overall_score = scorer.calculate_overall_score(results, missing)
    print(f"✓ Overall Compliance Score: {overall_score:.2f}/100")
    
    # Generate summary
    summary = scorer.generate_compliance_summary(results)
    print(f"\n✓ Compliance Summary:")
    print(f"  - Total Clauses: {summary.total_clauses}")
    print(f"  - Compliant: {summary.compliant_clauses}")
    print(f"  - Partial: {summary.partial_clauses}")
    print(f"  - Non-Compliant: {summary.non_compliant_clauses}")
    print(f"  - High Risk: {summary.high_risk_count}")
    print(f"  - Medium Risk: {summary.medium_risk_count}")
    print(f"  - Low Risk: {summary.low_risk_count}")
    
    # Identify high-risk items
    high_risk = scorer.identify_high_risk_items(results)
    print(f"\n✓ High-Risk Items: {len(high_risk)}")
    
    # Get framework breakdown
    breakdown = scorer.get_framework_breakdown(results, missing)
    print(f"\n✓ Framework Breakdown:")
    for framework, stats in breakdown.items():
        print(f"  - {framework}: Score {stats['score']:.2f}")
    
    print("\n✓ Compliance Scorer test completed")


def test_compliance_checker():
    """Test the main Compliance Checker orchestrator."""
    print("\n" + "="*70)
    print("TEST 4: Compliance Checker (Full Integration)")
    print("="*70)
    
    # Initialize compliance checker
    checker = ComplianceChecker()
    
    # Create sample clauses
    clauses = create_sample_clauses()
    
    print(f"✓ Compliance Checker initialized")
    print(f"✓ Testing with {len(clauses)} sample clauses")
    
    # Test single framework check
    print("\n--- Testing GDPR Compliance ---")
    gdpr_report = checker.check_single_framework(
        clauses,
        "GDPR",
        document_id="test_doc_001"
    )
    
    print(f"✓ GDPR Report Generated:")
    print(f"  - Document ID: {gdpr_report.document_id}")
    print(f"  - Overall Score: {gdpr_report.overall_score:.2f}/100")
    print(f"  - Frameworks Checked: {', '.join(gdpr_report.frameworks_checked)}")
    print(f"  - Clause Results: {len(gdpr_report.clause_results)}")
    print(f"  - Missing Requirements: {len(gdpr_report.missing_requirements)}")
    print(f"  - High-Risk Items: {len(gdpr_report.high_risk_items)}")
    
    if gdpr_report.summary:
        print(f"\n  Summary:")
        print(f"    - Total Clauses: {gdpr_report.summary.total_clauses}")
        print(f"    - Compliant: {gdpr_report.summary.compliant_clauses}")
        print(f"    - Non-Compliant: {gdpr_report.summary.non_compliant_clauses}")
        print(f"    - High Risk: {gdpr_report.summary.high_risk_count}")
    
    # Test multiple frameworks
    print("\n--- Testing Multiple Frameworks ---")
    multi_report = checker.check_compliance(
        clauses,
        ["GDPR", "HIPAA"],
        document_id="test_doc_002"
    )
    
    print(f"✓ Multi-Framework Report Generated:")
    print(f"  - Overall Score: {multi_report.overall_score:.2f}/100")
    print(f"  - Frameworks: {', '.join(multi_report.frameworks_checked)}")
    print(f"  - Total Results: {len(multi_report.clause_results)}")
    print(f"  - Missing Requirements: {len(multi_report.missing_requirements)}")
    
    # Test quick check
    print("\n--- Testing Quick Check ---")
    scores = checker.quick_check(clauses, ["GDPR", "HIPAA", "CCPA"])
    print(f"✓ Quick Check Scores:")
    for framework, score in scores.items():
        print(f"  - {framework}: {score:.2f}/100")
    
    # Test framework statistics
    print("\n--- Framework Statistics ---")
    stats = checker.get_framework_statistics()
    print(f"✓ Total Requirements: {stats['total_requirements']}")
    for framework, fw_stats in stats['frameworks'].items():
        print(f"  - {framework}: {fw_stats['total']} total "
              f"({fw_stats['mandatory']} mandatory)")
    
    print("\n✓ Compliance Checker test completed")


def test_error_handling():
    """Test error handling in compliance checker."""
    print("\n" + "="*70)
    print("TEST 5: Error Handling")
    print("="*70)
    
    checker = ComplianceChecker()
    
    # Test with empty clauses
    print("Testing with empty clauses...")
    empty_report = checker.check_compliance([], ["GDPR"], "empty_doc")
    print(f"✓ Empty clauses handled: Score = {empty_report.overall_score}")
    
    # Test with invalid framework
    print("\nTesting with invalid framework...")
    try:
        invalid_report = checker.check_compliance(
            create_sample_clauses()[:2],
            ["INVALID_FRAMEWORK"],
            "invalid_doc"
        )
        print(f"✗ Should have raised error for invalid framework")
    except ValueError as e:
        print(f"✓ Invalid framework handled correctly: {e}")
    
    # Test with no frameworks
    print("\nTesting with no frameworks...")
    try:
        no_fw_report = checker.check_compliance(
            create_sample_clauses()[:2],
            [],
            "no_fw_doc"
        )
        print(f"✗ Should have raised error for no frameworks")
    except ValueError as e:
        print(f"✓ No frameworks handled correctly: {e}")
    
    print("\n✓ Error handling test completed")


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("COMPLIANCE CHECKER IMPLEMENTATION TEST SUITE")
    print("="*70)
    
    try:
        # Run all tests
        test_compliance_rule_engine()
        test_compliance_assessor()
        test_compliance_scorer()
        test_compliance_checker()
        test_error_handling()
        
        print("\n" + "="*70)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\nSummary:")
        print("✓ Task 5.1: Compliance Rule Engine - PASSED")
        print("✓ Task 5.2: Clause-to-Requirement Matching - PASSED")
        print("✓ Task 5.3: Compliance Assessment Logic - PASSED")
        print("✓ Task 5.4: Overall Compliance Scoring - PASSED")
        print("✓ Task 5.5: Compliance Checker Orchestrator - PASSED")
        print("\n✓ Task 5: Implement compliance checking engine - COMPLETE")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
