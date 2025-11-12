"""
💱 Currency Manager - Standalone Version
Handles multiple currency support with focus on South African Rand (R)
Provides currency conversion, formatting, and exchange rate management
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from pathlib import Path

# Import standalone base tool
from tools.base_tool import BaseTool


class CurrencyConfig:
    """Currency configuration model"""
    def __init__(self, code: str, symbol: str, name: str, exchange_rate: float = 1.0,
                 is_default: bool = False, decimal_places: int = 2):
        self.code = code.upper()
        self.symbol = symbol
        self.name = name
        self.exchange_rate = float(exchange_rate)
        self.is_default = bool(is_default)
        self.decimal_places = int(decimal_places)

    def dict(self):
        """Convert to dictionary"""
        return {
            'code': self.code,
            'symbol': self.symbol,
            'name': self.name,
            'exchange_rate': self.exchange_rate,
            'is_default': self.is_default,
            'decimal_places': self.decimal_places
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create from dictionary"""
        return cls(**data)


class CurrencyManager(BaseTool):
    """
    Currency Manager - Multi-currency support with South African Rand focus

    Features:
    - Currency conversion and exchange rate management
    - Multiple currency display and reporting
    - Exchange rate tracking and updates
    - Default currency configuration
    - South African Rand (R) native support
    - Real-time exchange rate simulation
    """

    def __init__(self, workspace_path: str = None):
        """Initialize currency manager"""
        super().__init__()

        # Set currency config file path
        if workspace_path:
            self.currencies_file = Path(workspace_path) / "currencies_config.json"
        else:
            self.currencies_file = Path("currencies_config.json")

        # Load currencies database
        self.currencies_db = self._load_currencies_database()

    def _load_currencies_database(self) -> Dict[str, Any]:
        """Load currencies database from file"""
        try:
            if self.currencies_file.exists():
                with open(self.currencies_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Validate and upgrade if needed
                    return self._validate_and_upgrade_currencies(data)
            else:
                return self._get_default_currencies()
        except Exception as e:
            print(f"Warning: Could not load currencies database: {e}")
            return self._get_default_currencies()

    def _validate_and_upgrade_currencies(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and upgrade currencies database"""
        # Ensure required structure
        if "default_currency" not in data:
            data["default_currency"] = "ZAR"

        if "currencies" not in data:
            data["currencies"] = {}

        # Add last_updated timestamp
        if "last_updated" not in data:
            data["last_updated"] = datetime.now().isoformat()

        # Ensure ZAR exists and is properly configured
        if "ZAR" not in data["currencies"]:
            data["currencies"]["ZAR"] = {
                "code": "ZAR",
                "symbol": "R",
                "name": "South African Rand",
                "exchange_rate": 1.0,
                "is_default": True,
                "decimal_places": 2
            }

        return data

    def _get_default_currencies(self) -> Dict[str, Any]:
        """Get default South African focused currency configuration"""
        return {
            "version": "1.0",
            "default_currency": "ZAR",
            "last_updated": datetime.now().isoformat(),
            "base_currency": "ZAR",
            "currencies": {
                "ZAR": {
                    "code": "ZAR",
                    "symbol": "R",
                    "name": "South African Rand",
                    "exchange_rate": 1.0,
                    "is_default": True,
                    "decimal_places": 2
                },
                "USD": {
                    "code": "USD",
                    "symbol": "$",
                    "name": "US Dollar",
                    "exchange_rate": 18.50,  # 1 USD = 18.50 ZAR
                    "is_default": False,
                    "decimal_places": 2
                },
                "EUR": {
                    "code": "EUR",
                    "symbol": "€",
                    "name": "Euro",
                    "exchange_rate": 20.25,  # 1 EUR = 20.25 ZAR
                    "is_default": False,
                    "decimal_places": 2
                },
                "GBP": {
                    "code": "GBP",
                    "symbol": "£",
                    "name": "British Pound",
                    "exchange_rate": 23.75,  # 1 GBP = 23.75 ZAR
                    "is_default": False,
                    "decimal_places": 2
                },
                "JPY": {
                    "code": "JPY",
                    "symbol": "¥",
                    "name": "Japanese Yen",
                    "exchange_rate": 0.124,  # 1 JPY = 0.124 ZAR
                    "is_default": False,
                    "decimal_places": 0
                },
                "CNY": {
                    "code": "CNY",
                    "symbol": "¥",
                    "name": "Chinese Yuan",
                    "exchange_rate": 2.55,  # 1 CNY = 2.55 ZAR
                    "is_default": False,
                    "decimal_places": 2
                }
            }
        }

    def _save_currencies_database(self) -> bool:
        """Save currencies database to file"""
        try:
            # Ensure directory exists
            self.currencies_file.parent.mkdir(parents=True, exist_ok=True)

            # Update timestamp
            self.currencies_db["last_updated"] = datetime.now().isoformat()

            with open(self.currencies_file, 'w', encoding='utf-8') as f:
                json.dump(self.currencies_db, f, indent=2, ensure_ascii=False)

            print(f"💾 Currencies database saved to {self.currencies_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving currencies database: {e}")
            return False

    def get_default_currency(self) -> Dict[str, Any]:
        """Get default currency configuration"""
        default_code = self.currencies_db.get("default_currency", "ZAR")
        return self.currencies_db["currencies"].get(default_code, self.currencies_db["currencies"]["ZAR"])

    def set_default_currency(self, currency_code: str) -> bool:
        """Set default currency for the system"""
        currency_code = currency_code.strip().upper()

        # Validate currency exists
        if currency_code not in self.currencies_db["currencies"]:
            print(f"❌ Currency '{currency_code}' not found in system")
            return False

        # Update default currency
        # Reset all currencies to non-default first
        for code in self.currencies_db["currencies"]:
            self.currencies_db["currencies"][code]["is_default"] = False

        # Set new default
        self.currencies_db["currencies"][currency_code]["is_default"] = True
        self.currencies_db["default_currency"] = currency_code

        # Save changes
        if self._save_currencies_database():
            currency_info = self.currencies_db["currencies"][currency_code]
            print(f"✅ Default currency set to {currency_info['name']} ({currency_info['symbol']})")
            return True

        return False

    def list_currencies(self) -> List[Dict[str, Any]]:
        """Get list of available currencies"""
        currencies = []
        for currency_code, currency_info in self.currencies_db["currencies"].items():
            currencies.append({
                'code': currency_code,
                'symbol': currency_info['symbol'],
                'name': currency_info['name'],
                'exchange_rate': currency_info['exchange_rate'],
                'is_default': currency_info['is_default'],
                'decimal_places': currency_info['decimal_places']
            })

        # Sort by default currency first, then by code
        currencies.sort(key=lambda x: (not x['is_default'], x['code']))
        return currencies

    def convert_amount(self, amount: float, from_currency: str, to_currency: str = None) -> Tuple[float, str, str]:
        """
        Convert amount between currencies
        Returns: (converted_amount, from_symbol, to_symbol)
        """
        if to_currency is None:
            to_currency = self.currencies_db.get("default_currency", "ZAR")

        from_currency = from_currency.strip().upper()
        to_currency = to_currency.strip().upper()

        # Validate currencies
        if from_currency not in self.currencies_db["currencies"]:
            raise ValueError(f"Source currency '{from_currency}' not found")

        if to_currency not in self.currencies_db["currencies"]:
            raise ValueError(f"Target currency '{to_currency}' not found")

        # If same currency, no conversion needed
        if from_currency == to_currency:
            currency_info = self.currencies_db["currencies"][from_currency]
            return amount, currency_info['symbol'], currency_info['symbol']

        # Get exchange rates (relative to base currency ZAR)
        from_rate = self.currencies_db["currencies"][from_currency]["exchange_rate"]
        to_rate = self.currencies_db["currencies"][to_currency]["exchange_rate"]

        # Convert through base currency (ZAR)
        # Convert from_currency to ZAR, then to to_currency
        zar_amount = amount / from_rate
        converted_amount = zar_amount * to_rate

        from_symbol = self.currencies_db["currencies"][from_currency]["symbol"]
        to_symbol = self.currencies_db["currencies"][to_currency]["symbol"]

        return converted_amount, from_symbol, to_symbol

    def update_exchange_rate(self, currency_code: str, exchange_rate: float) -> bool:
        """Update exchange rate for a currency"""
        currency_code = currency_code.strip().upper()

        if currency_code == "ZAR":
            print("❌ Cannot update exchange rate for base currency ZAR (always 1.0)")
            return False

        if currency_code not in self.currencies_db["currencies"]:
            print(f"❌ Currency '{currency_code}' not found in system")
            return False

        old_rate = self.currencies_db["currencies"][currency_code]["exchange_rate"]
        self.currencies_db["currencies"][currency_code]["exchange_rate"] = float(exchange_rate)

        if self._save_currencies_database():
            currency_info = self.currencies_db["currencies"][currency_code]
            print(f"✅ Updated {currency_info['name']} exchange rate: {old_rate} → {exchange_rate}")
            return True

        return False

    def add_currency(self, currency_code: str, symbol: str, name: str, exchange_rate: float = 1.0,
                    decimal_places: int = 2) -> bool:
        """Add a new currency to the system"""
        currency_code = currency_code.strip().upper()

        if currency_code in self.currencies_db["currencies"]:
            print(f"⚠️ Currency '{currency_code}' already exists. Use update_exchange_rate instead.")
            return False

        # Create new currency
        self.currencies_db["currencies"][currency_code] = CurrencyConfig(
            code=currency_code,
            symbol=symbol,
            name=name,
            exchange_rate=exchange_rate,
            is_default=False,
            decimal_places=decimal_places
        ).dict()

        if self._save_currencies_database():
            print(f"✅ Added new currency: {name} ({symbol})")
            return True

        return False

    def format_currency(self, amount: float, currency_code: str = None, show_symbol: bool = True) -> str:
        """Format amount with currency symbol"""
        if currency_code is None:
            currency_code = self.currencies_db.get("default_currency", "ZAR")

        currency_code = currency_code.strip().upper()
        currency_info = self.currencies_db["currencies"].get(currency_code)

        if not currency_info:
            # Fallback to simple formatting
            return f"{amount:,.2f}"

        symbol = currency_info["symbol"] if show_symbol else ""
        decimals = currency_info.get("decimal_places", 2)

        # Use Decimal for precise rounding
        decimal_amount = Decimal(str(amount)).quantize(Decimal(f"0.{ '0' * decimals }"), rounding=ROUND_HALF_UP)

        # Format with thousand separators
        formatted_amount = f"{decimal_amount:,.{decimals}f}"

        return f"{symbol}{formatted_amount}"

    def format_amounts_list(self, amounts: List[float], currency_code: str = None) -> List[str]:
        """Format a list of amounts with currency symbol"""
        return [self.format_currency(amount, currency_code, True) for amount in amounts]

    def create_currency_formatter(self, currency_code: str = None):
        """Create a currency formatting function"""
        if currency_code is None:
            currency_code = self.currencies_db.get("default_currency", "ZAR")

        def formatter(amount: float) -> str:
            return self.format_currency(amount, currency_code, True)

        formatter.currency_code = currency_code
        return formatter

    def convert_and_format_list(self, amounts: List[float], from_currency: str, to_currency: str = None) -> List[str]:
        """Convert amounts list and format with target currency"""
        if to_currency is None:
            to_currency = self.currencies_db.get("default_currency", "ZAR")

        converted_amounts = []
        for amount in amounts:
            converted_amount, _, _ = self.convert_amount(amount, from_currency, to_currency)
            converted_amounts.append(converted_amount)

        return self.format_amounts_list(converted_amounts, to_currency)

    def convert_single_and_format(self, amount: float, from_currency: str, to_currency: str = None) -> str:
        """Convert single amount and format with currency symbol"""
        converted_amount, _, to_symbol = self.convert_amount(amount, from_currency, to_currency)
        if to_currency is None:
            to_currency = self.currencies_db.get("default_currency", "ZAR")
        return self.format_currency(converted_amount, to_currency, True)

    def get_exchange_rate(self, from_currency: str, to_currency: str) -> Optional[float]:
        """Get exchange rate between two currencies"""
        from_currency = from_currency.strip().upper()
        to_currency = to_currency.strip().upper()

        if from_currency not in self.currencies_db["currencies"]:
            return None

        if to_currency not in self.currencies_db["currencies"]:
            return None

        if from_currency == to_currency:
            return 1.0

        # Get rates relative to base currency (ZAR)
        from_rate = self.currencies_db["currencies"][from_currency]["exchange_rate"]
        to_rate = self.currencies_db["currencies"][to_currency]["exchange_rate"]

        # Calculate rate through base currency
        return to_rate / from_rate

    def simulate_exchange_rate_update(self, currency_code: str, volatility: float = 0.02) -> Optional[float]:
        """
        Simulate exchange rate update (for demonstration)
        volatility: percentage change (default 2%)
        """
        currency_code = currency_code.strip().upper()

        if currency_code == "ZAR":
            return None  # Base currency doesn't change

        if currency_code not in self.currencies_db["currencies"]:
            return None

        current_rate = self.currencies_db["currencies"][currency_code]["exchange_rate"]

        # Simulate random change within volatility range
        import random
        change_percent = random.uniform(-volatility, volatility)
        new_rate = current_rate * (1 + change_percent)

        # Ensure rate doesn't go negative
        new_rate = max(0.01, new_rate)

        self.update_exchange_rate(currency_code, new_rate)
        return new_rate

    def get_currency_summary(self) -> Dict[str, Any]:
        """Get summary of all currencies"""
        currencies = self.list_currencies()
        default_currency = self.get_default_currency()

        summary = {
            "total_currencies": len(currencies),
            "default_currency": default_currency,
            "last_updated": self.currencies_db.get("last_updated"),
            "currencies": []
        }

        for currency in currencies:
            summary["currencies"].append({
                "code": currency["code"],
                "symbol": currency["symbol"],
                "name": currency["name"],
                "exchange_rate": currency["exchange_rate"],
                "is_default": currency["is_default"]
            })

        return summary

    def _execute(self, **kwargs) -> str:
        """Execute tool operation (required by BaseTool)"""
        operation = kwargs.get("operation", "summary")

        try:
            if operation == "summary":
                summary = self.get_currency_summary()
                return f"Currency Summary: {json.dumps(summary, indent=2)}"
            elif operation == "convert":
                amount = kwargs.get("amount", 0)
                from_currency = kwargs.get("from_currency", "ZAR")
                to_currency = kwargs.get("to_currency", None)

                if not amount:
                    return "❌ Amount is required for conversion"

                converted_amount, from_symbol, to_symbol = self.convert_amount(
                    float(amount), from_currency, to_currency
                )
                return f"💱 {amount} {from_symbol} = {converted_amount:,.2f} {to_symbol}"
            else:
                return f"Unknown operation: {operation}"

        except Exception as e:
            return f"❌ Error: {str(e)}"


# Utility functions for easy access
def get_currency_manager(workspace_path: str = None) -> CurrencyManager:
    """Get currency manager instance"""
    return CurrencyManager(workspace_path)


def format_zar(amount: float) -> str:
    """Quick ZAR formatting function"""
    manager = CurrencyManager()
    return manager.format_currency(amount, "ZAR")


def convert_to_zar(amount: float, from_currency: str) -> str:
    """Quick convert to ZAR"""
    manager = CurrencyManager()
    return manager.convert_single_and_format(amount, from_currency, "ZAR")


if __name__ == "__main__":
    # Example usage
    manager = CurrencyManager()

    print("=== Personal In and Out Dashboard - Currency Manager ===")
    print(f"Default currency: {manager.get_default_currency()['name']}")

    # Test conversions
    amount = 1000
    print(f"\n💱 Converting {amount} ZAR to other currencies:")

    for currency in ["USD", "EUR", "GBP"]:
        converted = manager.convert_single_and_format(amount, "ZAR", currency)
        print(f"  {amount} ZAR = {converted}")

    # Test formatting
    print(f"\n💰 Formatting examples:")
    print(f"  ZAR: {manager.format_currency(1234.56, 'ZAR')}")
    print(f"  USD: {manager.format_currency(1234.56, 'USD')}")
    print(f"  EUR: {manager.format_currency(1234.56, 'EUR')}")

    # List currencies
    print(f"\n📊 Available currencies:")
    for currency in manager.list_currencies():
        default_mark = "🌐" if currency['is_default'] else "  "
        print(f"  {default_mark} {currency['code']} - {currency['symbol']} {currency['name']}")