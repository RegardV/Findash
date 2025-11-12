"""
📊 Master Transaction Database Manager - Standalone Version
Handles CRUD operations for categories, labels, and transaction patterns
Optimized for South African financial data
"""

import json
import os
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path

# Import standalone base tool
from tools.base_tool import BaseTool


class CategoryModel:
    """Data model for a transaction category"""
    def __init__(self, name: str, description: str = "", color: str = "#000000",
                 is_active: bool = True, **kwargs):
        self.name = name
        self.description = description
        self.color = color
        self.created_at = kwargs.get('created_at', datetime.now().isoformat())
        self.updated_at = kwargs.get('updated_at', datetime.now().isoformat())
        self.is_active = is_active

    def dict(self):
        """Convert to dictionary"""
        return {
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'is_active': self.is_active
        }


class LabelModel:
    """Data model for a transaction label within a category"""
    def __init__(self, name: str, description: str = "", patterns: List[str] = None,
                 keywords: List[str] = None, is_active: bool = True, **kwargs):
        self.name = name
        self.description = description
        self.patterns = patterns or []
        self.keywords = keywords or []
        self.created_at = kwargs.get('created_at', datetime.now().isoformat())
        self.updated_at = kwargs.get('updated_at', datetime.now().isoformat())
        self.is_active = is_active

    def dict(self):
        """Convert to dictionary"""
        return {
            'name': self.name,
            'description': self.description,
            'patterns': self.patterns,
            'keywords': self.keywords,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'is_active': self.is_active
        }


class PatternModel:
    """Data model for transaction matching patterns"""
    def __init__(self, pattern: str, confidence: float = 0.8, category: str = "",
                 label: str = "", match_count: int = 0, last_matched: str = None, **kwargs):
        self.pattern = pattern
        self.confidence = confidence
        self.category = category
        self.label = label
        self.match_count = match_count
        self.last_matched = last_matched
        self.created_at = kwargs.get('created_at', datetime.now().isoformat())

    def dict(self):
        """Convert to dictionary"""
        return {
            'pattern': self.pattern,
            'confidence': self.confidence,
            'category': self.category,
            'label': self.label,
            'match_count': self.match_count,
            'last_matched': self.last_matched,
            'created_at': self.created_at
        }


class TransactionModel:
    """Data model for a single transaction"""
    def __init__(self, date: datetime, description: str, amount: float,
                 category: str = None, label: str = None, entity: str = None,
                 currency: str = "ZAR", reference: str = None, **kwargs):
        self.date = date
        self.description = description
        self.amount = amount
        self.category = category
        self.label = label
        self.entity = entity
        self.currency = currency
        self.reference = reference
        self.created_at = kwargs.get('created_at', datetime.now().isoformat())
        self.validated_at = kwargs.get('validated_at')

    def dict(self):
        """Convert to dictionary"""
        return {
            'date': self.date.isoformat() if isinstance(self.date, datetime) else self.date,
            'description': self.description,
            'amount': self.amount,
            'category': self.category,
            'label': self.label,
            'entity': self.entity,
            'currency': self.currency,
            'reference': self.reference,
            'created_at': self.created_at,
            'validated_at': self.validated_at
        }


