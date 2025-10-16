# Quick Start Guide

## Prerequisites

Ensure you have completed the setup:
```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
python test_setup.py
```

## Running the Application

### Option 1: Streamlit Web Interface (Recommended)

```bash
cd App
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`

### Option 2: Test Integration

```bash
cd App
python test_streamlit_integration.py
```

This runs automated tests to verify all services are working correctly.

## First-Time Usage

### 1. Launch Application
```bash
streamlit run app.py
```

### 2. Select Frameworks
In the left sidebar, check at least one regulatory framework:
- ✅ GDPR
- ✅ HIPAA
- ✅ CCPA
- ✅ SOX

### 3. Upload a Contract
Go to the "Contract Analysis" tab:
- Click "Choose a file" or drag and drop
- Supported formats: PDF, DOCX, TXT, PNG, JPG
- Maximum size: 10MB

### 4. Analyze
- Wait for document processing to complete
- Click "🚀 Analyze Contract"
- Watch the 3-step progress indicator
- View results when complete

### 5. Review Results
- **Dashboard Tab**: Overview metrics and charts
- **Clause Details Tab**: Detailed analysis with filtering
- Review high-risk items first
- Check missing requirements
- Read recommendations

## Sample Workflow

```bash
# 1. Start the application
cd App
streamlit run app.py

# 2. In the browser:
#    - Select GDPR and HIPAA frameworks
#    - Upload a Data Processing Agreement (PDF)
#    - Click "Analyze Contract"
#    - Review dashboard metrics
#    - Filter clause details by "High" risk
#    - Read recommendations for non-compliant clauses
#    - Check missing requirements section
```

## Testing with Sample Text

If you don't have a contract file, use the Text Input method:

1. Select "Text Input" in the Contract Analysis tab
2. Paste this sample text:

```
DATA PROCESSING AGREEMENT

1. Data Processing Terms
The Processor shall process Personal Data only on documented instructions from the Controller.

2. Security Measures
The Processor shall implement appropriate technical and organizational measures to ensure
a level of security appropriate to the risk.

3. Sub-processor Authorization
The Processor shall not engage another processor without prior written authorization from
the Controller.

4. Data Subject Rights
The Processor shall assist the Controller in responding to requests for exercising the
data subject's rights.

5. Breach Notification
The Processor shall notify the Controller without undue delay after becoming aware of a
personal data breach.
```

3. Click "Process Text"
4. Click "🚀 Analyze Contract"
5. Review results

## Common Issues

### Issue: Models downloading on first run
**Solution:** This is normal. First run downloads ~440MB of models. Subsequent runs are instant.

### Issue: Analysis button disabled
**Solution:** 
1. Ensure a document is uploaded
2. Ensure at least one framework is selected

### Issue: Low compliance score
**Solution:** This is expected for incomplete contracts. Review missing requirements and recommendations.

### Issue: Application won't start
**Solution:**
```bash
# Check Python version (3.8+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Run setup test
python test_setup.py
```

## Performance Tips

1. **First Run**: Allow 5-10 minutes for model downloads
2. **Subsequent Runs**: Application starts in seconds
3. **Large Documents**: May take 10-20 seconds to analyze
4. **Multiple Frameworks**: More frameworks = longer analysis time

## Getting Help

1. Check `STREAMLIT_APP_USAGE_GUIDE.md` for detailed instructions
2. Review `TASK_7_IMPLEMENTATION_SUMMARY.md` for technical details
3. Check console logs for error messages
4. Run `python test_streamlit_integration.py` to verify setup

## What's Next?

After successfully running the application:
1. Try analyzing your own contracts
2. Experiment with different framework combinations
3. Review the detailed clause analysis
4. Export functionality coming soon (Task 8)

## Support

For issues or questions:
- Check the logs in the console
- Review error messages in the UI
- Consult the usage guide
- Run integration tests

---

**Ready to start? Run:** `streamlit run app.py`
