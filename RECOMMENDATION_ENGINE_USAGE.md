# Recommendation Engine Usage Guide

## Quick Start

### Basic Usage

```python
from services.recommendation_engine import RecommendationEngine
from services.compliance_checker import ComplianceChecker

# Initialize services
compliance_checker = ComplianceChecker()
recommendation_engine = RecommendationEngine()

# Analyze contract
compliance_report = compliance_checker.check_compliance(
    clauses=analyzed_clauses,
    frameworks=["GDPR", "HIPAA"],
    document_id="contract_001"
)

# Generate recommendations
recommendations = recommendation_engine.generate_recommendations(
    compliance_report
)

# Display recommendations
for rec in recommendations:
    print(f"Priority: {rec.get_priority_label()}")
    print(f"Action: {rec.action_type.value}")
    print(f"Description: {rec.description}")
    print(f"Reference: {rec.regulatory_reference}")
    print("---")
```

## Advanced Usage

### Generate Clause Text for Recommendations

```python
# Generate clause text for a specific recommendation
clause_text = recommendation_engine.generate_clause_for_recommendation(
    recommendation=recommendations[0],
    contract_context="Data Processing Agreement between Company A and Company B",
    existing_clauses=existing_clause_list
)

print(f"Generated Clause:\n{clause_text}")
```

### Generate All Missing Clauses

```python
# Generate clauses for all missing requirements
missing_clauses = recommendation_engine.generate_all_missing_clauses(
    missing_requirements=compliance_report.missing_requirements,
    contract_context="Data Processing Agreement"
)

for req_id, clause_text in missing_clauses.items():
    print(f"Requirement: {req_id}")
    print(f"Clause: {clause_text}\n")
```

### Generate Comprehensive Report

```python
# Generate complete report with recommendations and clause text
comprehensive_report = recommendation_engine.generate_comprehensive_report(
    compliance_report=compliance_report,
    contract_context="DPA between Company A and Company B"
)

print(f"Total Recommendations: {len(comprehensive_report['recommendations'])}")
print(f"High Priority: {comprehensive_report['high_priority_count']}")
print(f"Medium Priority: {comprehensive_report['medium_priority_count']}")
print(f"Low Priority: {comprehensive_report['low_priority_count']}")
```

## Configuration

### Using Without LLaMA (Fallback Mode)

```python
# Initialize without LLaMA for faster startup
engine = RecommendationEngine(use_llama=False)

# Will use rule-based generation
recommendations = engine.generate_recommendations(compliance_report)
```

### Custom LLaMA Model

```python
from services.legal_llama import LegalLLaMA

# Initialize custom LLaMA model
llama = LegalLLaMA(
    model_name="meta-llama/Llama-2-7b-chat-hf",  # Smaller model
    use_gpu=True,
    max_tokens=256,
    temperature=0.6
)

# Use with recommendation engine
engine = RecommendationEngine(llama_model=llama)
```

### Adjust Timeout

```python
from config.settings import config

# Increase timeout for slower systems
config.llm.generation_timeout = 120  # 2 minutes

engine = RecommendationEngine()
```

## Streamlit Integration

### With Caching

```python
import streamlit as st

@st.cache_resource
def load_recommendation_engine():
    """Load and cache recommendation engine."""
    return RecommendationEngine()

# Use cached engine
engine = load_recommendation_engine()

# Generate recommendations
if st.button("Generate Recommendations"):
    with st.spinner("Generating recommendations..."):
        recommendations = engine.generate_recommendations(compliance_report)
    
    st.success(f"Generated {len(recommendations)} recommendations")
    
    # Display recommendations
    for rec in recommendations:
        with st.expander(f"{rec.get_priority_label()}: {rec.action_type.value}"):
            st.write(f"**Description:** {rec.description}")
            st.write(f"**Rationale:** {rec.rationale}")
            st.write(f"**Reference:** {rec.regulatory_reference}")
            
            if rec.suggested_text:
                st.code(rec.suggested_text, language="text")
```

### With Progress Indicators

```python
import streamlit as st

# Generate recommendations with progress
progress_bar = st.progress(0)
status_text = st.empty()

status_text.text("Analyzing compliance gaps...")
progress_bar.progress(25)

recommendations = engine.generate_recommendations(compliance_report)

status_text.text("Generating clause text...")
progress_bar.progress(50)

for i, rec in enumerate(recommendations[:5]):  # Top 5
    if rec.action_type.value == "Add Clause":
        clause_text = engine.generate_clause_for_recommendation(rec)
        rec.suggested_text = clause_text
    
    progress_bar.progress(50 + (i + 1) * 10)

status_text.text("Complete!")
progress_bar.progress(100)
```

## Error Handling

### Handling Timeouts

```python
try:
    recommendations = engine.generate_recommendations(compliance_report)
except Exception as e:
    print(f"Error: {e}")
    # Engine automatically falls back to rule-based generation
    # Check statistics for timeout information
    stats = engine.get_statistics()
    if stats['timeouts'] > 0:
        print("Warning: Some operations timed out, using fallback generation")
```

### Checking Statistics

```python
# Get engine statistics
stats = engine.get_statistics()

print(f"Recommendations Generated: {stats['recommendations_generated']}")
print(f"Clauses Generated: {stats['clauses_generated']}")
print(f"Errors: {stats['errors']}")
print(f"Timeouts: {stats['timeouts']}")

# Reset statistics
engine.reset_statistics()
```

