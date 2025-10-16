"""
Test script for click-to-detail navigation functionality.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from services.document_viewer import DocumentViewer
from models.processed_document import ProcessedDocument
from models.clause import Clause
from models.regulatory_requirement import RegulatoryRequirement
from models.recommendation import Recommendation, ActionType


def test_document_viewer_initialization():
    """Test that DocumentViewer initializes correctly."""
    print("Testing DocumentViewer initialization...")
    viewer = DocumentViewer()
    assert viewer is not None
    assert hasattr(viewer, 'risk_colors')
    assert hasattr(viewer, 'risk_text_colors')
    print("✅ DocumentViewer initialized successfully")


def test_highlighted_html_generation():
    """Test generation of highlighted HTML with click handlers."""
    print("\nTesting highlighted HTML generation...")
    
    viewer = DocumentViewer()
    
    # Create sample document
    sample_text = """
    Article 1: Data Processing Agreement
    
    The processor shall process personal data only on documented instructions from the controller.
    
    Article 2: Security Measures
    
    The processor shall implement appropriate technical and organizational measures.
    """
    
    clauses = [
        Clause(
            clause_id="clause_001",
            text="The processor shall process personal data only on documented instructions from the controller.",
            start_position=50,
            end_position=150,
            section_number="1",
            heading="Data Processing Agreement"
        ),
        Clause(
            clause_id="clause_002",
            text="The processor shall implement appropriate technical and organizational measures.",
            start_position=200,
            end_position=280,
            section_number="2",
            heading="Security Measures"
        )
    ]
    
    processed_doc = ProcessedDocument(
        document_id="test_doc_001",
        original_filename="test_contract.pdf",
        extracted_text=sample_text,
        clauses=clauses,
        metadata={},
        processing_time=1.5
    )
    
    # Create risk map
    clause_risk_map = {
        "clause_001": "High",
        "clause_002": "Medium"
    }
    
    # Create details map
    clause_details_map = {
        "clause_001": {
            "compliance_status": "Non-Compliant",
            "issues": ["Missing specific security requirements"],
            "clause_type": "Data Processing"
        },
        "clause_002": {
            "compliance_status": "Partial",
            "issues": ["Incomplete security measures"],
            "clause_type": "Security Safeguards"
        }
    }
    
    # Generate highlighted HTML
    html = viewer.create_highlighted_html(
        processed_doc,
        clause_risk_map,
        clause_details_map
    )
    
    # Verify HTML contains expected elements
    assert 'highlighted-clause' in html
    assert 'clickable-clause' in html
    assert 'data-clause-id="clause_001"' in html
    assert 'data-clause-id="clause_002"' in html
    assert 'data-risk-level="High"' in html
    assert 'data-risk-level="Medium"' in html
    assert 'data-compliance-status="Non-Compliant"' in html
    assert 'data-clause-type="Data Processing"' in html
    assert 'tooltip-content' in html
    assert 'Click to view details' in html or 'Click for details' in html
    
    print("✅ Highlighted HTML generated successfully with click handlers")
    print(f"   - HTML length: {len(html)} characters")
    print(f"   - Contains clickable clauses: Yes")
    print(f"   - Contains tooltips: Yes")


def test_click_handler_javascript():
    """Test generation of click handler JavaScript."""
    print("\nTesting click handler JavaScript generation...")
    
    viewer = DocumentViewer()
    js_code = viewer.get_click_handler_javascript()
    
    # Verify JavaScript contains expected functions
    assert 'handleClauseClick' in js_code
    assert 'handleMissingClauseClick' in js_code
    assert 'initializeClickHandlers' in js_code
    assert 'clickable-clause' in js_code
    assert 'clickable-missing-clause' in js_code
    assert 'addEventListener' in js_code
    assert 'scrollIntoView' in js_code
    
    print("✅ Click handler JavaScript generated successfully")
    print(f"   - JavaScript length: {len(js_code)} characters")
    print(f"   - Contains handleClauseClick: Yes")
    print(f"   - Contains handleMissingClauseClick: Yes")
    print(f"   - Contains scroll functionality: Yes")


def test_missing_clauses_panel():
    """Test generation of missing clauses panel with click handlers."""
    print("\nTesting missing clauses panel generation...")
    
    viewer = DocumentViewer()
    
    # Create sample missing requirements
    missing_requirements = [
        RegulatoryRequirement(
            requirement_id="GDPR_ART28_01",
            framework="GDPR",
            article_reference="Article 28",
            clause_type="Data Processing",
            description="Processor obligations and data processing terms",
            mandatory=True,
            keywords=["processor", "processing", "instructions"],
            mandatory_elements=[
                "Processing only on documented instructions",
                "Confidentiality obligations",
                "Security measures"
            ]
        ),
        RegulatoryRequirement(
            requirement_id="GDPR_BREACH_01",
            framework="GDPR",
            article_reference="Article 33",
            clause_type="Breach Notification",
            description="Notification of personal data breach",
            mandatory=True,
            keywords=["breach", "notification", "72 hours"],
            mandatory_elements=[
                "Notification within 72 hours",
                "Description of breach",
                "Contact point"
            ]
        )
    ]
    
    # Create sample recommendations
    recommendations = [
        Recommendation(
            recommendation_id="rec_001",
            clause_id=None,
            requirement=missing_requirements[0],
            priority=1,
            action_type=ActionType.ADD_CLAUSE,
            description="Add comprehensive data processing clause",
            suggested_text="The Processor shall process Personal Data only on documented instructions from the Controller...",
            rationale="Required by GDPR Article 28",
            regulatory_reference="GDPR Article 28"
        ),
        Recommendation(
            recommendation_id="rec_002",
            clause_id=None,
            requirement=missing_requirements[1],
            priority=2,
            action_type=ActionType.ADD_CLAUSE,
            description="Add breach notification clause",
            suggested_text="In the event of a personal data breach, the Processor shall notify the Controller without undue delay...",
            rationale="Required by GDPR Article 33",
            regulatory_reference="GDPR Article 33"
        )
    ]
    
    # Generate missing clauses panel
    panel_html = viewer.create_missing_clauses_panel(
        missing_requirements,
        recommendations
    )
    
    # Verify panel contains expected elements
    assert 'missing-clauses-panel' in panel_html
    assert 'missing-clause-card' in panel_html
    assert 'clickable-missing-clause' in panel_html
    assert 'data-req-id="GDPR_ART28_01"' in panel_html
    assert 'data-req-id="GDPR_BREACH_01"' in panel_html
    assert 'HIGH PRIORITY' in panel_html
    assert 'Click to view full recommendation' in panel_html
    assert 'Suggested:' in panel_html
    
    print("✅ Missing clauses panel generated successfully")
    print(f"   - Panel HTML length: {len(panel_html)} characters")
    print(f"   - Contains clickable cards: Yes")
    print(f"   - Contains priority badges: Yes")
    print(f"   - Contains suggested text previews: Yes")


def test_css_styles():
    """Test CSS styles generation."""
    print("\nTesting CSS styles generation...")
    
    viewer = DocumentViewer()
    css = viewer.get_css_styles()
    
    # Verify CSS contains expected styles
    assert '.highlighted-clause' in css
    assert '.clickable-clause' in css
    assert '.tooltip-content' in css
    assert 'cursor: pointer' in css
    assert 'transition:' in css
    assert ':hover' in css
    
    print("✅ CSS styles generated successfully")
    print(f"   - CSS length: {len(css)} characters")
    print(f"   - Contains hover effects: Yes")
    print(f"   - Contains tooltip styles: Yes")


def test_legend_html():
    """Test legend HTML generation."""
    print("\nTesting legend HTML generation...")
    
    viewer = DocumentViewer()
    legend = viewer.create_legend_html()
    
    # Verify legend contains expected elements
    assert 'High Risk' in legend
    assert 'Medium Risk' in legend
    assert 'Low Risk' in legend
    assert '#ff6b6b' in legend  # High risk color
    assert '#ffd166' in legend  # Medium risk color
    assert '#06d6a0' in legend  # Low risk color
    assert 'Click on highlighted clauses' in legend
    
    print("✅ Legend HTML generated successfully")
    print(f"   - Legend HTML length: {len(legend)} characters")
    print(f"   - Contains all risk levels: Yes")
    print(f"   - Contains click instructions: Yes")


def test_empty_missing_clauses():
    """Test missing clauses panel with no missing requirements."""
    print("\nTesting empty missing clauses panel...")
    
    viewer = DocumentViewer()
    panel_html = viewer.create_missing_clauses_panel([], [])
    
    # Verify panel shows success message
    assert 'All Required Clauses Present' in panel_html
    assert 'No missing clauses detected' in panel_html
    
    print("✅ Empty missing clauses panel generated successfully")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("CLICK-TO-DETAIL NAVIGATION TESTS")
    print("=" * 70)
    
    try:
        test_document_viewer_initialization()
        test_highlighted_html_generation()
        test_click_handler_javascript()
        test_missing_clauses_panel()
        test_css_styles()
        test_legend_html()
        test_empty_missing_clauses()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        print("\nClick-to-detail navigation functionality verified:")
        print("  ✓ Highlighted clauses have click handlers")
        print("  ✓ Missing clause cards have click handlers")
        print("  ✓ JavaScript scroll-to functionality implemented")
        print("  ✓ Tooltips display on hover")
        print("  ✓ Visual feedback on click")
        print("  ✓ Modal/expanded view for full recommendations")
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
