"""
Test script for Recommendation Engine implementation.
Tests the LLaMA-based recommendation engine without requiring actual model loading.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from models.recommendation import Recommendation, ActionType
from models.regulatory_requirement import (
    RegulatoryRequirement,
    ComplianceReport,
    ClauseComplianceResult,
    ComplianceSummary,
    ComplianceStatus,
    RiskLevel
)
from models.clause_analysis import ClauseAnalysis
from services.prompt_builder import PromptBuilder
from services.recommendation_generator import RecommendationGenerator
from services.clause_generator import ClauseGenerator
from services.recommendation_engine import RecommendationEngine
import numpy as np


def test_prompt_builder():
    """Test PromptBuilder functionality."""
    print("\n=== Testing PromptBuilder ===")
    
    builder = PromptBuilder()
    
    # Create test data
    requirement = RegulatoryRequirement(
        requirement_id="GDPR_ART28_01",
        framework="GDPR",
        article_reference="GDPR Article 28",
        clause_type="Data Processing",
        description="Processor obligations and data processing terms",
        mandatory=True,
        keywords=["processor", "processing", "instructions"],
        mandatory_elements=[
            "Processing only on documented instructions",
            "Confidentiality obligations",
            "Security measures"
        ]
    )
    
    clause = ClauseAnalysis(
        clause_id="clause_001",
        clause_text="The processor shall process data as instructed.",
        clause_type="Data Processing",
        confidence_score=0.85,
        embeddings=np.random.rand(384),
        alternative_types=[]
    )
    
    issues = ["Missing confidentiality obligations", "No security measures specified"]
    
    # Test recommendation prompt
    print("\n1. Testing recommendation prompt generation...")
    rec_prompt = builder.build_recommendation_prompt(clause, requirement, issues)
    assert len(rec_prompt) > 0
    assert "GDPR Article 28" in rec_prompt
    assert "Missing confidentiality obligations" in rec_prompt
    print("✓ Recommendation prompt generated successfully")
    print(f"  Prompt length: {len(rec_prompt)} characters")
    
    # Test generation prompt
    print("\n2. Testing clause generation prompt...")
    gen_prompt = builder.build_generation_prompt(
        requirement,
        "Data Processing Agreement between Company A and Company B",
        ["Sample existing clause text"]
    )
    assert len(gen_prompt) > 0
    assert "GDPR Article 28" in gen_prompt
    print("✓ Generation prompt created successfully")
    
    # Test modification prompt
    print("\n3. Testing modification prompt...")
    mod_prompt = builder.build_modification_prompt(clause, requirement, issues)
    assert len(mod_prompt) > 0
    assert "MODIFIED CLAUSE" in mod_prompt
    print("✓ Modification prompt created successfully")
    
    # Test regulatory context injection
    print("\n4. Testing regulatory context injection...")
    context = builder.build_regulatory_context_injection(requirement)
    assert "GDPR" in context
    assert "Article 28" in context
    print("✓ Regulatory context generated successfully")
    
    print("\n✓ All PromptBuilder tests passed!")


def test_recommendation_generator():
    """Test RecommendationGenerator functionality (without LLaMA)."""
    print("\n=== Testing RecommendationGenerator ===")
    
    # Initialize without LLaMA model
    generator = RecommendationGenerator(llama_model=None)
    
    # Create test data
    requirement = RegulatoryRequirement(
        requirement_id="GDPR_ART28_02",
        framework="GDPR",
        article_reference="GDPR Article 28(2)",
        clause_type="Sub-processor Authorization",
        description="Sub-processor authorization and notification",
        mandatory=True,
        risk_level=RiskLevel.HIGH
    )
    
    # Test missing requirement recommendation
    print("\n1. Testing missing requirement recommendation generation...")
    rec = generator._generate_missing_requirement_recommendation(requirement)
    assert rec is not None
    assert rec.action_type == ActionType.ADD_CLAUSE
    assert rec.priority == 1  # HIGH risk = priority 1
    assert "GDPR Article 28(2)" in rec.regulatory_reference
    print("✓ Missing requirement recommendation generated")
    print(f"  Priority: {rec.get_priority_label()}")
    print(f"  Action: {rec.action_type.value}")
    
    # Test action type determination
    print("\n2. Testing action type determination...")
    issues_missing = ["Missing required element"]
    action = generator._determine_action_type(issues_missing)
    assert action == ActionType.ADD_CLAUSE
    print("✓ Action type correctly determined as ADD_CLAUSE")
    
    issues_unclear = ["Unclear language", "Ambiguous terms"]
    action = generator._determine_action_type(issues_unclear)
    assert action == ActionType.CLARIFY_CLAUSE
    print("✓ Action type correctly determined as CLARIFY_CLAUSE")
    
    # Test risk to priority conversion
    print("\n3. Testing risk to priority conversion...")
    priority_high = generator._risk_to_priority(RiskLevel.HIGH)
    assert priority_high == 1
    priority_medium = generator._risk_to_priority(RiskLevel.MEDIUM)
    assert priority_medium == 3
    priority_low = generator._risk_to_priority(RiskLevel.LOW)
    assert priority_low == 4
    print("✓ Risk levels correctly converted to priorities")
    
    # Test regulatory reference extraction
    print("\n4. Testing regulatory reference extraction...")
    text = "According to GDPR Article 28 and HIPAA §164.308, the processor must..."
    refs = generator.extract_regulatory_references(text)
    assert len(refs) > 0
    assert any("GDPR" in ref for ref in refs)
    print(f"✓ Extracted {len(refs)} regulatory references")
    
    print("\n✓ All RecommendationGenerator tests passed!")


def test_clause_generator():
    """Test ClauseGenerator functionality (without LLaMA)."""
    print("\n=== Testing ClauseGenerator ===")
    
    # Initialize without LLaMA model
    generator = ClauseGenerator(llama_model=None)
    
    # Create test requirement
    requirement = RegulatoryRequirement(
        requirement_id="GDPR_ART28_01",
        framework="GDPR",
        article_reference="GDPR Article 28",
        clause_type="Data Processing",
        description="Processor obligations and data processing terms",
        mandatory=True,
        mandatory_elements=[
            "Processing only on documented instructions",
            "Confidentiality obligations"
        ]
    )
    
    # Test fallback clause generation
    print("\n1. Testing fallback clause generation...")
    clause_text = generator._generate_fallback_clause(requirement)
    assert len(clause_text) > 0
    assert "GDPR Article 28" in clause_text
    assert "Data Processing" in clause_text
    print("✓ Fallback clause generated successfully")
    print(f"  Clause length: {len(clause_text)} characters")
    
    # Test text post-processing
    print("\n2. Testing clause post-processing...")
    raw_text = "GENERATED CLAUSE: the processor shall process data"
    processed = generator._remove_prompt_artifacts(raw_text)
    assert "GENERATED CLAUSE:" not in processed
    print("✓ Prompt artifacts removed successfully")
    
    # Test heading generation
    print("\n3. Testing heading generation...")
    heading = generator._generate_heading("Data_Processing")
    assert "Data Processing" in heading
    print(f"✓ Heading generated: {heading}")
    
    # Test clause validation
    print("\n4. Testing clause validation...")
    validation = generator.validate_generated_clause(clause_text, requirement)
    assert 'valid' in validation
    assert 'issues' in validation
    assert 'warnings' in validation
    print(f"✓ Clause validation completed")
    print(f"  Valid: {validation['valid']}")
    print(f"  Issues: {len(validation['issues'])}")
    print(f"  Warnings: {len(validation['warnings'])}")
    
    print("\n✓ All ClauseGenerator tests passed!")


def test_recommendation_engine():
    """Test RecommendationEngine orchestrator."""
    print("\n=== Testing RecommendationEngine ===")
    
    # Initialize engine without LLaMA
    engine = RecommendationEngine(llama_model=None, use_llama=False)
    
    # Create test compliance report
    requirement = RegulatoryRequirement(
        requirement_id="GDPR_ART28_01",
        framework="GDPR",
        article_reference="GDPR Article 28",
        clause_type="Data Processing",
        description="Processor obligations",
        mandatory=True,
        risk_level=RiskLevel.HIGH
    )
    
    clause_result = ClauseComplianceResult(
        clause_id="clause_001",
        clause_text="The processor shall process data.",
        clause_type="Data Processing",
        framework="GDPR",
        compliance_status=ComplianceStatus.PARTIAL,
        risk_level=RiskLevel.MEDIUM,
        matched_requirements=[requirement],
        confidence=0.75,
        issues=["Missing confidentiality obligations"]
    )
    
    report = ComplianceReport(
        document_id="test_doc_001",
        frameworks_checked=["GDPR"],
        overall_score=65.0,
        clause_results=[clause_result],
        missing_requirements=[requirement],
        high_risk_items=[],
        summary=ComplianceSummary(
            total_clauses=1,
            compliant_clauses=0,
            non_compliant_clauses=0,
            partial_clauses=1,
            high_risk_count=0,
            medium_risk_count=1,
            low_risk_count=0
        )
    )
    
    # Test recommendation generation
    print("\n1. Testing recommendation generation...")
    recommendations = engine.generate_recommendations(report)
    assert isinstance(recommendations, list)
    print(f"✓ Generated {len(recommendations)} recommendations")
    
    if recommendations:
        rec = recommendations[0]
        print(f"  First recommendation:")
        print(f"    Priority: {rec.get_priority_label()}")
        print(f"    Action: {rec.action_type.value}")
        print(f"    Description: {rec.description[:100]}...")
    
    # Test fallback clause generation
    print("\n2. Testing fallback clause generation...")
    clause_text = engine._generate_fallback_clause_text(requirement)
    assert len(clause_text) > 0
    assert "GDPR Article 28" in clause_text
    print("✓ Fallback clause text generated")
    
    # Test statistics
    print("\n3. Testing statistics...")
    stats = engine.get_statistics()
    assert 'recommendations_generated' in stats
    assert 'clauses_generated' in stats
    assert 'errors' in stats
    print("✓ Statistics retrieved successfully")
    print(f"  Recommendations: {stats['recommendations_generated']}")
    print(f"  Clauses: {stats['clauses_generated']}")
    print(f"  Errors: {stats['errors']}")
    
    # Test configuration validation
    print("\n4. Testing configuration validation...")
    validation = engine.validate_configuration()
    assert 'valid' in validation
    print(f"✓ Configuration validated")
    print(f"  Valid: {validation['valid']}")
    print(f"  Issues: {len(validation['issues'])}")
    print(f"  Warnings: {len(validation['warnings'])}")
    
    print("\n✓ All RecommendationEngine tests passed!")


def test_data_models():
    """Test data models."""
    print("\n=== Testing Data Models ===")
    
    # Test ActionType enum
    print("\n1. Testing ActionType enum...")
    assert ActionType.ADD_CLAUSE.value == "Add Clause"
    assert ActionType.MODIFY_CLAUSE.value == "Modify Clause"
    print("✓ ActionType enum working correctly")
    
    # Test Recommendation model
    print("\n2. Testing Recommendation model...")
    requirement = RegulatoryRequirement(
        requirement_id="TEST_01",
        framework="GDPR",
        article_reference="Article 28",
        clause_type="Data Processing",
        description="Test requirement",
        mandatory=True
    )
    
    rec = Recommendation(
        recommendation_id="rec_001",
        requirement=requirement,
        priority=1,
        action_type=ActionType.ADD_CLAUSE,
        description="Add missing clause",
        rationale="Required by regulation",
        regulatory_reference="Article 28"
    )
    
    assert rec.get_priority_label() == "Critical"
    
    # Test to_dict conversion
    rec_dict = rec.to_dict()
    assert 'recommendation_id' in rec_dict
    assert 'priority' in rec_dict
    assert 'action_type' in rec_dict
    print("✓ Recommendation model working correctly")
    
    print("\n✓ All data model tests passed!")


def main():
    """Run all tests."""
    print("=" * 60)
    print("RECOMMENDATION ENGINE TEST SUITE")
    print("=" * 60)
    
    try:
        test_data_models()
        test_prompt_builder()
        test_recommendation_generator()
        test_clause_generator()
        test_recommendation_engine()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED SUCCESSFULLY!")
        print("=" * 60)
        print("\nRecommendation Engine implementation verified.")
        print("Note: LLaMA model integration tested without actual model loading.")
        print("For full testing with LLaMA, ensure the model is downloaded and configured.")
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
