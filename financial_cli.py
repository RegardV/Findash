"""
🎨 CLI Utilities and Formatting for Personal In and Out Dashboard
Provides beautiful colored terminal interface and user interaction helpers
"""

import os
import sys
from datetime import datetime
from typing import Optional, Union, List, Dict

class Colors:
    """Terminal color codes for beautiful CLI interface"""

    # Basic colors
    reset = '\033[0m'
    bold = '\033[1m'
    dim = '\033[2m'
    italic = '\033[3m'
    underline = '\033[4m'

    # Colors
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[34m'
    magenta = '\033[35m'
    cyan = '\033[36m'
    white = '\033[37m'

    # Bright colors
    bright_black = '\033[90m'
    bright_red = '\033[91m'
    bright_green = '\033[92m'
    bright_yellow = '\033[93m'
    bright_blue = '\033[94m'
    bright_magenta = '\033[95m'
    bright_cyan = '\033[96m'
    bright_white = '\033[97m'

    # Background colors
    bg_black = '\033[40m'
    bg_red = '\033[41m'
    bg_green = '\033[42m'
    bg_yellow = '\033[43m'
    bg_blue = '\033[44m'
    bg_magenta = '\033[45m'
    bg_cyan = '\033[46m'
    bg_white = '\033[47m'

    # Semantic colors for financial dashboard
    success = green
    error = red
    warning = yellow
    info = blue
    highlight = cyan

    @staticmethod
    def supports_color() -> bool:
        """Check if terminal supports color"""
        return (
            hasattr(sys.stdout, "isatty") and sys.stdout.isatty() and
            os.environ.get('TERM') != 'dumb' and
            not os.environ.get('NO_COLOR')
        )

    @staticmethod
    def disable_colors():
        """Disable all colors (for environments that don't support them)"""
        for attr in dir(Colors):
            if not attr.startswith('_') and isinstance(getattr(Colors, attr), str):
                setattr(Colors, attr, '')

def color_enabled() -> bool:
    """Check if colors should be enabled"""
    return Colors.supports_color()

def format_currency(amount: Union[int, float], currency_code: str = "ZAR") -> str:
    """Format currency amount with appropriate symbol and formatting"""
    currency_symbols = {
        "ZAR": "R",
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "CNY": "¥",
    }

    symbol = currency_symbols.get(currency_code, currency_code)

    # Format amount with thousand separators
    if currency_code in ["ZAR", "USD", "EUR", "GBP"]:
        formatted = f"{amount:,.2f}"
    elif currency_code in ["JPY", "CNY"]:
        formatted = f"{amount:,.0f}"
    else:
        formatted = f"{amount:,.2f}"

    return f"{symbol}{formatted}"

def format_date(date_obj: datetime, format_type: str = "short") -> str:
    """Format date with different styles"""
    if format_type == "short":
        return date_obj.strftime("%Y-%m-%d")
    elif format_type == "long":
        return date_obj.strftime("%B %d, %Y")
    elif format_type == "time":
        return date_obj.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return date_obj.strftime("%Y-%m-%d")

def format_percentage(value: float, decimals: int = 1) -> str:
    """Format percentage with color coding"""
    formatted = f"{value:.{decimals}f}%"

    if value >= 0:
        return f"{Colors.success}{formatted}{Colors.reset}"
    else:
        return f"{Colors.error}{formatted}{Colors.reset}"

def print_header(title: str, width: int = 60):
    """Print a centered header with box"""
    if not color_enabled():
        print(f"\n{title:^{width}}")
        print("=" * width)
        return

    # Create top border
    border = f"{Colors.cyan}┌{'─' * (width - 2)}┐{Colors.reset}"
    print(f"\n{border}")

    # Create title line
    padding = (width - len(title) - 2) // 2
    title_line = f"{Colors.cyan}│{Colors.reset}{' ' * padding}{Colors.bold}{Colors.yellow}{title}{Colors.reset}{' ' * (width - len(title) - padding - 2)}{Colors.cyan}│{Colors.reset}"
    print(title_line)

    # Create bottom border
    border = f"{Colors.cyan}└{'─' * (width - 2)}┘{Colors.reset}"
    print(border)

def print_separator(title: str = "", width: int = 60):
    """Print a separator line with optional title"""
    if not color_enabled():
        if title:
            print(f"\n--- {title} ---")
        else:
            print("\n" + "-" * width)
        return

    if title:
        # Center the title in the separator
        title_len = len(title) + 4  # Add space for " [] "
        dashes = (width - title_len) // 2
        separator = f"\n{Colors.cyan}{'─' * dashes} [{Colors.bold}{Colors.yellow}{title}{Colors.reset}{Colors.cyan}] {'─' * (width - dashes - title_len)}{Colors.reset}"
    else:
        separator = f"\n{Colors.cyan}{'─' * width}{Colors.reset}"

    print(separator)

def print_success(message: str):
    """Print a success message"""
    if color_enabled():
        print(f"{Colors.success}✅ {message}{Colors.reset}")
    else:
        print(f"✓ {message}")

def print_error(message: str):
    """Print an error message"""
    if color_enabled():
        print(f"{Colors.error}❌ {message}{Colors.reset}")
    else:
        print(f"✗ {message}")

def print_warning(message: str):
    """Print a warning message"""
    if color_enabled():
        print(f"{Colors.warning}⚠️ {message}{Colors.reset}")
    else:
        print(f"⚠ {message}")

def print_info(message: str):
    """Print an info message"""
    if color_enabled():
        print(f"{Colors.info}ℹ️ {message}{Colors.reset}")
    else:
        print(f"ℹ {message}")

def print_list(items: List[str], bullet: str = "•", color: str = None):
    """Print a list with custom bullet and color"""
    if color and color_enabled():
        bullet = f"{color}{bullet}{Colors.reset}"

    for item in items:
        print(f"  {bullet} {item}")

def print_table(data: List[Dict[str, Union[str, int, float]]], headers: List[str] = None):
    """Print a formatted table"""
    if not data:
        print("(No data)")
        return

    # Use headers from data if not provided
    if headers is None:
        headers = list(data[0].keys())

    # Calculate column widths
    col_widths = {}
    for header in headers:
        col_widths[header] = len(header)
        for row in data:
            value = str(row.get(header, ""))
            col_widths[header] = max(col_widths[header], len(value))

    # Print header row
    header_row = " | ".join(f"{header:<{col_widths[header]}}" for header in headers)
    if color_enabled():
        header_row = f"{Colors.bold}{Colors.cyan}{header_row}{Colors.reset}"
    print(header_row)

    # Print separator
    separator = "-+-".join("-" * col_widths[header] for header in headers)
    if color_enabled():
        separator = f"{Colors.cyan}{separator}{Colors.reset}"
    print(separator)

    # Print data rows
    for row in data:
        data_row = " | ".join(f"{str(row.get(header, '')):<{col_widths[header]}}" for header in headers)
        print(data_row)

def print_progress_bar(current: int, total: int, width: int = 50, description: str = ""):
    """Print a progress bar"""
    if total == 0:
        percentage = 100
    else:
        percentage = (current / total) * 100

    filled_width = int(width * percentage / 100)
    bar = "█" * filled_width + "░" * (width - filled_width)

    if color_enabled():
        bar = f"{Colors.green}{bar}{Colors.reset}"

    description = f"{description} " if description else ""
    print(f"\r{description}[{bar}] {percentage:.1f}%", end="", flush=True)

    if current >= total:
        print()  # New line when complete

def get_user_input(prompt: str, required: bool = True, default: str = None) -> str:
    """Get user input with validation and optional default"""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "

    while True:
        try:
            user_input = input(prompt).strip()

            # Use default if provided and user didn't enter anything
            if default and not user_input:
                user_input = default

            if required and not user_input:
                print_error("This field is required. Please enter a value.")
                continue

            return user_input

        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise
        except EOFError:
            print("\nOperation cancelled.")
            raise

def get_number_input(prompt: str, min_value: float = None, max_value: float = None, default: float = None) -> float:
    """Get numeric input with validation"""
    while True:
        try:
            default_str = f" [{default}]" if default is not None else ""
            user_input = input(f"{prompt}{default_str}: ").strip()

            if default is not None and not user_input:
                user_input = str(default)

            value = float(user_input)

            if min_value is not None and value < min_value:
                print_error(f"Value must be at least {min_value}")
                continue

            if max_value is not None and value > max_value:
                print_error(f"Value must be at most {max_value}")
                continue

            return value

        except ValueError:
            print_error("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise

def get_choice_input(prompt: str, choices: List[str], default: str = None) -> str:
    """Get choice input from a list of options"""
    while True:
        try:
            # Display choices
            for i, choice in enumerate(choices, 1):
                print(f"  {i}. {choice}")

            default_str = f" [{choices.index(default) + 1}]" if default in choices else ""
            user_input = input(f"{prompt}{default_str}: ").strip()

            if default in choices and not user_input:
                return default

            choice_num = int(user_input)
            if 1 <= choice_num <= len(choices):
                return choices[choice_num - 1]
            else:
                print_error(f"Please enter a number between 1 and {len(choices)}")

        except ValueError:
            print_error("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise

def confirm(message: str, default: bool = False) -> bool:
    """Ask for yes/no confirmation"""
    default_str = "Y/n" if default else "y/N"

    while True:
        try:
            response = input(f"{message} ({default_str}): ").strip().lower()

            if not response:
                return default

            if response in ['y', 'yes', 'yep', 'yeah']:
                return True
            elif response in ['n', 'no', 'nope', 'nah']:
                return False
            else:
                print_error("Please enter 'y' or 'n'")

        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise

def pause(message: str = "Press Enter to continue..."):
    """Pause execution until user presses Enter"""
    try:
        input(f"\n{Colors.info}{message}{Colors.reset}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        raise

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_loading(message: str = "Loading...", duration: float = 2.0):
    """Show a loading animation"""
    import time
    import itertools

    spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])

    start_time = time.time()

    while time.time() - start_time < duration:
        print(f"\r{Colors.info}{next(spinner)} {message}{Colors.reset}", end="", flush=True)
        time.sleep(0.1)

    print(f"\r{Colors.success}✅ {message} completed{Colors.reset}")

def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to specified length with suffix"""
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix