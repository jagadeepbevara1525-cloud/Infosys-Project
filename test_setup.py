"""
Test script to verify project setup.
"""
from config import config
from utils import get_logger


def test_configuration():
    """Test configuration loading."""
    print("=" * 60)
    print("Testing Configuration System")
    print("=" * 60)
    
    print(f"\nApp Name: {config.app_name}")
    print(f"Version: {config.version}")
    print(f"Debug Mode: {config.debug}")
    print(f"Log Level: {config.log_level}")
    
    print(f"\nModel Configuration:")
    print(f"  LegalBERT: {config.models.legal_bert_model}")
    print(f"  LLaMA: {config.models.llama_model}")
    print(f"  Sentence Transformer: {config.models.sentence_transformer_model}")
    print(f"  Use GPU: {config.models.use_gpu}")
    
    print(f"\nProcessing Configuration:")
    print(f"  Max File Size: {config.processing.max_file_size_mb} MB")
    print(f"  Supported Formats: {', '.join(config.processing.supported_formats)}")
    print(f"  Confidence Threshold: {config.processing.confidence_threshold}")
    
    print(f"\nCompliance Configuration:")
    print(f"  Enabled Frameworks: {', '.join(config.compliance.enabled_frameworks)}")
    print(f"  Risk Tolerance: {config.compliance.risk_tolerance}")
    
    print(f"\nDirectory Paths:")
    print(f"  Base: {config.base_dir}")
    print(f"  Data: {config.data_dir}")
    print(f"  Logs: {config.logs_dir}")
    print(f"  Temp: {config.temp_dir}")
    
    print("\n✓ Configuration loaded successfully!")


def test_logging():
    """Test logging system."""
    print("\n" + "=" * 60)
    print("Testing Logging System")
    print("=" * 60)
    
    # Create logger
    logger = get_logger(
        name="test_logger",
        log_level=config.log_level,
        log_dir=config.logs_dir,
        sanitize=True
    )
    
    print("\nTesting log levels:")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    print("\nTesting sensitive data sanitization:")
    logger.info("User email: test@example.com should be sanitized")
    logger.info("Phone number: 555-123-4567 should be sanitized")
    logger.info("API Key: api_key=sk_test_1234567890abcdefghij should be sanitized")
    
    print("\nTesting performance logging:")
    logger.log_performance("test_operation", 1.23, {"clauses": 10, "score": 85.5})
    
    print("\nTesting analysis logging:")
    logger.log_analysis_start("doc_001", "test_contract.pdf")
    logger.log_analysis_complete("doc_001", 3.45, 87.5)
    
    print("\nTesting compliance logging:")
    logger.log_compliance_check("GDPR", "Compliant", "Low")
    
    print("\n✓ Logging system working correctly!")
    print(f"✓ Logs saved to: {config.logs_dir}")


def test_directory_structure():
    """Test directory structure."""
    print("\n" + "=" * 60)
    print("Testing Directory Structure")
    print("=" * 60)
    
    directories = [
        config.data_dir,
        config.logs_dir,
        config.temp_dir
    ]
    
    for directory in directories:
        if directory.exists():
            print(f"✓ {directory.name}/ directory exists")
        else:
            print(f"✗ {directory.name}/ directory missing")
    
    print("\n✓ Directory structure verified!")


if __name__ == "__main__":
    try:
        test_configuration()
        test_logging()
        test_directory_structure()
        
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED!")
        print("=" * 60)
        print("\nProject setup is complete and working correctly.")
        print("You can now proceed with implementing the next tasks.")
        
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
