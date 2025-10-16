"""
Configuration management system for model paths and settings.
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ModelConfig:
    """Configuration for ML models."""
    legal_bert_model: str = "nlpaueb/legal-bert-base-uncased"
    llama_model: str = "meta-llama/Llama-2-13b-chat-hf"
    sentence_transformer_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    cache_dir: str = "./models_cache"
    use_gpu: bool = True
    max_length: int = 512


@dataclass
class ProcessingConfig:
    """Configuration for document processing."""
    max_file_size_mb: int = 10
    supported_formats: list = field(default_factory=lambda: ['pdf', 'docx', 'txt', 'png', 'jpg'])
    ocr_language: str = 'eng'
    confidence_threshold: float = 0.75
    processing_timeout: int = 300  # seconds


@dataclass
class ComplianceConfig:
    """Configuration for compliance checking."""
    enabled_frameworks: list = field(default_factory=lambda: ['GDPR', 'HIPAA', 'CCPA', 'SOX'])
    risk_tolerance: str = 'Medium'  # Low, Medium, High
    similarity_threshold: float = 0.75
    min_clause_length: int = 20


@dataclass
class LLMConfig:
    """Configuration for LLM generation."""
    max_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.9
    generation_timeout: int = 60  # seconds


@dataclass
class AppConfig:
    """Main application configuration."""
    app_name: str = "AI-Powered Regulatory Compliance Checker"
    version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"
    
    # Sub-configurations
    models: ModelConfig = field(default_factory=ModelConfig)
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    compliance: ComplianceConfig = field(default_factory=ComplianceConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    
    # Paths
    base_dir: Path = field(default_factory=lambda: Path(__file__).parent.parent)
    data_dir: Path = field(init=False)
    logs_dir: Path = field(init=False)
    temp_dir: Path = field(init=False)
    
    def __post_init__(self):
        """Initialize derived paths."""
        self.data_dir = self.base_dir / "data"
        self.logs_dir = self.base_dir / "logs"
        self.temp_dir = self.base_dir / "temp"
        
        # Create directories if they don't exist
        self.data_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'app_name': self.app_name,
            'version': self.version,
            'debug': self.debug,
            'log_level': self.log_level,
            'models': {
                'legal_bert_model': self.models.legal_bert_model,
                'llama_model': self.models.llama_model,
                'sentence_transformer_model': self.models.sentence_transformer_model,
                'cache_dir': self.models.cache_dir,
                'use_gpu': self.models.use_gpu,
                'max_length': self.models.max_length,
            },
            'processing': {
                'max_file_size_mb': self.processing.max_file_size_mb,
                'supported_formats': self.processing.supported_formats,
                'ocr_language': self.processing.ocr_language,
                'confidence_threshold': self.processing.confidence_threshold,
                'processing_timeout': self.processing.processing_timeout,
            },
            'compliance': {
                'enabled_frameworks': self.compliance.enabled_frameworks,
                'risk_tolerance': self.compliance.risk_tolerance,
                'similarity_threshold': self.compliance.similarity_threshold,
                'min_clause_length': self.compliance.min_clause_length,
            },
            'llm': {
                'max_tokens': self.llm.max_tokens,
                'temperature': self.llm.temperature,
                'top_p': self.llm.top_p,
                'generation_timeout': self.llm.generation_timeout,
            }
        }
    
    @classmethod
    def from_env(cls) -> 'AppConfig':
        """Load configuration from environment variables."""
        config = cls()
        
        # Override with environment variables if present
        if os.getenv('DEBUG'):
            config.debug = os.getenv('DEBUG').lower() == 'true'
        
        if os.getenv('LOG_LEVEL'):
            config.log_level = os.getenv('LOG_LEVEL')
        
        if os.getenv('LEGAL_BERT_MODEL'):
            config.models.legal_bert_model = os.getenv('LEGAL_BERT_MODEL')
        
        if os.getenv('LLAMA_MODEL'):
            config.models.llama_model = os.getenv('LLAMA_MODEL')
        
        if os.getenv('USE_GPU'):
            config.models.use_gpu = os.getenv('USE_GPU').lower() == 'true'
        
        return config


# Global configuration instance
config = AppConfig.from_env()
