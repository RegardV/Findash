"""
Minimal Base Tool Implementation
Lightweight replacement for SuperAGI base tools
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseTool(ABC):
    """Minimal base tool for financial analysis"""

    def __init__(self, **kwargs):
        """Initialize base tool"""
        self.name = self.__class__.__name__
        self.description = getattr(self.__class__, '__doc__', 'Financial analysis tool')

    @abstractmethod
    def _execute(self, **kwargs) -> str:
        """Execute the tool"""
        pass

    def execute(self, **kwargs) -> str:
        """Public execute method with error handling"""
        try:
            return self._execute(**kwargs)
        except Exception as e:
            error_msg = f"Error in {self.name}: {str(e)}"
            logger.error(error_msg)
            return error_msg

class ToolInput:
    """Base input schema for tools"""

    def __init__(self, **kwargs):
        """Initialize tool input"""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')
        }