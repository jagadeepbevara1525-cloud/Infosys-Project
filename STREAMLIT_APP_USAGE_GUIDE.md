# Streamlit Application Usage Guide

## Overview
The AI-Powered Regulatory Compliance Checker is now fully integrated with real analysis capabilities. This guide explains how to use the application effectively.

## Getting Started

### 1. Launch the Application

```bash
cd App
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### 2. Configure Regulatory Frameworks

**Location:** Left sidebar under "Regulatory Frameworks"

**Steps:**
1. Select one or more frameworks to check against:
   - ✅ GDPR (General Data Protection Regulation)
   - ✅ HIPAA (Health Insurance Portability and Accountability Act)
   - ✅ CCPA (California Consumer Privacy Act)
   - ✅ SOX (Sarbanes-Oxley Act)

2. At least one framework must be selected
3. The UI will show a warning if no frameworks are selected
4. A success message shows the count of selected frameworks

**Note:** Framework selection affects all subsequent analyses

### 3. Adjust Analysis Settings (Optional)

**Location:** Left sidebar under "Analysis Settings"

**Available Settings:**
- **Risk Tolerance:** Low / Medium / High
- **Confidence Threshold:** 50% - 95% (default: 75%)
  - Higher threshold = more conservative classification
  - Lower threshold = more clauses classified with lower confidence

## Using the Application

### Tab 1: Contract Analysis

#### Upload a Contract

**Method 1: File Upload**
1. Select "File Upload" radio button
2. Click "Choose a file" or drag and drop
3. Supported formats:
   - PDF (text-based or scanned)
   - DOCX (Microsoft Word)
   - TXT (plain text)
   - PNG, JPG (images with OCR)
4. Maximum file size: 10MB
5. Document is processed automatically upon upload

**Method 2: Text Input**
1. Select "Text Input" radio button
2. Paste contract text into the text area
3. Minimum 100 characters required
4. Click "Process Text" button
5. Text is segmented into clauses

**Method 3: Google Sheets URL**
- Currently a placeholder
- Coming in future release

#### Processing Feedback

After upload, you'll see:
- ✅ Success message
- 📄 Number of clauses extracted
- 📊 Total word count
- ⏱️ Processing time

#### Analyze the Contract

1. Ensure a document is uploaded (status shows "✅ Document Ready")
2. Ensure at least one framework is selected
3. Click "🚀 Analyze Contract" button
4. Watch the progress indicators:
   - Step 1/3: Analyzing clauses (NLP classification)
   - Step 2/3: Checking compliance (regulatory matching)
   - Step 3/3: Generating recommendations (AI suggestions)

#### View Quick Results

After analysis completes, you'll see:
- **Compliance Score:** Overall percentage (0-100%)
- **High Risk Items:** Count of high-risk findings
- **Missing Clauses:** Count of missing mandatory requirements

### Tab 2: Dashboard

**Overview Metrics:**
- Overall Compliance: Current compliance percentage
- High Risk Items: Count of high-risk issues
- Contracts Analyzed: Total contracts in history
- Missing Clauses: Count of missing requirements

**Compliance by Framework Chart:**
- Bar chart showing compliance score per framework
- Red target line at 90%
- Hover for exact values

**Risk Distribution Chart:**
- Pie chart showing breakdown of risk levels
- Color-coded: Red (High), Yellow (Medium), Green (Low)
- Only shows non-zero values

**Recent Analysis Activity:**
- Table of all analyzed contracts
- Columns: Contract name, Date, Status, Risk, Score
- Sortable and searchable

### Tab 3: Clause Details

**Filtering Options:**

1. **Risk Level Filter:**
   - High, Medium, Low
   - Default: High and Medium selected
   - Shows only clauses matching selected risk levels

2. **Regulation Filter:**
   - GDPR, HIPAA, CCPA, SOX
   - Default: All selected frameworks
   - Shows only clauses for selected regulations

3. **Status Filter:**
   - Compliant, Non-Compliant, Partial
   - Default: Non-Compliant and Partial
   - Focus on issues that need attention

**Clause Details:**

Each clause shows:
- **Clause ID:** Unique identifier
- **Clause Type:** Classification (e.g., Data Processing)
- **Framework:** Which regulation it applies to
- **Risk Level:** Color-coded (Red/Yellow/Green)
- **Compliance Status:** Compliant/Non-Compliant/Partial
- **Confidence:** Classification confidence percentage
- **Clause Text:** Full or truncated text
- **Issues:** List of specific problems found
- **Recommendations:** Actionable suggestions

**Fix Button:**
- Available for non-compliant clauses
- Click to show suggested compliant text
- Generated text appears below recommendation

**Missing Required Clauses Section:**

Shows all missing mandatory requirements:
- Requirement name and framework
- Article reference (e.g., GDPR Article 28)
- Description of requirement
- Required elements list
- "Show Suggested Clause" button for AI-generated text

### Tab 4: Regulatory Updates

**Note:** This tab currently shows placeholder data for demonstration purposes. Real regulatory update tracking will be implemented in a future release.

### Tab 5: Settings

**Note:** This tab currently shows configuration options for demonstration purposes. Integration settings (API keys, etc.) will be implemented in a future release.

## Understanding Results

### Compliance Scores

- **90-100%:** Excellent compliance
- **80-89%:** Good compliance, minor issues
- **70-79%:** Moderate compliance, needs attention
- **Below 70%:** Poor compliance, immediate action required

### Risk Levels

- **High (Red):** Critical issues, legal/financial risk
  - Missing mandatory clauses
  - Violations of key requirements
  - Immediate remediation needed

- **Medium (Yellow):** Important issues, moderate risk
  - Incomplete clauses
  - Missing recommended elements
  - Should be addressed soon

- **Low (Green):** Minor issues, low risk
  - Compliant clauses
  - Minor improvements possible
  - No immediate action required

### Compliance Status

- **Compliant:** Clause meets all requirements
- **Non-Compliant:** Clause missing or violates requirements
- **Partial:** Clause present but incomplete

## Best Practices

### 1. Document Preparation
- Use high-quality scans for image-based PDFs
- Ensure text is readable and well-formatted
- Remove unnecessary headers/footers if possible

### 2. Framework Selection
- Select only relevant frameworks for your use case
- Don't select all frameworks unless necessary
- Consider your industry and jurisdiction

### 3. Analysis Workflow
1. Upload document
2. Review extraction results
3. Select appropriate frameworks
4. Run analysis
5. Review dashboard for overview
6. Examine clause details for specifics
7. Address high-risk items first
8. Review recommendations
9. Export results for documentation

### 4. Interpreting Results
- Focus on high-risk items first
- Review missing requirements carefully
- Consider confidence scores when evaluating classifications
- Use recommendations as guidance, not absolute rules
- Consult legal professionals for final decisions

### 5. Performance Tips
- Smaller documents process faster
- Text-based PDFs are faster than scanned PDFs
- Fewer frameworks = faster analysis
- Use caching (automatic) for repeated analyses

## Troubleshooting

### Document Upload Issues

**Problem:** File upload fails
- **Solution:** Check file size (max 10MB), format (PDF/DOCX/TXT/PNG/JPG)

**Problem:** OCR extraction fails
- **Solution:** Ensure Tesseract is installed, try text-based PDF instead

**Problem:** No clauses extracted
- **Solution:** Check document formatting, ensure text is readable

### Analysis Issues

**Problem:** Analysis button disabled
- **Solution:** Upload a document first, select at least one framework

**Problem:** Low confidence scores
- **Solution:** Normal for ambiguous clauses, review manually

**Problem:** Analysis takes too long
- **Solution:** Large documents take time, be patient, check logs

### Display Issues

**Problem:** Dashboard shows no data
- **Solution:** Run an analysis first

**Problem:** Filters show no results
- **Solution:** Adjust filter settings, check if clauses match criteria

## Technical Details

### Session State
The application maintains state across interactions:
- Processed documents persist until page refresh
- Analysis results cached for quick access
- Contract history maintained during session
- Framework selection remembered

### Caching
Services are cached for performance:
- Models loaded once and reused
- Embeddings cached automatically
- Regulatory requirements precomputed

### Logging
All operations are logged:
- Check console for detailed logs
- Errors logged with stack traces
- Performance metrics tracked

## Export and Reporting

**Note:** Export functionality (PDF, JSON, CSV) will be implemented in Task 8. Currently, you can:
- View results in the application
- Take screenshots
- Copy text from clause details

## Support and Feedback

For issues or questions:
1. Check this guide first
2. Review error messages in the UI
3. Check console logs for details
4. Consult technical documentation
5. Contact development team

## Future Enhancements

Coming soon:
- Export functionality (PDF, JSON, CSV)
- Google Sheets integration
- Visual highlighting in documents
- Interactive clause tooltips
- Missing clause side panel
- Performance optimizations
- Enhanced error messages

## Version Information

- **Version:** 1.0.0
- **Last Updated:** October 15, 2024
- **Status:** Production Ready (Core Features)

---

**Happy Analyzing! 🎉**
