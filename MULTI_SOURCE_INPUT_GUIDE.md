# Multi-Source Input Support Guide

The AI Compliance Checker now supports multiple input methods for contract analysis, making it flexible and easy to use regardless of where your contracts are stored.

## Supported Input Methods

### 1. File Upload

Upload contract documents directly from your computer.

**Supported Formats:**
- PDF (`.pdf`) - Text-based and scanned documents
- Microsoft Word (`.docx`)
- Plain Text (`.txt`)
- Images (`.png`, `.jpg`) - Uses OCR for text extraction

**Features:**
- Automatic file type detection
- File size validation (max 10MB)
- OCR support for scanned documents and images
- Automatic text extraction and cleaning

**Usage:**
1. Select "File Upload" as the upload method
2. Click "Choose a file" or drag and drop
3. Wait for automatic processing
4. Review extracted clauses

**Example:**
```
✅ Document processed successfully!
📄 Extracted 15 clauses (2,450 words) in 2.3s
```

### 2. Text Input

Paste contract text directly into the application.

**Features:**
- Direct text processing
- Minimum length validation (100 characters)
- Same analysis pipeline as file uploads
- Ideal for quick analysis or partial contracts

**Usage:**
1. Select "Text Input" as the upload method
2. Paste your contract text into the text area
3. Click "Process Text"
4. Review extracted clauses

**Best Practices:**
- Ensure text is properly formatted with paragraph breaks
- Include complete clauses for accurate analysis
- Minimum 100 characters required

### 3. Google Sheets Integration

Extract contract text directly from Google Sheets.

**Features:**
- Direct API integration with Google Sheets
- Support for specific sheet names
- Support for cell range selection
- Automatic text extraction from cells
- Secure authentication via service account

**Setup Required:**
See [GOOGLE_SHEETS_SETUP.md](config/GOOGLE_SHEETS_SETUP.md) for detailed setup instructions.

**Usage:**
1. Select "Google Sheets URL" as the upload method
2. Paste your Google Sheets URL
3. (Optional) Specify sheet name and cell range in Advanced Options
4. Click "Process Google Sheet"
5. Review extracted clauses

**URL Format:**
```
https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit
```

**Advanced Options:**
- **Sheet Name**: Specify which sheet to read (defaults to first sheet)
- **Cell Range**: Specify range like "A1:B10" (defaults to all data)

**Example:**
```
✅ Google Sheet processed successfully!
📄 Extracted 12 clauses (1,890 words)
```

## File Size Limits

- **Maximum file size**: 10MB
- **Minimum text length**: 100 characters
- Files exceeding the limit will be rejected with a clear error message

## Error Handling

### File Upload Errors

**Unsupported Format:**
```
❌ Unsupported file format: .xyz
Supported formats: PDF, DOCX, TXT, PNG, JPG
```

**File Too Large:**
```
❌ File size (15.2 MB) exceeds maximum allowed size (10 MB)
```

**Corrupted File:**
```
❌ Error processing document: File appears corrupted
```

### Text Input Errors

**Text Too Short:**
```
⚠️ Please enter at least 100 characters of contract text
```

**Empty Input:**
```
❌ Error processing text: Text input cannot be empty
```

### Google Sheets Errors

**Invalid URL:**
```
❌ Invalid Google Sheets URL
Expected format: https://docs.google.com/spreadsheets/d/{id}/edit
```

**Authentication Error:**
```
❌ Google API credentials not found
See troubleshooting tips below
```

**Permission Denied:**
```
❌ The caller does not have permission
Ensure the sheet is shared with the service account
```

**No Data Found:**
```
❌ No data found in the specified range
Verify the cell range contains data
```

## Troubleshooting

### Google Sheets Issues

1. **Authentication Error**
   - Ensure `google_credentials.json` is in `App/config/`
   - Verify the credentials file is valid JSON
   - Check that Google Sheets API is enabled

2. **Permission Denied**
   - Share the Google Sheet with the service account email
   - Grant at least "Viewer" access
   - Wait a few minutes for permissions to propagate

