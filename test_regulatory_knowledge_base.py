"""
Test script for Regulatory Knowledge Base implementation.
"""
import sys
import numpy as np
from models.regulatory_requirement import (
    RegulatoryRequirement,
    ComplianceStatus,
    RiskLevel,
    ClauseComplianceResult,
    ComplianceSummary,
    ComplianceReport
)
from models.clause_analysis import ClauseAnalysis
from services.regulatory_knowledge_base import RegulatoryKnowledgeBase
from data.gdpr_requirements import get_gdpr_requirements
from data.hipaa_requirements import get_hipaa_requirements
from data.ccpa_requirements import get_ccpa_requirements
from data.sox_requirements import get_sox_requirements


def test_data_models():
    """Test regulatory requirement data models."""
    print("Testing data models...")
    
    # Test RegulatoryRequirement
    req = RegulatoryRequirement(
        requirement_id="TEST_01",
        framework="GDPR",
        article_reference="Test Article",
        clause_type="Data Processing",
        description="Test requirement",
        mandatory=True,
        keywords=["test", "requirement"],
        risk_level=RiskLevel.HIGH
    )
    
    assert req.requirement_id == "TEST_01"
    assert req.framework == "GDPR"
    assert req.risk_level == RiskLevel.HIGH
    print("✓ RegulatoryRequirement model works")
    
    # Test ComplianceStatus enum
    assert ComplianceStatus.COMPLIANT.value == "Compliant"
    assert ComplianceStatus.NON_COMPLIANT.value == "Non-Compliant"
    print("✓ ComplianceStatus enum works")
    
    # Test RiskLevel enum
    assert RiskLevel.HIGH.value == "High"
    assert RiskLevel.MEDIUM.value == "Medium"
    assert RiskLevel.LOW.value == "Low"
    print("✓ RiskLevel enum works")
    
    # Test ClauseComplianceResult
    result = ClauseComplianceResult(
        clause_id="clause_1",
        clause_text="Test clause",
        clause_type="Data Processing",
        framework="GDPR",
        compliance_status=ComplianceStatus.COMPLIANT,
        risk_level=RiskLevel.LOW,
        confidence=0.95
    )
    assert result.clause_id == "clause_1"
    print("✓ ClauseComplianceResult model works")
    
    # Test ComplianceSummary
    summary = ComplianceSummary(
        total_clauses=10,
        compliant_clauses=7,
        non_compliant_clauses=2,
        partial_clauses=1,
        high_risk_count=2,
        medium_risk_count=3,
        low_risk_count=5
    )
    assert summary.total_clauses == 10
    print("✓ ComplianceSummary model works")
    
    # Test ComplianceReport
    report = ComplianceReport(
        document_id="doc_1",
        frameworks_checked=["GDPR", "HIPAA"],
        overall_score=85.5,
        summary=summary
    )
    assert report.document_id == "doc_1"
    assert len(report.frameworks_checked) == 2
    print("✓ ComplianceReport model works")
    
    print("✅ All data models passed!\n")


def test_requirement_databases():
    """Test requirement database functions."""
    print("Testing requirement databases...")
    
    # Test GDPR requirements
    gdpr_reqs = get_gdpr_requirements()
    assert len(gdpr_reqs) > 0
    assert all(req.framework == "GDPR" for req in gdpr_reqs)
    print(f"✓ GDPR: {len(gdpr_reqs)} requirements loaded")
    
    # Test HIPAA requirements
    hipaa_reqs = get_hipaa_requirements()
    assert len(hipaa_reqs) > 0
    assert all(req.framework == "HIPAA" for req in hipaa_reqs)
    print(f"✓ HIPAA: {len(hipaa_reqs)} requirements loaded")
    
    # Test CCPA requirements
    ccpa_reqs = get_ccpa_requirements()
    assert len(ccpa_reqs) > 0
    assert all(req.framework == "CCPA" for req in ccpa_reqs)
    print(f"✓ CCPA: {len(ccpa_reqs)} requirements loaded")
    
    # Test SOX requirements
    sox_reqs = get_sox_requirements()
    assert len(sox_reqs) > 0
    assert all(req.framework == "SOX" for req in sox_reqs)
    print(f"✓ SOX: {len(sox_reqs)} requirements loaded")
    
    # Verify requirement structure
    sample_req = gdpr_reqs[0]
    assert hasattr(sample_req, 'requirement_id')
    assert hasattr(sample_req, 'framework')
    assert hasattr(sample_req, 'article_reference')
    assert hasattr(sample_req, 'clause_type')
    assert hasattr(sample_req, 'description')
    assert hasattr(sample_req, 'mandatory')
    assert hasattr(sample_req, 'keywords')
    assert len(sample_req.keywords) > 0
    print("✓ Requirement structure is valid")
    
    print("✅ All requirement databases passed!\n")


