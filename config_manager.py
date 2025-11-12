"""
⚙️ Configuration Management for Personal In and Out Dashboard
Handles application settings, preferences, and configuration persistence
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union
from datetime import datetime, date

class ConfigManager:
    """Manages application configuration and settings"""

    def __init__(self, config_file: str = None):
        """Initialize configuration manager"""
        if config_file is None:
            # Default to config file in user's home directory
            home_dir = Path.home()
            config_dir = home_dir / ".config" / "financial-dashboard"
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / "config.json"

        self.config_file = Path(config_file)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file: {e}")
                return self._get_default_config()
        else:
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "app": {
                "name": "Personal In and Out Dashboard",
                "version": "1.0.0",
                "first_run": True,
                "last_run": None
            },
            "currency": {
                "default": "ZAR",
                "format": "symbol",  # symbol, code, both
                "decimal_places": 2
            },
            "display": {
                "theme": "default",
                "date_format": "short",  # short, long, time
                "table_style": "default",
                "progress_bar_width": 50
            },
            "data": {
                "workspace_path": None,  # Will be set dynamically
                "auto_backup": True,
                "backup_interval_days": 7,
                "max_backups": 10
            },
            "import": {
                "default_chunk_size": 1000,
                "auto_categorize": True,
                "duplicate_detection": True,
                "csv_delimiter": ",",
                "csv_encoding": "utf-8"
            },
            "budget": {
                "warning_threshold": 0.8,  # 80%
                "critical_threshold": 1.0,  # 100%
                "monthly_reset": True
            },
            "tax": {
                "default_year": str(date.today().year),
                "individual_brackets": {
                    "1": {"min": 0, "max": 237100, "rate": 0.18},
                    "2": {"min": 237101, "max": 370500, "rate": 0.26},
                    "3": {"min": 370501, "max": 512800, "rate": 0.31},
                    "4": {"min": 512801, "max": 673000, "rate": 0.36},
                    "5": {"min": 673001, "max": 857900, "rate": 0.39},
                    "6": {"min": 857901, "max": 1817000, "rate": 0.41},
                    "7": {"min": 1817001, "max": float("inf"), "rate": 0.45}
                },
                "company_rate": 0.28,
                "small_business_rates": {
                    "turnover_bracket_1": {"max": 335000, "rate": 0.0},
                    "turnover_bracket_2": {"max": 585000, "rate": 0.15},
                    "turnover_bracket_3": {"max": 785000, "rate": 0.21},
                    "turnover_bracket_4": {"max": float("inf"), "rate": 0.28}
                }
            },
            "entities": {
                "default_entities": [
                    {"name": "Dad", "type": "person", "description": "Father's expenses"},
                    {"name": "Mom", "type": "person", "description": "Mother's expenses"},
                    {"name": "Household", "type": "household", "description": "Shared household expenses"},
                    {"name": "Business", "type": "business", "description": "Business expenses (TA-REALW)"},
                    {"name": "Emergency", "type": "savings", "description": "Emergency fund"}
                ]
            },
            "categories": {
                "default_categories": [
                    {"name": "Groceries", "description": "Food and household items"},
                    {"name": "Transportation", "description": "Fuel, public transport, vehicle maintenance"},
                    {"name": "Motors", "description": "Vehicle expenses and maintenance"},
                    {"name": "Data/Communication", "description": "Internet, phone bills"},
                    {"name": "Home", "description": "Rent/mortgage, utilities, home maintenance"},
                    {"name": "Healthcare", "description": "Medical expenses, insurance"},
                    {"name": "Education", "description": "School fees, books, courses"},
                    {"name": "Entertainment", "description": "Movies, dining out, hobbies"},
                    {"name": "Shopping", "description": "Clothing, electronics, personal items"},
                    {"name": "Savings", "description": "Savings accounts, investments"},
                    {"name": "Business", "description": "Business-related expenses"},
                    {"name": "Other", "description": "Miscellaneous expenses"}
                ]
            }
        }

    def save_config(self):
        """Save configuration to file"""
        try:
            # Ensure directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)

            # Add last run timestamp
            self.config["app"]["last_run"] = datetime.now().isoformat()

            # Save to file
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)

            return True
        except IOError as e:
            print(f"Error saving config: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'currency.default')"""
        keys = key.split('.')
        value = self.config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any):
        """Set configuration value using dot notation"""
        keys = key.split('.')
        config = self.config

        # Navigate to parent of target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        # Set the value
        config[keys[-1]] = value

    def get_all(self) -> Dict[str, Any]:
        """Get entire configuration dictionary"""
        return self.config.copy()

    def update(self, updates: Dict[str, Any]):
        """Update multiple configuration values"""
        for key, value in updates.items():
            self.set(key, value)

    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = self._get_default_config()
        self.save_config()

    def export_config(self, file_path: str):
        """Export configuration to specified file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error exporting config: {e}")
            return False

    def import_config(self, file_path: str, merge: bool = True):
        """Import configuration from specified file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)

            if merge:
                # Merge with existing config
                self._deep_merge(self.config, imported_config)
            else:
                # Replace entire config
                self.config = imported_config

            self.save_config()
            return True
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error importing config: {e}")
            return False

    def _deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]):
        """Deep merge two dictionaries"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def validate_config(self) -> bool:
        """Validate configuration structure and values"""
        try:
            # Check required top-level keys
            required_keys = ['app', 'currency', 'display', 'data', 'import', 'budget', 'tax', 'entities', 'categories']
            for key in required_keys:
                if key not in self.config:
                    print(f"Missing required configuration section: {key}")
                    return False

            # Validate currency settings
            if not self.get('currency.default'):
                print("Default currency not specified")
                return False

            # Validate tax brackets structure
            tax_brackets = self.get('tax.individual_brackets', {})
            for bracket, data in tax_brackets.items():
                if not all(k in data for k in ['min', 'max', 'rate']):
                    print(f"Invalid tax bracket structure for bracket {bracket}")
                    return False

            return True
        except Exception as e:
            print(f"Configuration validation error: {e}")
            return False

    def get_workspace_path(self) -> Optional[Path]:
        """Get the workspace path, create if needed"""
        workspace_path = self.get('data.workspace_path')
        if workspace_path:
            return Path(workspace_path)
        return None

    def set_workspace_path(self, path: Union[str, Path]):
        """Set the workspace path"""
        self.set('data.workspace_path', str(Path(path)))
        self.save_config()

    def is_first_run(self) -> bool:
        """Check if this is the first time running the application"""
        return self.get('app.first_run', True)

    def mark_first_run_complete(self):
        """Mark first run as complete"""
        self.set('app.first_run', False)
        self.save_config()

    def get_currency_info(self, currency_code: str = None) -> Dict[str, Any]:
        """Get currency information"""
        if currency_code is None:
            currency_code = self.get('currency.default', 'ZAR')

        # Basic currency info (could be expanded)
        currency_info = {
            "ZAR": {"name": "South African Rand", "symbol": "R", "code": "ZAR"},
            "USD": {"name": "US Dollar", "symbol": "$", "code": "USD"},
            "EUR": {"name": "Euro", "symbol": "€", "code": "EUR"},
            "GBP": {"name": "British Pound", "symbol": "£", "code": "GBP"},
            "JPY": {"name": "Japanese Yen", "symbol": "¥", "code": "JPY"},
            "CNY": {"name": "Chinese Yuan", "symbol": "¥", "code": "CNY"}
        }

        return currency_info.get(currency_code, {
            "name": currency_code,
            "symbol": currency_code,
            "code": currency_code
        })

    def get_tax_info(self) -> Dict[str, Any]:
        """Get tax configuration information"""
        return self.get('tax', {})

    def get_entities(self) -> list:
        """Get default entities"""
        return self.get('entities.default_entities', [])

    def get_categories(self) -> list:
        """Get default categories"""
        return self.get('categories.default_categories', [])

    def __str__(self) -> str:
        """String representation of config manager"""
        return f"ConfigManager(file={self.config_file})"

    def __repr__(self) -> str:
        """Detailed string representation"""
        return f"ConfigManager(file='{self.config_file}', sections={list(self.config.keys())})"