3. **Sheet Not Found**
   - Verify the URL is correct
   - Check that the sheet exists
   - Ensure the sheet name (if specified) is correct

4. **No Data Found**
   - Verify the cell range is correct
   - Ensure cells contain text data
   - Try leaving range empty to read all data

### OCR Issues

1. **Poor OCR Quality**
   - Ensure image is high resolution (300+ DPI)
   - Check that text is clearly visible
   - Avoid skewed or rotated images

2. **Tesseract Not Installed**
   - Install Tesseract OCR: https://github.com/tesseract-ocr/tesseract
   - Add Tesseract to system PATH
   - Restart the application

### General Processing Issues

1. **Processing Takes Too Long**
   - Large files may take longer to process
   - OCR processing is slower than text extraction
   - Consider splitting large documents

2. **Incorrect Clause Segmentation**
   - Ensure document has clear structure
   - Use headings and numbering
   - Check for proper paragraph breaks

## Best Practices

### For File Uploads
- Use text-based PDFs when possible (faster processing)
- Ensure scanned documents are high quality
- Keep files under 10MB for optimal performance

### For Text Input
- Include complete clauses with context
- Maintain original formatting and structure
- Use for quick analysis or testing

### For Google Sheets
- Organize contract text in a single column
- Use clear cell ranges for specific sections
- Keep one contract per sheet for clarity
- Share sheets with service account before processing

## Performance Considerations

| Input Method | Typical Processing Time | Best For |
|--------------|------------------------|----------|
| Text-based PDF | 1-3 seconds | Standard contracts |
| Scanned PDF/Image | 5-15 seconds | Legacy documents |
| DOCX | 1-2 seconds | Modern contracts |
| Text Input | < 1 second | Quick analysis |
| Google Sheets | 2-5 seconds | Collaborative workflows |

## Security Notes

### File Upload
- Files are processed in temporary storage
- Temporary files are deleted after processing
- No files are permanently stored on server

### Text Input
- Text is processed in memory only
- No persistent storage of input text
- Session data cleared on browser close

### Google Sheets
- Uses service account authentication
- Read-only access to sheets
- Credentials stored securely in config folder
- Never commit credentials to version control

## Examples

### Example 1: Upload PDF Contract
```
1. Click "File Upload"
2. Select "contract.pdf"
3. Wait for processing
4. Click "Analyze Contract"
```

### Example 2: Paste Contract Text
```
1. Click "Text Input"
2. Paste contract text
3. Click "Process Text"
4. Click "Analyze Contract"
```

### Example 3: Import from Google Sheets
```
1. Click "Google Sheets URL"
2. Paste: https://docs.google.com/spreadsheets/d/abc123/edit
3. (Optional) Set Sheet Name: "Contract Terms"
4. (Optional) Set Range: "A1:A50"
5. Click "Process Google Sheet"
6. Click "Analyze Contract"
```

## API Reference

### DocumentProcessor Methods

```python
# Process file upload
processed_doc = processor.process_document(
    file_path="contract.pdf",
    file_type="pdf",  # Optional, auto-detected
    use_ocr=False     # Force OCR if True
)

# Process text input
processed_doc = processor.process_text(
    text="Contract text here...",
    filename="contract.txt"  # Optional
)

# Process Google Sheets
processed_doc = processor.process_google_sheet(
    url="https://docs.google.com/spreadsheets/d/...",
    sheet_name="Sheet1",  # Optional
    cell_range="A1:B10"   # Optional
)
```

## Support

For issues or questions:
1. Check this guide for common solutions
2. Review error messages and troubleshooting tips
3. Check application logs in `App/logs/`
4. Consult [GOOGLE_SHEETS_SETUP.md](config/GOOGLE_SHEETS_SETUP.md) for Google Sheets issues

## Future Enhancements

Planned features:
- Support for additional file formats (RTF, ODT)
- Batch processing of multiple files
- Direct integration with cloud storage (Dropbox, OneDrive)
- Email attachment processing
- API endpoint for programmatic access