### Validating Configuration

```python
# Validate engine configuration
validation = engine.validate_configuration()

if not validation['valid']:
    print("Configuration issues:")
    for issue in validation['issues']:
        print(f"  - {issue}")

if validation['warnings']:
    print("Configuration warnings:")
    for warning in validation['warnings']:
        print(f"  - {warning}")
```

## Memory Management

### Clear Caches

```python
# Clear caches to free memory
engine.clear_cache()

# Also clear compliance checker cache if needed
compliance_checker.clear_cache()
```

### Monitor Memory Usage

```python
import psutil
import os

def get_memory_usage():
    """Get current memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

print(f"Memory before: {get_memory_usage():.2f} MB")

# Generate recommendations
recommendations = engine.generate_recommendations(compliance_report)

print(f"Memory after: {get_memory_usage():.2f} MB")

# Clear cache
engine.clear_cache()

print(f"Memory after clearing: {get_memory_usage():.2f} MB")
```

## Best Practices

### 1. Use Lazy Loading

```python
# Don't initialize LLaMA until needed
engine = RecommendationEngine()  # LLaMA not loaded yet

# LLaMA loads on first use
recommendations = engine.generate_recommendations(compliance_report)
```

### 2. Batch Operations

```python
# More efficient than individual calls
missing_clauses = engine.generate_all_missing_clauses(
    missing_requirements=compliance_report.missing_requirements
)

# Instead of:
# for req in missing_requirements:
#     clause = engine.generate_clause_for_recommendation(...)
```

### 3. Provide Context

```python
# Better results with context
clause_text = engine.generate_clause_for_recommendation(
    recommendation=rec,
    contract_context="Data Processing Agreement between Company A (Controller) and Company B (Processor)",
    existing_clauses=existing_clauses  # For style matching
)
```

### 4. Handle Priorities

```python
# Focus on high-priority recommendations first
high_priority = [r for r in recommendations if r.priority <= 2]

for rec in high_priority:
    # Generate clause text only for high priority
    if rec.action_type.value in ["Add Clause", "Modify Clause"]:
        clause_text = engine.generate_clause_for_recommendation(rec)
        rec.suggested_text = clause_text
```

### 5. Monitor Performance

```python
import time

start_time = time.time()

recommendations = engine.generate_recommendations(compliance_report)

elapsed = time.time() - start_time
print(f"Generation took {elapsed:.2f} seconds")

# Check if performance is acceptable
if elapsed > 10:
    print("Warning: Generation is slow, consider:")
    print("  - Using smaller LLaMA model")
    print("  - Increasing timeout")
    print("  - Using fallback mode")
```

## Troubleshooting

### LLaMA Model Not Loading

```python
# Check if model is available
try:
    from services.legal_llama import LegalLLaMA
    llama = LegalLLaMA()
    print("LLaMA loaded successfully")
except Exception as e:
    print(f"LLaMA loading failed: {e}")
    print("Using fallback mode")
    engine = RecommendationEngine(use_llama=False)
```

### GPU Not Detected

```python
import torch

print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA device count: {torch.cuda.device_count()}")

if torch.cuda.is_available():
    print(f"CUDA device: {torch.cuda.get_device_name(0)}")
else:
    print("Using CPU (slower but works)")
```

### Generation Quality Issues

```python
# Adjust temperature for more focused output
from services.legal_llama import LegalLLaMA

llama = LegalLLaMA(
    temperature=0.3,  # Lower = more focused
    max_tokens=512    # More tokens = more detailed
)

engine = RecommendationEngine(llama_model=llama)
```

## API Reference

### RecommendationEngine

#### Methods

- `generate_recommendations(compliance_report)` - Generate all recommendations
- `generate_clause_for_recommendation(recommendation, context, existing_clauses)` - Generate clause text
- `generate_all_missing_clauses(missing_requirements, context)` - Generate all missing clauses
- `generate_modification_for_clause(clause, requirement, issues)` - Generate modification
- `generate_comprehensive_report(compliance_report, context)` - Generate complete report
- `get_statistics()` - Get engine statistics
- `reset_statistics()` - Reset statistics
- `clear_cache()` - Clear caches
- `validate_configuration()` - Validate configuration

### Recommendation Model

#### Fields

- `recommendation_id` - Unique identifier
- `clause_id` - Associated clause ID (None for new)
- `requirement` - RegulatoryRequirement object
- `priority` - 1-5 (1 = highest)
- `action_type` - ActionType enum
- `description` - Recommendation description
- `suggested_text` - Generated clause text
- `rationale` - Explanation
- `regulatory_reference` - Article/section reference
- `confidence` - Confidence score (0-1)

#### Methods

- `to_dict()` - Convert to dictionary
- `get_priority_label()` - Get priority label (Critical, High, Medium, Low, Optional)

### ActionType Enum

- `ADD_CLAUSE` - Add new clause
- `MODIFY_CLAUSE` - Modify existing clause
- `REMOVE_CLAUSE` - Remove clause
- `CLARIFY_CLAUSE` - Clarify ambiguous clause

## Examples

See `test_recommendation_engine.py` for comprehensive examples of all functionality.
