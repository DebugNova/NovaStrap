"""
JsonValidator - Validates JSON content for FFlag configuration
"""
import json
from typing import Dict, Any, Tuple


class JsonValidator:
    """Validates JSON content for FFlag files."""
    
    MAX_SIZE = 1_000_000  # 1 MB
    
    @staticmethod
    def validate(text: str) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate JSON text.
        
        Args:
            text: JSON text to validate
        
        Returns:
            Tuple of (is_valid, error_message, parsed_data)
            - is_valid: True if valid, False otherwise
            - error_message: Empty string if valid, error message otherwise
            - parsed_data: Parsed JSON dict if valid, empty dict otherwise
        """
        # Check if empty
        if not text or not text.strip():
            return False, "JSON content is empty", {}
        
        # Check size
        if len(text) > JsonValidator.MAX_SIZE:
            return False, f"JSON too large (max {JsonValidator.MAX_SIZE} bytes)", {}
        
        # Parse JSON
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON: {e.msg} at line {e.lineno}, column {e.colno}"
            return False, error_msg, {}
        except Exception as e:
            return False, f"Invalid JSON: {str(e)}", {}
        
        # Check that it's an object (dict)
        if not isinstance(data, dict):
            return False, "Top-level JSON must be an object ({})", {}
        
        return True, "", data
    
    @staticmethod
    def format_json(text: str) -> str:
        """
        Format/prettify JSON text.
        
        Args:
            text: JSON text to format
        
        Returns:
            Formatted JSON text, or original text if parsing fails
        """
        try:
            data = json.loads(text)
            return json.dumps(data, indent=2, ensure_ascii=False)
        except Exception:
            return text

