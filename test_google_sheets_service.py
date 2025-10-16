"""Tests for Google Sheets service."""

import pytest
from pathlib import Path
from services.google_sheets_service import (
    GoogleSheetsService,
    GoogleSheetsError,
    AuthenticationError,
    SheetNotFoundError
)


class TestGoogleSheetsService:
    """Test Google Sheets service functionality."""
    
    def test_parse_valid_url(self):
        """Test parsing valid Google Sheets URL."""
        service = GoogleSheetsService()
        
        url = "https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit"
        spreadsheet_id, sheet_name = service.parse_sheet_url(url)
        
        assert spreadsheet_id == "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
    
    def test_parse_url_with_gid(self):
        """Test parsing URL with gid parameter."""
        service = GoogleSheetsService()
        
        url = "https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit#gid=0"
        spreadsheet_id, sheet_name = service.parse_sheet_url(url)
        
        assert spreadsheet_id == "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
    
    def test_parse_invalid_url(self):
        """Test parsing invalid URL raises error."""
        service = GoogleSheetsService()
        
        with pytest.raises(GoogleSheetsError):
            service.parse_sheet_url("https://invalid-url.com")
    
    def test_validate_url_valid(self):
        """Test URL validation with valid URL."""
        service = GoogleSheetsService()
        
        url = "https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit"
        assert service.validate_url(url) is True
    
    def test_validate_url_invalid(self):
        """Test URL validation with invalid URL."""
        service = GoogleSheetsService()
        
        assert service.validate_url("https://invalid-url.com") is False
    
    def test_credentials_path_default(self):
        """Test default credentials path."""
        service = GoogleSheetsService()
        
        assert "google_credentials.json" in service.credentials_path
        assert "config" in service.credentials_path
    
    def test_credentials_path_custom(self):
        """Test custom credentials path."""
        custom_path = "/custom/path/credentials.json"
        service = GoogleSheetsService(credentials_path=custom_path)
        
        assert service.credentials_path == custom_path
    
    def test_authentication_error_no_credentials(self):
        """Test authentication error when credentials file doesn't exist."""
        service = GoogleSheetsService(credentials_path="/nonexistent/path.json")
        
        with pytest.raises(AuthenticationError):
            service._initialize_service()
    
    def test_extract_text_invalid_url(self):
        """Test extracting text with invalid URL."""
        service = GoogleSheetsService()
        
        with pytest.raises(GoogleSheetsError):
            service.extract_text_from_sheet("https://invalid-url.com")


class TestGoogleSheetsIntegration:
    """Integration tests for Google Sheets (requires credentials)."""
    
    @pytest.fixture
    def service(self):
        """Create service instance."""
        return GoogleSheetsService()
    
    @pytest.fixture
    def has_credentials(self, service):
        """Check if credentials are available."""
        return Path(service.credentials_path).exists()
    
    @pytest.mark.skipif(
        not Path("App/config/google_credentials.json").exists(),
        reason="Google API credentials not configured"
    )
    def test_connection(self, service):
        """Test connection to Google Sheets API."""
        assert service.test_connection() is True
    
    @pytest.mark.skipif(
        not Path("App/config/google_credentials.json").exists(),
        reason="Google API credentials not configured"
    )
    def test_extract_text_from_public_sheet(self, service):
        """Test extracting text from a public Google Sheet."""
        # This is a public test sheet
        url = "https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit"
        
        try:
            text = service.extract_text_from_sheet(url)
            assert len(text) > 0
            assert isinstance(text, str)
        except GoogleSheetsError as e:
            # Expected if sheet is not shared with service account
            pytest.skip(f"Sheet not accessible: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
