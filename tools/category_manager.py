"""
🏷️ Category Manager - Standalone Version
Manages financial categories and labels with South African context
Provides CRUD operations and intelligent categorization
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path

# Import standalone base tool
from tools.base_tool import BaseTool


class Category:
    """Category data model"""
    def __init__(self, name: str, description: str = "", color: str = "#000000",
                 is_active: bool = True, created_at: str = None, updated_at: str = None):
        self.name = name.strip().lower()
        self.description = description.strip()
        self.color = color
        self.is_active = is_active
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()

    def dict(self):
        """Convert to dictionary"""
        return {
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create from dictionary"""
        return cls(**data)


class Label:
    """Label data model"""
    def __init__(self, name: str, category: str, description: str = "",
                 patterns: List[str] = None, keywords: List[str] = None,
                 is_active: bool = True, created_at: str = None, updated_at: str = None):
        self.name = name.strip().lower()
        self.category = category.strip().lower()
        self.description = description.strip()
        self.patterns = [p.strip().lower() for p in (patterns or []) if p.strip()]
        self.keywords = [k.strip().lower() for k in (keywords or []) if k.strip()]
        self.is_active = is_active
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()

    def dict(self):
        """Convert to dictionary"""
        return {
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'patterns': self.patterns,
            'keywords': self.keywords,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create from dictionary"""
        return cls(**data)


class CategoryManager(BaseTool):
    """
    Category Manager - Financial categorization system

    Features:
    - Category and label management
    - Intelligent transaction categorization
    - Pattern matching and keyword detection
    - South African business patterns
    - Entity-based categorization
    """

    def __init__(self, workspace_path: str = None):
        """Initialize category manager"""
        super().__init__()

        # Set data file path
        if workspace_path:
            self.categories_file = Path(workspace_path) / "categories_config.json"
        else:
            self.categories_file = Path("categories_config.json")

        # Load categories and labels
        self.data = self._load_categories_data()

    def _load_categories_data(self) -> Dict[str, Any]:
        """Load categories data from file"""
        try:
            if self.categories_file.exists():
                with open(self.categories_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return self._validate_and_upgrade_data(data)
            else:
                return self._create_default_categories()
        except Exception as e:
            print(f"Warning: Could not load categories data: {e}")
            return self._create_default_categories()

    def _validate_and_upgrade_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and upgrade categories data"""
        # Ensure required sections exist
        if "version" not in data:
            data["version"] = "1.0"

        if "categories" not in data:
            data["categories"] = {}

        if "labels" not in data:
            data["labels"] = []

        if "settings" not in data:
            data["settings"] = {
                "case_sensitive": False,
                "min_pattern_length": 3,
                "auto_learn": True,
                "confidence_threshold": 0.7
            }

        return data

    def _create_default_categories(self) -> Dict[str, Any]:
        """Create default South African focused categories"""
        return {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "created_by": "Personal In and Out Dashboard",
            "categories": {
                "home": Category(
                    name="home",
                    description="Household expenses and maintenance",
                    color="#FF6B6B"
                ).dict(),
                "dad": Category(
                    name="dad",
                    description="Dad's personal expenses",
                    color="#4ECDC4"
                ).dict(),
                "mom": Category(
                    name="mom",
                    description="Mom's personal expenses",
                    color="#95E77E"
                ).dict(),
                "business": Category(
                    name="business",
                    description="Business and TA-REALW expenses",
                    color="#9B59B6"
                ).dict(),
                "data_communication": Category(
                    name="data_communication",
                    description="Data and communication expenses",
                    color="#3498DB"
                ).dict(),
                "motors": Category(
                    name="motors",
                    description="Vehicle expenses and maintenance",
                    color="#E67E22"
                ).dict(),
                "groceries": Category(
                    name="groceries",
                    description="Grocery shopping and household items",
                    color="#2ECC71"
                ).dict(),
                "health": Category(
                    name="health",
                    description="Healthcare and medical expenses",
                    color="#E74C3C"
                ).dict(),
                "entertainment": Category(
                    name="entertainment",
                    description="Entertainment and leisure",
                    color="#F39C12"
                ).dict(),
                "education": Category(
                    name="education",
                    description="Education and learning expenses",
                    color="#8E44AD"
                ).dict(),
                "savings": Category(
                    name="savings",
                    description="Savings and investments",
                    color="#16A085"
                ).dict(),
                "other": Category(
                    name="other",
                    description="Miscellaneous expenses",
                    color="#95A5A6"
                ).dict()
            },
            "labels": [
                # Home labels
                Label(
                    name="rent_mortgage",
                    category="home",
                    description="Bond payments or rent",
                    patterns=["bond payment", "rent payment", "property levy", "municipal rates"],
                    keywords=["bond", "rent", "mortgage", "property", "levy", "rates"]
                ).dict(),
                Label(
                    name="utilities",
                    category="home",
                    description="Eskom, water, rates, and internet",
                    patterns=["eskom", "city power", "municipality", "telkom", "vodacom fibre", "rain internet"],
                    keywords=["eskom", "electricity", "water", "rates", "municipal", "telkom", "internet"]
                ).dict(),
                Label(
                    name="maintenance",
                    category="home",
                    description="Home repairs and maintenance",
                    patterns=["builder warehouse", "built it", "game", "checkers", "home depot", "builders"],
                    keywords=["builder", "built it", "maintenance", "repair", "home", "builders"]
                ).dict(),

                # Dad labels
                Label(
                    name="personal_care",
                    category="dad",
                    description="Personal grooming and care",
                    patterns=["barber", "clicks", "dis-chem", "gym", "pharmacy"],
                    keywords=["barber", "haircut", "clicks", "dis-chem", "gym", "personal", "pharmacy"]
                ).dict(),
                Label(
                    name="motors_transport",
                    category="dad",
                    description="Vehicle and transport costs",
                    patterns=["sasol", "engen", "bp", "shell", "total", "car wash", "tyres", "uber", "taxi"],
                    keywords=["sasol", "engen", "bp", "shell", "fuel", "petrol", "car", "tyres", "uber", "taxi"]
                ).dict(),
                Label(
                    name="work_lunch",
                    category="dad",
                    description="Work-related food expenses",
                    patterns=["woolworths food", "kfc", "mcdonalds", "debonairs", "steers", "wimpy"],
                    keywords=["lunch", "work", "parking", "toll", "kfc", "mcdonalds", "debonairs"]
                ).dict(),

                # Mom labels
                Label(
                    name="personal_care",
                    category="mom",
                    description="Personal grooming and care",
                    patterns=["salon", "spa", "clicks", "dis-chem", "beauty", "cosmetics"],
                    keywords=["salon", "spa", "nails", "beauty", "cosmetics", "skincare"]
                ).dict(),
                Label(
                    name="shopping_clothing",
                    category="mom",
                    description="Clothing and shopping",
                    patterns=["edgars", "jet", "pick n pay", "shoprite", "woolworths", "truworths"],
                    keywords=["edgars", "jet", "clothing", "fashion", "retail", "shop", "woolworths"]
                ).dict(),
                Label(
                    name="groceries_household",
                    category="mom",
                    description="Grocery shopping",
                    patterns=["pick n pay", "shoprite", "checkers", "woolworths food", "spar"],
                    keywords=["grocery", "food", "supermarket", "pick n pay", "shoprite", "spar", "checkers"]
                ).dict(),

                # Business labels
                Label(
                    name="ta_realw",
                    category="business",
                    description="TA-REALW business expenses",
                    patterns=["ta-realw", "realw", "business account", "office", "company"],
                    keywords=["ta-realw", "realw", "business", "office", "company", "work"]
                ).dict(),
                Label(
                    name="supplies_equipment",
                    category="business",
                    description="Business supplies and equipment",
                    patterns=["maker", "cash and carry", "bunny chow", "stationery", "pioneer"],
                    keywords=["supplies", "equipment", "tools", "stationery", "office", "pioneer", "cash and carry"]
                ).dict(),

                # Data & Communication labels
                Label(
                    name="mobile_data",
                    category="data_communication",
                    description="Mobile phone and data",
                    patterns=["vodacom", "mtn", "cell c", "rain", "telkom mobile", "airtime", "data"],
                    keywords=["vodacom", "mtn", "cell c", "rain", "data", "airtime", "mobile"]
                ).dict(),
                Label(
                    name="internet",
                    category="data_communication",
                    description="Home internet and connectivity",
                    patterns=["telkom", "fibre", "vox", "webconnex", "openserve", "vuma"],
                    keywords=["telkom", "fibre", "internet", "adsl", "webconnex", "openserve", "vuma"]
                ).dict(),

                # Motors labels
                Label(
                    name="fuel",
                    category="motors",
                    description="Fuel and petrol costs",
                    patterns=["sasol", "engen", "bp", "shell", "total", "caltex", "garage"],
                    keywords=["sasol", "engen", "bp", "shell", "fuel", "petrol", "diesel", "garage"]
                ).dict(),
                Label(
                    name="maintenance_repairs",
                    category="motors",
                    description="Vehicle maintenance and repairs",
                    patterns=["fit it", "hi-q", "bidvest", "tyre plus", "car wash", "service", "brakes"],
                    keywords=["fit it", "hi-q", "tyre", "brake", "service", "car wash", "maintenance", "repairs"]
                ).dict(),
                Label(
                    name="insurance_licensing",
                    category="motors",
                    description="Vehicle insurance and licensing",
                    patterns=["outsurance", "miway", "discovery insure", "license", "disc", "registration"],
                    keywords=["insurance", "license", "disc", "outsurance", "miway", "discovery", "registration"]
                ).dict()
            ],
            "settings": {
                "case_sensitive": False,
                "min_pattern_length": 3,
                "auto_learn": True,
                "confidence_threshold": 0.7
            }
        }

    def _save_categories_data(self) -> bool:
        """Save categories data to file"""
        try:
            # Ensure directory exists
            self.categories_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.categories_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"Error saving categories data: {e}")
            return False

    def list_categories(self):
        """List all categories"""
        return [Category.from_dict(cat_data) for cat_data in self.data["categories"].values()]

    def list_labels(self):
        """List all labels"""
        return [Label.from_dict(label_data) for label_data in self.data["labels"]]

    def categorize_transaction(self, description: str, amount: float = 0) -> Tuple[Optional[str], Optional[str], float]:
        """
        Automatically categorize a transaction based on description and amount
        Returns: (category, label, confidence_score)
        """
        description_lower = description.lower().strip()
        best_match = {"category": None, "label": None, "score": 0.0}

        for label_data in self.data["labels"]:
            if not label_data["is_active"]:
                continue

            score = self._calculate_match_score(description_lower, label_data, amount)

            if score > best_match["score"]:
                best_match = {
                    "category": label_data["category"],
                    "label": label_data["name"],
                    "score": score
                }

        threshold = self.data["settings"]["confidence_threshold"]
        if best_match["score"] >= threshold:
            return best_match["category"], best_match["label"], best_match["score"]

        return None, None, 0.0

    def _calculate_match_score(self, description: str, label_data: Dict[str, Any], amount: float = 0) -> float:
        """Calculate match score for a label"""
        score = 0.0

        # Pattern matching (higher weight)
        for pattern in label_data["patterns"]:
            if pattern in description:
                score += 0.4

        # Keyword matching (medium weight)
        for keyword in label_data["keywords"]:
            if keyword in description:
                score += 0.2

        # Exact phrase matching (highest weight)
        if label_data["name"] in description:
            score += 0.3

        # Amount-based matching (if applicable)
        # Some categories have typical amount ranges
        if amount > 0:
            category = label_data["category"]
            if category in ["groceries", "home"] and amount > 200:
                score += 0.1
            elif category in ["motors"] and amount > 100:
                score += 0.1
            elif category in ["data_communication"] and 50 < amount < 1000:
                score += 0.1

        # Cap score at 1.0
        return min(score, 1.0)

    def get_statistics(self) -> Dict[str, Any]:
        """Get category and label statistics"""
        total_labels = len(self.data["labels"])
        active_labels = len([label for label in self.data["labels"] if label["is_active"]])

        # Count labels per category
        labels_per_category = {}
        for label_data in self.data["labels"]:
            category = label_data["category"]
            labels_per_category[category] = labels_per_category.get(category, 0) + 1

        return {
            "total_categories": len(self.data["categories"]),
            "total_labels": total_labels,
            "active_labels": active_labels,
            "inactive_labels": total_labels - active_labels,
            "labels_per_category": labels_per_category,
            "settings": self.data["settings"]
        }

    def _execute(self, **kwargs) -> str:
        """Execute tool operation (required by BaseTool)"""
        operation = kwargs.get("operation", "statistics")

        if operation == "statistics":
            stats = self.get_statistics()
            return f"Category Statistics: {json.dumps(stats, indent=2)}"
        elif operation == "categorize":
            description = kwargs.get("description", "")
            amount = kwargs.get("amount", 0)
            if not description:
                return "Description is required for categorization"

            category, label, confidence = self.categorize_transaction(description, amount)
            if category and label:
                return f"Categorized as: {category}/{label} (confidence: {confidence:.2f})"
            else:
                return "No matching category found"
        else:
            return f"Unknown operation: {operation}"


if __name__ == "__main__":
    # Example usage
    manager = CategoryManager()

    print("=== Personal In and Out Dashboard - Category Manager ===")
    print(f"Categories: {len(manager.list_categories())}")
    print(f"Labels: {len(manager.list_labels())}")

    # Test categorization
    test_transactions = [
        "SASOL FUEL PRETORIA",
        "WOOLWORTHS FOODS",
        "TELKOM INTERNET BILL",
        "TA-REALW BUSINESS EXPENSE",
        "VODACOM AIRTIME RECHARGE"
    ]

    print(f"\n🏷️ Testing automatic categorization:")
    for transaction in test_transactions:
        category, label, confidence = manager.categorize_transaction(transaction)
        if category and label:
            print(f"  {transaction} -> {category}/{label} ({confidence:.2f})")
        else:
            print(f"  {transaction} -> Uncategorized")