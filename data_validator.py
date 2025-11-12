"""
✅ Data Validation for Personal In and Out Dashboard
Provides validation for financial data, user inputs, and file formats
"""

import re
from datetime import datetime, date
from typing import Any, Dict, List, Optional, Union, Tuple
from pathlib import Path

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class DataValidator:
    """Validates various types of financial data"""

    def __init__(self):
        # South African bank account regex patterns
        self.bank_account_patterns = {
            'absa': r'^\d{10,13}$',
            'standard_bank': r'^\d{10,11}$',
            'fnb': r'^\d{9,10}$',
            'nedbank': r'^\d{9,11}$',
            'capitec': r'^\d{10}$',
            'investec': r'^\d{11}$'
        }

        # South African ID number pattern
        self.sa_id_pattern = r'^(\d{2})(\d{2})(\d{2})(\d{4})(\d{1})(\d{1})(\d{1})$'

        # Email pattern
        self.email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # Phone pattern (South African)
        self.phone_pattern = r'^(\+27|0)?[6-7][0-9]{8}$'

    def validate_amount(self, amount: Union[str, int, float]) -> float:
        """Validate and convert amount to float"""
        try:
            # Remove common formatting characters
            if isinstance(amount, str):
                # Remove currency symbols, spaces, commas
                amount_clean = re.sub(r'[R$\€\£\s,]', '', amount)
                amount = float(amount_clean)
            elif isinstance(amount, int):
                amount = float(amount)

            # Check if amount is reasonable
            if abs(amount) > 999999999:  # 999 million max
                raise ValidationError(f"Amount too large: {amount}")

            if not isinstance(amount, float):
                raise ValidationError(f"Invalid amount format: {amount}")

            return amount

        except (ValueError, TypeError) as e:
            raise ValidationError(f"Invalid amount format: {amount}")

    def validate_date(self, date_input: Union[str, datetime, date], formats: List[str] = None) -> datetime:
        """Validate and convert date input to datetime"""
        if formats is None:
            formats = [
                '%Y-%m-%d',          # 2024-01-15
                '%d/%m/%Y',          # 15/01/2024
                '%d-%m-%Y',          # 15-01-2024
                '%Y/%m/%d',          # 2024/01/15
                '%d %b %Y',          # 15 Jan 2024
                '%d %B %Y',          # 15 January 2024
                '%b %d, %Y',         # Jan 15, 2024
                '%B %d, %Y',         # January 15, 2024
            ]

        if isinstance(date_input, datetime):
            return date_input

        if isinstance(date_input, date):
            return datetime.combine(date_input, datetime.min.time())

        if isinstance(date_input, str):
            date_input = date_input.strip()

            for fmt in formats:
                try:
                    return datetime.strptime(date_input, fmt)
                except ValueError:
                    continue

            # Try natural language parsing (simple cases)
            if date_input.lower() in ['today', 'now']:
                return datetime.now()
            elif date_input.lower() == 'yesterday':
                return datetime.now().replace(hour=0, minute=0, second=0) - datetime.timedelta(days=1)

        raise ValidationError(f"Invalid date format: {date_input}")

    def validate_currency_code(self, currency_code: str) -> str:
        """Validate currency code"""
        if not isinstance(currency_code, str):
            raise ValidationError("Currency code must be a string")

        currency_code = currency_code.upper().strip()

        valid_currencies = ['ZAR', 'USD', 'EUR', 'GBP', 'JPY', 'CNY']
        if currency_code not in valid_currencies:
            raise ValidationError(f"Invalid currency code: {currency_code}. Valid codes: {', '.join(valid_currencies)}")

        return currency_code

    def validate_email(self, email: str) -> str:
        """Validate email address"""
        if not isinstance(email, str):
            raise ValidationError("Email must be a string")

        email = email.strip().lower()

        if not re.match(self.email_pattern, email):
            raise ValidationError(f"Invalid email format: {email}")

        return email

    def validate_phone(self, phone: str) -> str:
        """Validate South African phone number"""
        if not isinstance(phone, str):
            raise ValidationError("Phone number must be a string")

        phone = re.sub(r'[\s\-\(\)]', '', phone.strip())  # Remove spaces, dashes, parentheses

        if not re.match(self.phone_pattern, phone):
            raise ValidationError(f"Invalid South African phone number: {phone}")

        # Normalize to international format
        if phone.startswith('0'):
            phone = '+27' + phone[1:]
        elif not phone.startswith('+27'):
            phone = '+27' + phone

        return phone

    def validate_sa_id_number(self, id_number: str) -> Tuple[str, datetime, str]:
        """Validate South African ID number"""
        if not isinstance(id_number, str):
            raise ValidationError("ID number must be a string")

        id_number = re.sub(r'\s', '', id_number.strip())

        if len(id_number) != 13:
            raise ValidationError("South African ID number must be 13 digits")

        if not id_number.isdigit():
            raise ValidationError("ID number must contain only digits")

        match = re.match(self.sa_id_pattern, id_number)
        if not match:
            raise ValidationError("Invalid ID number format")

        # Extract components
        yy = int(match.group(1))
        mm = int(match.group(2))
        dd = int(match.group(3))
        citizenship = match.group(6)

        # Determine century (simplified - assumes no one is over 100 years old)
        current_year = datetime.now().year
        current_century = current_year // 100 * 100
        year_2digit = current_year % 100

        if yy <= year_2digit:
            year = current_century + yy
        else:
            year = current_century + yy - 100

        try:
            birth_date = datetime(year, mm, dd)
        except ValueError:
            raise ValidationError("Invalid date in ID number")

        # Citizenship status
        citizenship_str = "SA Citizen" if citizenship == '0' else "Permanent Resident"

        return id_number, birth_date, citizenship_str

    def validate_bank_account(self, account_number: str, bank_code: str = None) -> str:
        """Validate South African bank account number"""
        if not isinstance(account_number, str):
            raise ValidationError("Account number must be a string")

        account_number = re.sub(r'[\s\-\_]', '', account_number.strip())

        if not account_number.isdigit():
            raise ValidationError("Account number must contain only digits")

        if bank_code and bank_code.lower() in self.bank_account_patterns:
            pattern = self.bank_account_patterns[bank_code.lower()]
            if not re.match(pattern, account_number):
                raise ValidationError(f"Invalid account number format for {bank_code}")
        else:
            # Generic validation (6-20 digits)
            if not 6 <= len(account_number) <= 20:
                raise ValidationError("Account number must be 6-20 digits")

        return account_number

    def validate_transaction_data(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Validate transaction data"""
        required_fields = ['date', 'description', 'amount']
        validated_transaction = {}

        # Check required fields
        for field in required_fields:
            if field not in transaction:
                raise ValidationError(f"Missing required field: {field}")

        # Validate date
        validated_transaction['date'] = self.validate_date(transaction['date'])

        # Validate amount
        validated_transaction['amount'] = self.validate_amount(transaction['amount'])

        # Validate description
        description = transaction.get('description', '').strip()
        if not description:
            raise ValidationError("Transaction description cannot be empty")
        validated_transaction['description'] = description

        # Validate optional fields
        if 'category' in transaction:
            validated_transaction['category'] = transaction['category'].strip()

        if 'label' in transaction:
            validated_transaction['label'] = transaction['label'].strip()

        if 'entity' in transaction:
            validated_transaction['entity'] = transaction['entity'].strip()

        if 'currency' in transaction:
            validated_transaction['currency'] = self.validate_currency_code(transaction['currency'])

        if 'reference' in transaction:
            validated_transaction['reference'] = str(transaction['reference']).strip()

        # Add validation timestamp
        validated_transaction['validated_at'] = datetime.now().isoformat()

        return validated_transaction

    def validate_csv_headers(self, headers: List[str], required_headers: List[str] = None) -> bool:
        """Validate CSV headers for bank statement import"""
        if required_headers is None:
            required_headers = ['date', 'description', 'amount']

        normalized_headers = [h.lower().strip() for h in headers]

        missing_headers = []
        for required in required_headers:
            if not any(required in header for header in normalized_headers):
                missing_headers.append(required)

        if missing_headers:
            raise ValidationError(f"Missing required CSV columns: {', '.join(missing_headers)}")

        return True

    def validate_budget_data(self, budget: Dict[str, Any]) -> Dict[str, Any]:
        """Validate budget data"""
        required_fields = ['entity', 'category', 'amount']
        validated_budget = {}

        # Check required fields
        for field in required_fields:
            if field not in budget:
                raise ValidationError(f"Missing required field: {field}")

        # Validate entity
        entity = budget.get('entity', '').strip()
        if not entity:
            raise ValidationError("Budget entity cannot be empty")
        validated_budget['entity'] = entity

        # Validate category
        category = budget.get('category', '').strip()
        if not category:
            raise ValidationError("Budget category cannot be empty")
        validated_budget['category'] = category

        # Validate amount
        amount = self.validate_amount(budget['amount'])
        if amount <= 0:
            raise ValidationError("Budget amount must be positive")
        validated_budget['amount'] = amount

        # Validate optional fields
        if 'period' in budget:
            period = budget['period'].lower().strip()
            valid_periods = ['monthly', 'weekly', 'yearly', 'quarterly']
            if period not in valid_periods:
                raise ValidationError(f"Invalid period. Valid options: {', '.join(valid_periods)}")
            validated_budget['period'] = period

        if 'start_date' in budget:
            validated_budget['start_date'] = self.validate_date(budget['start_date'])

        if 'end_date' in budget:
            validated_budget['end_date'] = self.validate_date(budget['end_date'])

        # Add validation timestamp
        validated_budget['validated_at'] = datetime.now().isoformat()

        return validated_budget

    def validate_file_path(self, file_path: Union[str, Path], must_exist: bool = True) -> Path:
        """Validate file path"""
        try:
            path = Path(file_path)

            if must_exist and not path.exists():
                raise ValidationError(f"File does not exist: {path}")

            if must_exist and not path.is_file():
                raise ValidationError(f"Path is not a file: {path}")

            # Check for dangerous path traversal
            if '..' in str(path):
                raise ValidationError("Path traversal not allowed")

            return path

        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Invalid file path: {file_path}")

    def validate_category_name(self, name: str) -> str:
        """Validate category name"""
        if not isinstance(name, str):
            raise ValidationError("Category name must be a string")

        name = name.strip()
        if not name:
            raise ValidationError("Category name cannot be empty")

        if len(name) > 50:
            raise ValidationError("Category name too long (max 50 characters)")

        if not re.match(r'^[a-zA-Z0-9\s\-_/&]+$', name):
            raise ValidationError("Category name contains invalid characters")

        return name

    def validate_entity_name(self, name: str) -> str:
        """Validate entity name"""
        if not isinstance(name, str):
            raise ValidationError("Entity name must be a string")

        name = name.strip()
        if not name:
            raise ValidationError("Entity name cannot be empty")

        if len(name) > 30:
            raise ValidationError("Entity name too long (max 30 characters)")

        if not re.match(r'^[a-zA-Z0-9\s\-_]+$', name):
            raise ValidationError("Entity name contains invalid characters")

        return name

    def validate_tax_year(self, year: Union[str, int]) -> int:
        """Validate tax year"""
        try:
            if isinstance(year, str):
                year = int(year.strip())

            current_year = datetime.now().year

            if year < 2000 or year > current_year + 1:
                raise ValidationError(f"Tax year must be between 2000 and {current_year + 1}")

            return year

        except ValueError:
            raise ValidationError(f"Invalid tax year: {year}")

    def sanitize_input(self, text: str) -> str:
        """Sanitize user input to prevent injection"""
        if not isinstance(text, str):
            return ""

        # Remove potentially dangerous characters
        text = re.sub(r'[<>"\']', '', text)

        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def validate_data_consistency(self, data: List[Dict[str, Any]]) -> List[str]:
        """Validate consistency across multiple records"""
        issues = []

        if not data:
            return ["No data provided"]

        # Check for duplicate transactions
        seen_transactions = set()
        for i, transaction in enumerate(data):
            # Create a unique key based on date, description, and amount
            key = (
                transaction.get('date', ''),
                transaction.get('description', ''),
                transaction.get('amount', 0)
            )

            if key in seen_transactions:
                issues.append(f"Duplicate transaction found at row {i + 1}: {transaction}")
            else:
                seen_transactions.add(key)

        # Check date ranges
        dates = [t.get('date') for t in data if 'date' in t]
        if dates:
            min_date = min(dates)
            max_date = max(dates)

            # Check for future dates
            future_dates = [d for d in dates if d > datetime.now()]
            if future_dates:
                issues.append(f"Found {len(future_dates)} transactions with future dates")

            # Check for very old dates (more than 10 years)
            ten_years_ago = datetime.now().replace(year=datetime.now().year - 10)
            old_dates = [d for d in dates if d < ten_years_ago]
            if old_dates:
                issues.append(f"Found {len(old_dates)} transactions more than 10 years old")

        return issues

    def __str__(self) -> str:
        return "DataValidator"