def test_knowledge_base_basic():
    """Test basic knowledge base functionality."""
    print("Testing Regulatory Knowledge Base basic functions...")
    
    # Initialize knowledge base
    kb = RegulatoryKnowledgeBase()
    print("✓ Knowledge base initialized")
    
    # Test get_requirements
    gdpr_reqs = kb.get_requirements("GDPR")
    assert len(gdpr_reqs) > 0
    print(f"✓ Retrieved {len(gdpr_reqs)} GDPR requirements")
    
    hipaa_reqs = kb.get_requirements("HIPAA")
    assert len(hipaa_reqs) > 0
    print(f"✓ Retrieved {len(hipaa_reqs)} HIPAA requirements")
    
    # Test get_all_requirements
    all_reqs = kb.get_all_requirements()
    assert len(all_reqs) == len(gdpr_reqs) + len(hipaa_reqs) + len(kb.get_requirements("CCPA")) + len(kb.get_requirements("SOX"))
    print(f"✓ Retrieved {len(all_reqs)} total requirements")
    
    # Test get_requirements_by_clause_type
    data_processing_reqs = kb.get_requirements_by_clause_type("Data Processing", "GDPR")
    assert len(data_processing_reqs) > 0
    assert all(req.clause_type == "Data Processing" for req in data_processing_reqs)
    print(f"✓ Retrieved {len(data_processing_reqs)} Data Processing requirements for GDPR")
    
    # Test get_requirement_by_id
    req = kb.get_requirement_by_id("GDPR_ART28_01")
    assert req is not None
    assert req.requirement_id == "GDPR_ART28_01"
    print("✓ Retrieved requirement by ID")
    
    # Test search_requirements_by_keyword
    matches = kb.search_requirements_by_keyword("processor", "GDPR")
    assert len(matches) > 0
    print(f"✓ Found {len(matches)} requirements matching 'processor'")
    
    # Test get_statistics
    stats = kb.get_statistics()
    assert 'total_requirements' in stats
    assert 'frameworks' in stats
    assert 'GDPR' in stats['frameworks']
    print(f"✓ Statistics: {stats['total_requirements']} total requirements")
    
    print("✅ All basic knowledge base tests passed!\n")


def test_knowledge_base_advanced():
    """Test advanced knowledge base functionality (without actual embeddings)."""
    print("Testing Regulatory Knowledge Base advanced functions...")
    
    kb = RegulatoryKnowledgeBase()
    
    # Test similarity threshold
    kb.set_similarity_threshold(0.8)
    assert kb.similarity_threshold == 0.8
    print("✓ Similarity threshold updated")
    
    # Test cosine similarity calculation
    vec1 = np.array([1.0, 0.0, 0.0])
    vec2 = np.array([1.0, 0.0, 0.0])
    similarity = kb._cosine_similarity(vec1, vec2)
    assert abs(similarity - 1.0) < 0.01  # Should be 1.0 (identical vectors)
    print("✓ Cosine similarity calculation works")
    
    vec3 = np.array([1.0, 0.0, 0.0])
    vec4 = np.array([0.0, 1.0, 0.0])
    similarity2 = kb._cosine_similarity(vec3, vec4)
    assert abs(similarity2) < 0.01  # Should be 0.0 (orthogonal vectors)
    print("✓ Cosine similarity for orthogonal vectors works")
    
    # Test clear cache
    kb.clear_embedding_cache()
    print("✓ Embedding cache cleared")
    
    print("✅ All advanced knowledge base tests passed!\n")


def main():
    """Run all tests."""
    print("=" * 60)
    print("REGULATORY KNOWLEDGE BASE TEST SUITE")
    print("=" * 60 + "\n")
    
    try:
        test_data_models()
        test_requirement_databases()
        test_knowledge_base_basic()
        test_knowledge_base_advanced()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