class MasterTransactionDB(BaseTool):
    """Master database for transaction categories, labels, and patterns"""

    def __init__(self, workspace_path: str = None):
        """Initialize the transaction database"""
        super().__init__()

        # Set database path
        if workspace_path:
            self.db_path = Path(workspace_path) / "master_transaction_db.json"
        else:
            # Use current directory
            self.db_path = Path("master_transaction_db.json")

        # Also maintain a transactions file
        self.transactions_path = self.db_path.parent / "transactions.json"

        # Initialize data
        self.data = self._load_database()
        self.transactions = self._load_transactions()

    def _load_database(self) -> Dict[str, Any]:
        """Load database from file or create default"""
        if self.db_path.exists():
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Validate and migrate if needed
                    return self._validate_and_migrate(data)
            except Exception as e:
                print(f"Warning: Could not load database: {e}")
                return self._create_default_database()
        else:
            return self._create_default_database()

    def _load_transactions(self) -> List[Dict[str, Any]]:
        """Load transactions from file or create empty list"""
        if self.transactions_path.exists():
            try:
                with open(self.transactions_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load transactions: {e}")
                return []
        else:
            return []

    def _validate_and_migrate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate database structure and migrate if needed"""
        # Ensure required sections exist
        if "version" not in data:
            data["version"] = "1.0"
            data["migrated"] = datetime.now().isoformat()

        if "categories" not in data:
            data["categories"] = {}

        if "labels" not in data:
            data["labels"] = {}

        if "patterns" not in data:
            data["patterns"] = []

        if "settings" not in data:
            data["settings"] = {
                "default_confidence_threshold": 0.7,
                "auto_learn": True,
                "require_human_review": True,
                "default_currency": "ZAR",
                "date_format": "%Y-%m-%d"
            }

        return data

    def _create_default_database(self) -> Dict[str, Any]:
        """Create default database structure for South African users"""
        return {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "created_by": "Personal In and Out Dashboard",
            "categories": {},
            "labels": {},
            "patterns": [],
            "settings": {
                "default_confidence_threshold": 0.7,
                "auto_learn": True,
                "require_human_review": True,
                "default_currency": "ZAR",
                "date_format": "%Y-%m-%d"
            }
        }

    def _save_database(self) -> bool:
        """Save database to file"""
        try:
            # Ensure directory exists
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving database: {e}")
            return False

    def _save_transactions(self) -> bool:
        """Save transactions to file"""
        try:
            # Ensure directory exists
            self.transactions_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.transactions_path, 'w', encoding='utf-8') as f:
                json.dump(self.transactions, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving transactions: {e}")
            return False

    # CATEGORY MANAGEMENT
    def create_category(self, name: str, description: str = "", color: str = "#000000") -> bool:
        """Create a new category"""
        # Normalize name
        name = name.strip().lower()

        if name in [cat.lower() for cat in self.data["categories"].keys()]:
            print(f"Category '{name}' already exists")
            return False

        category = CategoryModel(name=name, description=description, color=color)
        self.data["categories"][name] = category.dict()
        self.data["labels"][name] = {}  # Initialize labels dict for this category

        print(f"✅ Created category: {name}")
        return self._save_database()

    def get_category(self, name: str) -> Optional[CategoryModel]:
        """Get category by name"""
        name = name.strip().lower()
        if name in self.data["categories"]:
            return CategoryModel(**self.data["categories"][name])
        return None

    def update_category(self, name: str, **kwargs) -> bool:
        """Update category"""
        name = name.strip().lower()
        if name not in self.data["categories"]:
            print(f"Category '{name}' not found")
            return False

        # Handle renaming
        if "new_name" in kwargs and kwargs["new_name"] != name:
            new_name = kwargs.pop("new_name").strip().lower()
            if new_name in self.data["categories"]:
                print(f"Category '{new_name}' already exists")
                return False

            # Move category data
            self.data["categories"][new_name] = self.data["categories"][name]
            self.data["labels"][new_name] = self.data["labels"][name]

            # Update patterns
            for pattern in self.data["patterns"]:
                if pattern["category"] == name:
                    pattern["category"] = new_name

            # Update transactions
            for transaction in self.transactions:
                if transaction.get("category") == name:
                    transaction["category"] = new_name

            # Delete old category
            del self.data["categories"][name]
            del self.data["labels"][name]
            name = new_name

        # Update other fields
        self.data["categories"][name].update(kwargs)
        self.data["categories"][name]["updated_at"] = datetime.now().isoformat()

        return self._save_database()

    def delete_category(self, name: str, force: bool = False) -> bool:
        """Delete category"""
        name = name.strip().lower()
        if name not in self.data["categories"]:
            print(f"Category '{name}' not found")
            return False

        # Check if category has labels
        if not force and self.data["labels"][name]:
            print(f"Category '{name}' has labels. Use force=True to delete")
            return False

        # Remove associated patterns
        self.data["patterns"] = [
            p for p in self.data["patterns"]
            if p["category"] != name
        ]

        # Delete category and labels
        del self.data["categories"][name]
        del self.data["labels"][name]

        print(f"✅ Deleted category: {name}")
        return self._save_database()

    def list_categories(self) -> List[CategoryModel]:
        """List all categories"""
        return [CategoryModel(**cat) for cat in self.data["categories"].values()]

    # LABEL MANAGEMENT
    def create_label(self, category: str, name: str, description: str = "",
                    patterns: List[str] = None, keywords: List[str] = None) -> bool:
        """Create a new label in a category"""
        category = category.strip().lower()
        name = name.strip().lower()

        if category not in self.data["categories"]:
            print(f"Category '{category}' not found")
            return False

        if name in [label.lower() for label in self.data["labels"][category].keys()]:
            print(f"Label '{name}' already exists in category '{category}'")
            return False

        label = LabelModel(
            name=name,
            description=description,
            patterns=patterns or [],
            keywords=keywords or []
        )
        self.data["labels"][category][name] = label.dict()

        # Create patterns from initial data
        if patterns:
            for pattern in patterns:
                self.add_pattern(pattern, category, name)

        print(f"✅ Created label: {name} in category {category}")
        return self._save_database()

    def get_label(self, category: str, name: str) -> Optional[LabelModel]:
        """Get label by category and name"""
        category = category.strip().lower()
        name = name.strip().lower()

        if category in self.data["labels"] and name in self.data["labels"][category]:
            return LabelModel(**self.data["labels"][category][name])
        return None

    def update_label(self, category: str, name: str, **kwargs) -> bool:
        """Update label"""
        category = category.strip().lower()
        name = name.strip().lower()

        if category not in self.data["labels"] or name not in self.data["labels"][category]:
            print(f"Label '{name}' not found in category '{category}'")
            return False

        # Handle renaming
        if "new_name" in kwargs and kwargs["new_name"] != name:
            new_name = kwargs.pop("new_name").strip().lower()
            if new_name in self.data["labels"][category]:
                print(f"Label '{new_name}' already exists in category '{category}'")
                return False

            # Move label data
            self.data["labels"][category][new_name] = self.data["labels"][category][name]
            del self.data["labels"][category][name]

            # Update patterns
            for pattern in self.data["patterns"]:
                if pattern["category"] == category and pattern["label"] == name:
                    pattern["label"] = new_name

            # Update transactions
            for transaction in self.transactions:
                if transaction.get("category") == category and transaction.get("label") == name:
                    transaction["label"] = new_name

            name = new_name

        # Update other fields
        self.data["labels"][category][name].update(kwargs)
        self.data["labels"][category][name]["updated_at"] = datetime.now().isoformat()

        return self._save_database()

    def delete_label(self, category: str, name: str, force: bool = False) -> bool:
        """Delete label"""
        category = category.strip().lower()
        name = name.strip().lower()

        if category not in self.data["labels"] or name not in self.data["labels"][category]:
            print(f"Label '{name}' not found in category '{category}'")
            return False

        # Check if label has patterns
        associated_patterns = [
            p for p in self.data["patterns"]
            if p["category"] == category and p["label"] == name
        ]

        if not force and associated_patterns:
            print(f"Label '{name}' has {len(associated_patterns)} patterns. Use force=True to delete")
            return False

        # Remove associated patterns
        self.data["patterns"] = [
            p for p in self.data["patterns"]
            if not (p["category"] == category and p["label"] == name)
        ]

        # Delete label
        del self.data["labels"][category][name]

        print(f"✅ Deleted label: {name} from category {category}")
        return self._save_database()

    def list_labels(self, category: str) -> List[LabelModel]:
        """List all labels in a category"""
        category = category.strip().lower()
        if category in self.data["labels"]:
            return [LabelModel(**label) for label in self.data["labels"][category].values()]
        return []

    # PATTERN MANAGEMENT
    def add_pattern(self, pattern: str, category: str, label: str, confidence: float = 0.8) -> bool:
        """Add a pattern to a label"""
        category = category.strip().lower()
        label = label.strip().lower()

        if category not in self.data["categories"]:
            print(f"Category '{category}' not found")
            return False

        if category not in self.data["labels"] or label not in self.data["labels"][category]:
            print(f"Label '{label}' not found in category '{category}'")
            return False

        pattern_model = PatternModel(
            pattern=pattern,
            confidence=confidence,
            category=category,
            label=label
        )

        self.data["patterns"].append(pattern_model.dict())

        # Add pattern to label's patterns list
        if pattern not in self.data["labels"][category][label]["patterns"]:
            self.data["labels"][category][label]["patterns"].append(pattern)

        return self._save_database()

    def remove_pattern(self, pattern: str) -> bool:
        """Remove a pattern"""
        original_count = len(self.data["patterns"])
        self.data["patterns"] = [p for p in self.data["patterns"] if p["pattern"] != pattern]
        result = len(self.data["patterns"]) < original_count and self._save_database()
        if result:
            print(f"✅ Removed pattern: {pattern}")
        return result

    def get_patterns(self, category: str = None, label: str = None) -> List[PatternModel]:
        """Get patterns, optionally filtered by category and/or label"""
        patterns = self.data["patterns"]

        if category:
            category = category.strip().lower()
            patterns = [p for p in patterns if p["category"] == category]

        if label:
            label = label.strip().lower()
            patterns = [p for p in patterns if p["label"] == label]

        return [PatternModel(**p) for p in patterns]

    # TRANSACTION MANAGEMENT
    def add_transaction(self, transaction: Dict[str, Any]) -> bool:
        """Add a transaction to the database"""
        try:
            # Validate transaction data
            validated_transaction = self._validate_transaction(transaction)

            # Add to transactions list
            self.transactions.append(validated_transaction)

            # Sort transactions by date
            self.transactions.sort(key=lambda x: x.get('date', ''))

            return self._save_transactions()
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return False

    def _validate_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Validate transaction data"""
        required_fields = ['date', 'description', 'amount']
        for field in required_fields:
            if field not in transaction:
                raise ValueError(f"Missing required field: {field}")

        # Normalize and validate date
        if isinstance(transaction['date'], str):
            # Try to parse date string
            try:
                date_obj = datetime.fromisoformat(transaction['date'].replace('Z', '+00:00'))
            except ValueError:
                date_obj = datetime.strptime(transaction['date'], '%Y-%m-%d')
            transaction['date'] = date_obj.isoformat()

        # Ensure amount is float
        transaction['amount'] = float(transaction['amount'])

        # Normalize text fields
        if 'category' in transaction and transaction['category']:
            transaction['category'] = transaction['category'].strip().lower()

        if 'label' in transaction and transaction['label']:
            transaction['label'] = transaction['label'].strip().lower()

        if 'description' in transaction:
            transaction['description'] = transaction['description'].strip()

        return transaction

    def get_transactions(self, category: str = None, label: str = None,
                        start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
        """Get transactions with optional filtering"""
        transactions = self.transactions

        if category:
            category = category.strip().lower()
            transactions = [t for t in transactions if t.get('category') == category]

        if label:
            label = label.strip().lower()
            transactions = [t for t in transactions if t.get('label') == label]

        if start_date:
            transactions = [t for t in transactions if t.get('date', '') >= start_date]

        if end_date:
            transactions = [t for t in transactions if t.get('date', '') <= end_date]

        return transactions

    # SEARCH AND MATCHING
    def find_matching_patterns(self, transaction_description: str) -> List[Dict[str, Any]]:
        """Find patterns that match a transaction description"""
        matches = []
        description_lower = transaction_description.lower()

        for pattern_data in self.data["patterns"]:
            pattern = pattern_data["pattern"].lower()

            # Check for exact match or substring match
            if pattern in description_lower:
                matches.append({
                    "pattern": pattern_data["pattern"],
                    "category": pattern_data["category"],
                    "label": pattern_data["label"],
                    "confidence": pattern_data["confidence"],
                    "match_count": pattern_data["match_count"]
                })

        # Sort by confidence (highest first)
        return sorted(matches, key=lambda x: x["confidence"], reverse=True)

    def categorize_transaction(self, description: str) -> Tuple[Optional[str], Optional[str], float]:
        """Automatically categorize a transaction based on patterns"""
        matches = self.find_matching_patterns(description)

        if not matches:
            return None, None, 0.0

        best_match = matches[0]
        threshold = self.data["settings"]["default_confidence_threshold"]

        if best_match["confidence"] >= threshold:
            # Update pattern match count
            for pattern in self.data["patterns"]:
                if pattern["pattern"] == best_match["pattern"]:
                    pattern["match_count"] += 1
                    pattern["last_matched"] = datetime.now().isoformat()
                    break

            return best_match["category"], best_match["label"], best_match["confidence"]

        return None, None, 0.0

    # STATISTICS AND REPORTING
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        return {
            "total_categories": len(self.data["categories"]),
            "total_labels": sum(len(labels) for labels in self.data["labels"].values()),
            "total_patterns": len(self.data["patterns"]),
            "total_transactions": len(self.transactions),
            "active_categories": len([
                cat for cat in self.data["categories"].values()
                if cat.get("is_active", True)
            ]),
            "last_updated": max([
                cat.get("updated_at", "")
                for cat in self.data["categories"].values()
            ] or [""])
        }

    def get_transaction_summary(self) -> Dict[str, Any]:
        """Get transaction summary statistics"""
        if not self.transactions:
            return {
                "total_transactions": 0,
                "total_income": 0.0,
                "total_expenses": 0.0,
                "net_cash_flow": 0.0,
                "date_range": None
            }

        # Calculate totals
        total_income = sum(t["amount"] for t in self.transactions if t["amount"] > 0)
        total_expenses = sum(abs(t["amount"]) for t in self.transactions if t["amount"] < 0)

        # Get date range
        dates = [t["date"] for t in self.transactions if t.get("date")]
        if dates:
            date_range = {
                "start": min(dates),
                "end": max(dates)
            }
        else:
            date_range = None

        return {
            "total_transactions": len(self.transactions),
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_cash_flow": total_income - total_expenses,
            "date_range": date_range
        }

    def _execute(self, **kwargs) -> str:
        """Execute tool operation (required by BaseTool)"""
        operation = kwargs.get("operation", "statistics")

        if operation == "statistics":
            stats = self.get_statistics()
            return f"Database Statistics: {json.dumps(stats, indent=2)}"
        elif operation == "transaction_summary":
            summary = self.get_transaction_summary()
            return f"Transaction Summary: {json.dumps(summary, indent=2)}"
        else:
            return f"Unknown operation: {operation}"


# Initialize with default South African financial categories
def initialize_default_sa_database(db_path: str = None) -> MasterTransactionDB:
    """Initialize the database with South African financial categories and labels"""
    db = MasterTransactionDB(db_path)

    # Create South African specific default categories
    default_categories = {
        "home": {
            "description": "Household expenses and maintenance (South Africa)",
            "color": "#FF6B6B",
            "labels": {
                "rent_mortgage": {
                    "description": "Bond payments or rent",
                    "patterns": ["BOND PAYMENT", "RENT PAYMENT", "PROPERTY LEVY"],
                    "keywords": ["bond", "rent", "mortgage", "property", "levy"]
                },
                "utilities": {
                    "description": "Eskom, water, rates, and internet",
                    "patterns": ["ESKOM", "CITY POWER", "MUNICIPALITY", "TELKOM", "VODACOM", "RAIN"],
                    "keywords": ["eskom", "electricity", "water", "rates", "municipal", "telkom", "internet"]
                },
                "maintenance": {
                    "description": "Home repairs and maintenance",
                    "patterns": ["BUILDER WAREHOUSE", "BUILT IT", "GAME", "CHECKERS", "HOME DEPOT"],
                    "keywords": ["builder", "built it", "maintenance", "repair", "home"]
                }
            }
        },
        "dad": {
            "description": "Dad's personal expenses",
            "color": "#4ECDC4",
            "labels": {
                "personal_care": {
                    "description": "Personal grooming and care",
                    "patterns": ["BARBER", "CLICKS", "DIS-CHEM", "GYM"],
                    "keywords": ["barber", "haircut", "clicks", "dis-chem", "gym", "personal"]
                },
                "motors": {
                    "description": "Vehicle and transport costs",
                    "patterns": ["SASOL", "ENGEN", "BP", "SHELL", "TOTAL", "CAR WASH", "TYRES"],
                    "keywords": ["sasol", "engen", "bp", "shell", "fuel", "petrol", "car", "tyres"]
                },
                "work_expenses": {
                    "description": "Work-related expenses",
                    "patterns": ["WOOLWORTHS FOOD", "KFC", "MCDONALDS", "STANDARD BANK"],
                    "keywords": ["lunch", "work", "parking", "toll", "business"]
                }
            }
        },
        "mom": {
            "description": "Mom's personal expenses",
            "color": "#95E77E",
            "labels": {
                "personal_care": {
                    "description": "Personal grooming and care",
                    "patterns": ["SALON", "SPA", "CLICKS", "DIS-CHEM"],
                    "keywords": ["salon", "spa", "nails", "beauty", "cosmetics"]
                },
                "shopping": {
                    "description": "Clothing and shopping",
                    "patterns": ["EDGARS", "JET", "PICK N PAY", "SHOPRITE", "WOOLWORTHS"],
                    "keywords": ["edgars", "jet", "clothing", "fashion", "retail", "shop"]
                },
                "groceries": {
                    "description": "Grocery shopping",
                    "patterns": ["PICK N PAY", "SHOPRITE", "CHECKERS", "WOOLWORTHS FOOD", "SPAR"],
                    "keywords": ["grocery", "food", "supermarket", "pick n pay", "shoprite", "spar"]
                }
            }
        },
        "business": {
            "description": "Business and TA-REALW expenses",
            "color": "#9B59B6",
            "labels": {
                "ta_realw": {
                    "description": "TA-REALW business expenses",
                    "patterns": ["TA-REALW", "REALW", "BUSINESS ACCOUNT", "OFFICE"],
                    "keywords": ["ta-realw", "realw", "business", "office", "company"]
                },
                "supplies": {
                    "description": "Business supplies and equipment",
                    "patterns": ["MAKER", "CASH AND CARRY", "BUNNY CHOW", "STATIONERY"],
                    "keywords": ["supplies", "equipment", "tools", "stationery", "office"]
                }
            }
        },
        "data_communication": {
            "description": "Data and communication expenses",
            "color": "#3498DB",
            "labels": {
                "mobile_data": {
                    "description": "Mobile phone and data",
                    "patterns": ["VODACOM", "MTN", "CELL C", "RAIN", "TELKOM MOBILE"],
                    "keywords": ["vodacom", "mtn", "cell c", "rain", "data", "airtime"]
                },
                "internet": {
                    "description": "Home internet and connectivity",
                    "patterns": ["TELKOM", "FIBRE", "VOX", "WEBCONNEX"],
                    "keywords": ["telkom", "fibre", "internet", "adsl", "webconnex"]
                }
            }
        },
        "motors": {
            "description": "Vehicle expenses and maintenance",
            "color": "#E67E22",
            "labels": {
                "fuel": {
                    "description": "Fuel and petrol costs",
                    "patterns": ["SASOL", "ENGEN", "BP", "SHELL", "TOTAL", "CALT"],
                    "keywords": ["sasol", "engen", "bp", "shell", "fuel", "petrol", "diesel"]
                },
                "maintenance": {
                    "description": "Vehicle maintenance and repairs",
                    "patterns": ["FIT IT", "HI-Q", "BIDVEST", "TYRE PLUS", "CAR WASH"],
                    "keywords": ["fit it", "hi-q", "tyre", "brake", "service", "car wash"]
                },
                "insurance_licensing": {
                    "description": "Vehicle insurance and licensing",
                    "patterns": ["OUTSURANCE", "MIWAY", "DISCOVERY INSURE", "LICENSE"],
                    "keywords": ["insurance", "license", "disc", "outsurance", "miway"]
                }
            }
        }
    }

    # Create categories and labels
    for category_name, category_data in default_categories.items():
        if not db.get_category(category_name):
            db.create_category(
                name=category_name,
                description=category_data["description"],
                color=category_data["color"]
            )

        for label_name, label_data in category_data["labels"].items():
            existing_labels = db.list_labels(category_name)
            if not any(label.name == label_name for label in existing_labels):
                db.create_label(
                    category=category_name,
                    name=label_name,
                    description=label_data["description"],
                    patterns=label_data["patterns"],
                    keywords=label_data["keywords"]
                )

    print("✅ Initialized South African financial database with default categories")
    return db


if __name__ == "__main__":
    # Example usage
    db = initialize_default_sa_database()
    print(f"Database created with {len(db.list_categories())} categories")
    print(f"Statistics: {db.get_statistics()}")