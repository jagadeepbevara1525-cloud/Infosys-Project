# AI-Powered Regulatory Compliance Checker

An intelligent system that automates contract compliance analysis across multiple regulatory frameworks (GDPR, HIPAA, CCPA, SOX).

## Project Structure

```
App/
├── config/                 # Configuration management
│   ├── __init__.py
│   └── settings.py        # Application settings and model configurations
├── models/                # Data models and schemas
│   └── __init__.py
├── services/              # Business logic services
│   └── __init__.py
├── utils/                 # Utility functions
│   ├── __init__.py
│   └── logger.py         # Logging with sensitive data sanitization
├── data/                  # Data storage (created at runtime)
├── logs/                  # Application logs (created at runtime)
├── temp/                  # Temporary files (created at runtime)
├── app.py                # Main Streamlit application
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Tesseract OCR (for image-based document processing)
- CUDA-capable GPU (optional, for faster model inference)

### Installation

1. Create a virtual environment:
```bash
python -m venv myenv
```

2. Activate the virtual environment:
- Windows: `myenv\Scripts\activate`
- Linux/Mac: `source myenv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Tesseract OCR:
- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
- Linux: `sudo apt-get install tesseract-ocr`
- Mac: `brew install tesseract`

### Configuration

Configuration can be customized via environment variables or by modifying `config/settings.py`.

Key configuration options:
- `DEBUG`: Enable debug mode (default: False)
- `LOG_LEVEL`: Logging level (default: INFO)
- `LEGAL_BERT_MODEL`: LegalBERT model path
- `LLAMA_MODEL`: LLaMA model path
- `USE_GPU`: Enable GPU acceleration (default: True)

### Running the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Features

- **Multi-format Document Processing**: PDF, DOCX, TXT, PNG, JPG
- **OCR Support**: Extract text from scanned documents
- **Clause Classification**: Automatic identification of clause types
- **Compliance Analysis**: Check against GDPR, HIPAA, CCPA, SOX
- **Risk Assessment**: Identify high, medium, and low-risk items
- **AI Recommendations**: Generate compliant clause text
- **Interactive Dashboard**: Visualize compliance metrics
- **Export Reports**: PDF, JSON, CSV formats

## Logging

The application includes comprehensive logging with automatic sanitization of sensitive data:
- Email addresses
- Phone numbers
- API keys
- Passwords
- Credit card numbers

Logs are stored in the `logs/` directory with daily rotation.

## Development

### Adding New Services

1. Create a new file in `services/` directory
2. Implement the service class
3. Import in `services/__init__.py`

### Adding New Models

1. Create a new file in `models/` directory
2. Define data classes using `@dataclass` decorator
3. Import in `models/__init__.py`

## License

Copyright © 2024 AI Compliance Checker
# Infosys-Project
