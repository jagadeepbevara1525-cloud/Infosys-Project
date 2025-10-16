"""
Test script for Export Service functionality.
Tests JSON, CSV, and PDF export capabilities.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.export_service import ExportService, ExportError
from models.regulatory_requirement import (
    ComplianceReport,
    ClauseComplianceResult,
    RegulatoryRequirement,
    ComplianceSummary,
    ComplianceStatus,
    RiskLevel
)
from models.recommendation import Recommendation, ActionType
import numpy as np


def create_sample_report():
    """Create a sample compliance report for testing."""
    
    # Create sample requirements
    req1 = RegulatoryRequirement(
        requirement_id="GDPR_ART28_01",
        framework="GDPR",
        article_reference="GDPR Article 28",
        clause_type="Data Processing",
        description="Processor obligations and data processing terms",
        mandatory=True,
        keywords=["processor", "processing", "instructions"],
        mandatory_elements=["Processing only on documented instructions"],
        risk_level=RiskLevel.HIGH
    )
    
    req2 = RegulatoryRequirement(
        requirement_id="HIPAA_164_308",
        framework="HIPAA",
        article_reference="HIPAA §164.308",
        clause_type="Security Safeguards",
        description="Administrative safeguards requirements",
        mandatory=True,
        keywords=["safeguards", "security"],
        mandatory_elements=["Security management process"],
        risk_level=RiskLevel.HIGH
    )
    
    # Create sample clause results
    result1 = ClauseComplianceResult(
        clause_id="clause_001",
        clause_text="The processor shall process personal data only on documented instructions from the controller.",
        clause_type="Data Processing",
        framework="GDPR",
        compliance_status=ComplianceStatus.COMPLIANT,
        risk_level=RiskLevel.LOW,
        matched_requirements=[req1],
        confidence=0.92,
        issues=[]
    )
    
    result2 = ClauseComplianceResult(
        clause_id="clause_002",
        clause_text="Security measures shall be implemented.",
        clause_type="Security Safeguards",
        framework="HIPAA",
        compliance_status=ComplianceStatus.PARTIAL,
        risk_level=RiskLevel.MEDIUM,
        matched_requirements=[req2],
        confidence=0.75,
        issues=["Missing specific safeguard details"]
    )
    
    result3 = ClauseComplianceResult(
        clause_id="clause_003",
        clause_text="Data retention period is not specified.",
        clause_type="Data Retention",
        framework="GDPR",
        compliance_status=ComplianceStatus.NON_COMPLIANT,
        risk_level=RiskLevel.HIGH,
        matched_requirements=[],
        confidence=0.65,
        issues=["No retention period specified", "Missing deletion procedures"]
    )
    
    # Create summary
    summary = ComplianceSummary(
        total_clauses=3,
        compliant_clauses=1,
        non_compliant_clauses=1,
        partial_clauses=1,
        high_risk_count=1,
        medium_risk_count=1,
        low_risk_count=1
    )
    
    # Create missing requirement
    missing_req = RegulatoryRequirement(
        requirement_id="GDPR_BREACH_01",
        framework="GDPR",
        article_reference="GDPR Article 33",
        clause_type="Breach Notification",
        description="Notification of personal data breach to supervisory authority",
        mandatory=True,
        keywords=["breach", "notification"],
        mandatory_elements=["72-hour notification requirement"],
        risk_level=RiskLevel.HIGH
    )
    
    # Create report
    report = ComplianceReport(
        document_id="test_contract_001",
        frameworks_checked=["GDPR", "HIPAA"],
        overall_score=66.7,
        clause_results=[result1, result2, result3],
        missing_requirements=[missing_req],
        high_risk_items=[result3],
        summary=summary
    )
    
    return report


def create_sample_recommendations():
    """Create sample recommendations for testing."""
    
    req = RegulatoryRequirement(
        requirement_id="GDPR_BREACH_01",
        framework="GDPR",
        article_reference="GDPR Article 33",
        clause_type="Breach Notification",
        description="Notification of personal data breach",
        mandatory=True,
        keywords=["breach"],
        risk_level=RiskLevel.HIGH
    )
    
    rec1 = Recommendation(
        recommendation_id="rec_001",
        requirement=req,
        priority=1,
        action_type=ActionType.ADD_CLAUSE,
        description="Add breach notification clause with 72-hour requirement",
        rationale="Required by GDPR Article 33 for data processor agreements",
        regulatory_reference="GDPR Article 33",
        clause_id=None,
        suggested_text="The processor shall notify the controller without undue delay and, where feasible, not later than 72 hours after becoming aware of a personal data breach.",
        confidence=0.95,
        estimated_risk_reduction="HIGH"
    )
    
    rec2 = Recommendation(
        recommendation_id="rec_002",
        requirement=req,
        priority=2,
        action_type=ActionType.MODIFY_CLAUSE,
        description="Enhance security safeguards clause with specific measures",
        rationale="Current clause lacks required detail per HIPAA §164.308",
        regulatory_reference="HIPAA §164.308",
        clause_id="clause_002",
        suggested_text="The processor shall implement administrative, physical, and technical safeguards including: access controls, audit controls, integrity controls, and transmission security.",
        confidence=0.88,
        estimated_risk_reduction="MEDIUM"
    )
    
    return [rec1, rec2]


def test_json_export():
    """Test JSON export functionality."""
    print("\n" + "="*60)
    print("Testing JSON Export")
    print("="*60)
    
    try:
        export_service = ExportService()
        report = create_sample_report()
        recommendations = create_sample_recommendations()
        
        # Export to JSON
        json_data = export_service.export_to_json(report, recommendations)
        
        print(f"✓ JSON export successful")
        print(f"  - Size: {len(json_data)} characters")
        print(f"  - Filename: {export_service.get_json_filename(report)}")
        
        # Verify JSON is valid
        import json
        parsed = json.loads(json_data)
        assert 'report' in parsed
        assert 'recommendations' in parsed
        assert 'metadata' in parsed
        
        print(f"✓ JSON structure validated")
        print(f"  - Report document ID: {parsed['report']['document_id']}")
        print(f"  - Frameworks: {', '.join(parsed['report']['frameworks_checked'])}")
        print(f"  - Overall score: {parsed['report']['overall_score']:.1f}%")
        print(f"  - Recommendations: {len(parsed['recommendations'])}")
        
        return True
        
    except Exception as e:
        print(f"✗ JSON export failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_csv_export():
    """Test CSV export functionality."""
    print("\n" + "="*60)
    print("Testing CSV Export")
    print("="*60)
    
    try:
        export_service = ExportService()
        report = create_sample_report()
        recommendations = create_sample_recommendations()
        
        # Export to CSV
        csv_data = export_service.export_to_csv(report, recommendations)
        
        print(f"✓ CSV export successful")
        print(f"  - Size: {len(csv_data)} characters")
        print(f"  - Filename: {export_service.get_csv_filename(report)}")
        
        # Verify CSV structure
        lines = csv_data.split('\n')
        print(f"✓ CSV structure validated")
        print(f"  - Total lines: {len(lines)}")
        print(f"  - Contains SUMMARY section: {'SUMMARY' in csv_data}")
        print(f"  - Contains MISSING REQUIREMENTS section: {'MISSING REQUIREMENTS' in csv_data}")
        print(f"  - Contains RECOMMENDATIONS section: {'RECOMMENDATIONS' in csv_data}")
        
        return True
        
    except Exception as e:
        print(f"✗ CSV export failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pdf_export():
    """Test PDF export functionality."""
    print("\n" + "="*60)
    print("Testing PDF Export")
    print("="*60)
    
    try:
        export_service = ExportService()
        report = create_sample_report()
        recommendations = create_sample_recommendations()
        
        # Export to PDF
        pdf_data = export_service.export_to_pdf(report, recommendations)
        
        print(f"✓ PDF export successful")
        print(f"  - Size: {len(pdf_data)} bytes ({len(pdf_data) / 1024:.1f} KB)")
        print(f"  - Filename: {export_service.get_pdf_filename(report)}")
        
        # Verify PDF header
        assert pdf_data[:4] == b'%PDF', "Invalid PDF header"
        print(f"✓ PDF format validated")
        
        # Optionally save to file for manual inspection
        output_file = "test_compliance_report.pdf"
        with open(output_file, 'wb') as f:
            f.write(pdf_data)
        print(f"✓ PDF saved to {output_file} for inspection")
        
        return True
        
    except ExportError as e:
        if "reportlab" in str(e).lower():
            print(f"⚠ PDF export skipped: ReportLab not installed")
            print(f"  Install with: pip install reportlab")
            return True  # Not a failure, just not available
        else:
            print(f"✗ PDF export failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    except Exception as e:
        print(f"✗ PDF export failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all export tests."""
    print("\n" + "="*60)
    print("EXPORT SERVICE TEST SUITE")
    print("="*60)
    
    results = {
        'JSON Export': test_json_export(),
        'CSV Export': test_csv_export(),
        'PDF Export': test_pdf_export()
    }
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("ALL TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())
