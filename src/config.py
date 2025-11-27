import os
from typing import Optional


class Config:
    
    # LangSmith Configuration
    LANGCHAIN_TRACING_V2: str = "true"
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGCHAIN_API_KEY: str = ""  # Add your key
    LANGCHAIN_PROJECT: str = "default"
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = ""  # Add your key
    
    # Model Configuration
    DEFAULT_MODEL: str = "gpt-4"
    DEFAULT_TEMPERATURE: float = 0.7
    
    # Research Configuration
    DEFAULT_NUM_SUB_QUESTIONS: int = 3
    DEFAULT_MAX_ITERATIONS: int = 2
    MIN_SUB_QUESTIONS: int = 1
    MAX_SUB_QUESTIONS: int = 10
    MIN_ITERATIONS: int = 1
    MAX_ITERATIONS: int = 5
    
    @classmethod
    def setup_environment(cls) -> None:
        """Set up environment variables for LangSmith tracing."""
        os.environ["LANGCHAIN_TRACING_V2"] = cls.LANGCHAIN_TRACING_V2
        os.environ["LANGCHAIN_ENDPOINT"] = cls.LANGCHAIN_ENDPOINT
        os.environ["LANGCHAIN_API_KEY"] = cls.LANGCHAIN_API_KEY
        os.environ["LANGCHAIN_PROJECT"] = cls.LANGCHAIN_PROJECT
    
    @classmethod
    def get_openai_api_key(cls) -> str:
        """Get OpenAI API key from config or environment."""
        return cls.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY", "")
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is set."""
        if not cls.get_openai_api_key():
            print("⚠️  Warning: OpenAI API key not configured")
            return False
        return True
