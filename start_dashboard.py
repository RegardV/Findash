#!/usr/bin/env python3
"""
📊 Personal In and Out Dashboard - Main CLI Application
A comprehensive financial management system for South African users
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from financial_cli import Colors, print_header, print_separator
from config_manager import ConfigManager
from data_validator import DataValidator

class FinancialDashboard:
    """Main Financial Dashboard Application"""

    def __init__(self):
        self.config_manager = ConfigManager()
        self.data_validator = DataValidator()
        self.workspace_path = None

    def initialize_workspace(self):
        """Initialize the financial workspace"""
        try:
            # Import workspace manager after workspace is set up
            from tools.workspace_manager import WorkspaceManager
            workspace_manager = WorkspaceManager()
            self.workspace_path = workspace_manager.ensure_workspace_exists()
            print(f"{Colors.success}✅ Workspace initialized: {self.workspace_path}{Colors.reset}")
            return True
        except Exception as e:
            print(f"{Colors.error}❌ Error initializing workspace: {e}{Colors.reset}")
            return False

    def show_main_menu(self):
        """Display the main menu"""
        while True:
            print_header("📊 Personal In and Out Dashboard")
            print(f"""
{Colors.cyan('1.')} 📁 Import & Process Bank Statements
{Colors.cyan('2.')} 📊 Generate Reports
{Colors.cyan('3.')} 🏷️  Manage Categories & Labels
{Colors.cyan('4.')} 💰 Budget Management
{Colors.cyan('5.')} 🧾 Tax Reporting
{Colors.cyan('6.')} 💼 Workspace Management
{Colors.cyan('7.')} 💱 Currency Settings
{Colors.cyan('8.')} 📈 Financial Analysis
{Colors.cyan('9.')} ⚙️  System Configuration
{Colors.cyan('0.')} 🚪 Exit

{Colors.warning('Enter your choice (0-9):')} """, end="")

            choice = input().strip()

            if choice == '0':
                print(f"\n{Colors.info}👋 Thank you for using Personal In and Out Dashboard!{Colors.reset}")
                print(f"{Colors.success}📊 Goodbye!{Colors.reset}")
                break
            elif choice == '1':
                self.handle_import_statements()
            elif choice == '2':
                self.handle_generate_reports()
            elif choice == '3':
                self.handle_manage_categories()
            elif choice == '4':
                self.handle_budget_management()
            elif choice == '5':
                self.handle_tax_reporting()
            elif choice == '6':
                self.handle_workspace_management()
            elif choice == '7':
                self.handle_currency_settings()
            elif choice == '8':
                self.handle_financial_analysis()
            elif choice == '9':
                self.handle_system_configuration()
            else:
                print(f"{Colors.error}❌ Invalid choice. Please enter 0-9.{Colors.reset}")

            input(f"\n{Colors.info}Press Enter to continue...{Colors.reset}")

    def handle_import_statements(self):
        """Handle bank statement import"""
        print_separator("📁 Import & Process Bank Statements")

        try:
            from tools.bank_statement_parser import BankStatementParser
            from tools.import_chunker import ImportChunker

            parser = BankStatementParser()
            chunker = ImportChunker()

            file_path = input(f"{Colors.info}Enter CSV file path (or 'b' to go back): {Colors.reset}").strip()

            if file_path.lower() == 'b':
                return

            if not os.path.exists(file_path):
                print(f"{Colors.error}❌ File not found: {file_path}{Colors.reset}")
                return

            if not file_path.endswith('.csv'):
                print(f"{Colors.error}❌ Please provide a CSV file{Colors.reset}")
                return

            print(f"{Colors.info}🔄 Processing bank statement...{Colors.reset}")

            # Process in chunks
            results = chunker.process_file(file_path, parser.parse_chunk)

            print(f"{Colors.success}✅ Successfully processed {results['total_records']} records{Colors.reset}")
            print(f"{Colors.success}✅ Categorized {results['categorized_records']} transactions{Colors.reset}")
            print(f"{Colors.warning}⚠️  Uncategorized: {results['uncategorized_records']}{Colors.reset}")

        except Exception as e:
            print(f"{Colors.error}❌ Error processing bank statement: {e}{Colors.reset}")

    def handle_generate_reports(self):
        """Handle report generation"""
        print_separator("📊 Generate Reports")

        print(f"""
{Colors.cyan('1.')} Monthly Summary
{Colors.cyan('2.')} Category Breakdown
{Colors.cyan('3.')} Budget Analysis
{Colors.cyan('4.')} Tax Report
{Colors.cyan('5.')} Entity Spending Report
{Colors.cyan('0.')} Back to Main Menu
        """)

        choice = input(f"{Colors.warning('Choose report type (0-5):')}").strip()

        if choice == '0':
            return
        elif choice == '1':
            self.generate_monthly_summary()
        elif choice == '2':
            self.generate_category_breakdown()
        elif choice == '3':
            self.generate_budget_analysis()
        elif choice == '4':
            self.generate_tax_report()
        elif choice == '5':
            self.generate_entity_report()
        else:
            print(f"{Colors.error}❌ Invalid choice{Colors.reset}")

    def handle_manage_categories(self):
        """Handle category management"""
        print_separator("🏷️ Manage Categories & Labels")

        try:
            from tools.category_manager import CategoryManager
            manager = CategoryManager()

            while True:
                print(f"""
{Colors.cyan('1.')} List Categories
{Colors.cyan('2.')} Add Category
{Colors.cyan('3.')} Update Category
{Colors.cyan('4.')} Delete Category
{Colors.cyan('5.')} List Labels
{Colors.cyan('6.')} Add Label
{Colors.cyan('7.')} Update Label
{Colors.cyan('8.')} Delete Label
{Colors.cyan('0.')} Back to Main Menu
                """)

                choice = input(f"{Colors.warning('Choose option (0-8):')}").strip()

                if choice == '0':
                    break
                elif choice == '1':
                    self.list_categories(manager)
                elif choice == '2':
                    self.add_category(manager)
                elif choice == '3':
                    self.update_category(manager)
                elif choice == '4':
                    self.delete_category(manager)
                elif choice == '5':
                    self.list_labels(manager)
                elif choice == '6':
                    self.add_label(manager)
                elif choice == '7':
                    self.update_label(manager)
                elif choice == '8':
                    self.delete_label(manager)
                else:
                    print(f"{Colors.error}❌ Invalid choice{Colors.reset}")

        except Exception as e:
            print(f"{Colors.error}❌ Error in category management: {e}{Colors.reset}")

    def handle_budget_management(self):
        """Handle budget management"""
        print_separator("💰 Budget Management")

        try:
            from tools.budget_manager import BudgetManager
            manager = BudgetManager()

            while True:
                print(f"""
{Colors.cyan('1.')} List Budgets
{Colors.cyan('2.')} Create Budget
{Colors.cyan('3.')} Update Budget
{Colors.cyan('4.')} Delete Budget
{Colors.cyan('5.')} Budget vs Actuals Report
{Colors.cyan('0.')} Back to Main Menu
                """)

                choice = input(f"{Colors.warning('Choose option (0-5):')}").strip()

                if choice == '0':
                    break
                elif choice == '1':
                    self.list_budgets(manager)
                elif choice == '2':
                    self.create_budget(manager)
                elif choice == '3':
                    self.update_budget(manager)
                elif choice == '4':
                    self.delete_budget(manager)
                elif choice == '5':
                    self.budget_vs_actuals(manager)
                else:
                    print(f"{Colors.error}❌ Invalid choice{Colors.reset}")

        except Exception as e:
            print(f"{Colors.error}❌ Error in budget management: {e}{Colors.reset}")

    def handle_tax_reporting(self):
        """Handle tax reporting"""
        print_separator("🧾 Tax Reporting")

        try:
            from tools.tax_reporting import TaxReporting
            tax_reporter = TaxReporting()

            year = input(f"{Colors.info}Enter tax year (e.g., 2024): {Colors.reset}").strip()
            if not year:
                year = str(datetime.now().year)

            print(f"{Colors.info}🔄 Generating tax report for {year}...{Colors.reset}")

            report = tax_reporter.generate_annual_tax_report(year)

            print(f"{Colors.success}✅ Tax report generated!{Colors.reset}")
            print(f"{Colors.info}📁 Saved to: {report['file_path']}{Colors.reset}")

        except Exception as e:
            print(f"{Colors.error}❌ Error generating tax report: {e}{Colors.reset}")

    def handle_workspace_management(self):
        """Handle workspace management"""
        print_separator("💼 Workspace Management")

        try:
            from tools.workspace_manager import WorkspaceManager
            manager = WorkspaceManager()

            while True:
                print(f"""
{Colors.cyan('1.')} Show Workspace Info
{Colors.cyan('2.')} Backup Data
{Colors.cyan('3.')} Restore Data
{Colors.cyan('4.')} Clean Workspace
{Colors.cyan('5.')} Export Data
{Colors.cyan('0.')} Back to Main Menu
                """)

                choice = input(f"{Colors.warning('Choose option (0-5):')}").strip()

                if choice == '0':
                    break
                elif choice == '1':
                    self.show_workspace_info(manager)
                elif choice == '2':
                    self.backup_workspace(manager)
                elif choice == '3':
                    self.restore_workspace(manager)
                elif choice == '4':
                    self.clean_workspace(manager)
                elif choice == '5':
                    self.export_workspace_data(manager)
                else:
                    print(f"{Colors.error}❌ Invalid choice{Colors.reset}")

        except Exception as e:
            print(f"{Colors.error}❌ Error in workspace management: {e}{Colors.reset}")

    def handle_currency_settings(self):
        """Handle currency settings"""
        print_separator("💱 Currency Settings")

        try:
            from tools.currency_manager import CurrencyManager
            manager = CurrencyManager()

            current_currency = manager.get_default_currency()
            print(f"{Colors.info}Current default currency: {current_currency['name']} ({current_currency['symbol']}){Colors.reset}")

            print(f"\n{Colors.cyan('Available currencies:')}")
            currencies = manager.list_currencies()
            for i, currency in enumerate(currencies, 1):
                marker = "👉" if currency['is_default'] else "  "
                print(f"{marker} {Colors.cyan(f'{i}.')} {currency['name']} ({currency['symbol']}) - {currency['code']}")

            choice = input(f"\n{Colors.warning('Enter number to set as default (or 0 to go back): ')}{Colors.reset}").strip()

            if choice == '0':
                return
            elif choice.isdigit() and 1 <= int(choice) <= len(currencies):
                selected = currencies[int(choice) - 1]
                manager.set_default_currency(selected['code'])
                print(f"{Colors.success}✅ Default currency changed to {selected['name']}{Colors.reset}")
            else:
                print(f"{Colors.error}❌ Invalid choice{Colors.reset}")

        except Exception as e:
            print(f"{Colors.error}❌ Error in currency settings: {e}{Colors.reset}")

    def handle_financial_analysis(self):
        """Handle financial analysis"""
        print_separator("📈 Financial Analysis")

        try:
            from tools.financial_analyzer import FinancialAnalyzer
            analyzer = FinancialAnalyzer()

            print(f"""
{Colors.cyan('1.')} Spending Patterns Analysis
{Colors.cyan('2.')} Income vs Expenses Trend
{Colors.cyan('3.')} Category Growth Analysis
{Colors.cyan('4.')} Budget Performance Analysis
{Colors.cyan('5.')} Financial Health Score
{Colors.cyan('0.')} Back to Main Menu
            """)

            choice = input(f"{Colors.warning('Choose analysis type (0-5):')}").strip()

            if choice == '0':
                return
            elif choice == '1':
                self.analyze_spending_patterns(analyzer)
            elif choice == '2':
                self.analyze_income_expenses(analyzer)
            elif choice == '3':
                self.analyze_category_growth(analyzer)
            elif choice == '4':
                self.analyze_budget_performance(analyzer)
            elif choice == '5':
                self.calculate_financial_health(analyzer)
            else:
                print(f"{Colors.error}❌ Invalid choice{Colors.reset}")

        except Exception as e:
            print(f"{Colors.error}❌ Error in financial analysis: {e}{Colors.reset}")

    def handle_system_configuration(self):
        """Handle system configuration"""
        print_separator("⚙️ System Configuration")

        print(f"""
{Colors.info}📊 System Status:{Colors.reset}
• Default Currency: {self.config_manager.get('default_currency', 'ZAR')}
• Workspace Path: {self.workspace_path}
• Database Status: {'✅ Active' if self.workspace_path else '❌ Not initialized'}
• Last Backup: {self.config_manager.get('last_backup', 'Never')}

{Colors.warning('Configuration options will be added in future versions.')}
        """)

    # Helper methods for sub-menus
    def list_categories(self, manager):
        """List all categories"""
        categories = manager.list_categories()
        print(f"\n{Colors.success('📋 Categories:')}")
        for i, cat in enumerate(categories, 1):
            print(f"  {Colors.cyan(f'{i}.')} {cat['name']} - {cat['description']}")

    def add_category(self, manager):
        """Add new category"""
        name = input(f"{Colors.info('Enter category name: ')}").strip()
        description = input(f"{Colors.info('Enter description: ')}").strip()

        if name:
            result = manager.add_category(name, description)
            if result:
                print(f"{Colors.success}✅ Category added successfully{Colors.reset}")
            else:
                print(f"{Colors.error}❌ Failed to add category{Colors.reset}")

    def update_category(self, manager):
        """Update category"""
        # Implementation would go here
        print(f"{Colors.warning}⚠️ Feature coming soon{Colors.reset}")

    def delete_category(self, manager):
        """Delete category"""
        # Implementation would go here
        print(f"{Colors.warning}⚠️ Feature coming soon{Colors.reset}")

    def list_labels(self, manager):
        """List all labels"""
        labels = manager.list_labels()
        print(f"\n{Colors.success('🏷️ Labels:')}")
        for i, label in enumerate(labels, 1):
            print(f"  {Colors.cyan(f'{i}.')} {label['name']} - {label['category']}")

    def add_label(self, manager):
        """Add new label"""
        name = input(f"{Colors.info('Enter label name: ')}").strip()
        category = input(f"{Colors.info('Enter category: ')}").strip()

        if name and category:
            result = manager.add_label(name, category)
            if result:
                print(f"{Colors.success}✅ Label added successfully{Colors.reset}")
            else:
                print(f"{Colors.error}❌ Failed to add label{Colors.reset}")

    def update_label(self, manager):
        """Update label"""
        print(f"{Colors.warning}⚠️ Feature coming soon{Colors.reset}")

    def delete_label(self, manager):
        """Delete label"""
        print(f"{Colors.warning}⚠️ Feature coming soon{Colors.reset}")

    def list_budgets(self, manager):
        """List budgets"""
        budgets = manager.list_budgets()
        print(f"\n{Colors.success('💰 Budgets:')}")
        for i, budget in enumerate(budgets, 1):
            print(f"  {Colors.cyan(f'{i}.')} {budget['entity']} - {budget['category']}: R{budget['amount']}")

    def create_budget(self, manager):
        """Create budget"""
        entity = input(f"{Colors.info('Enter entity (Dad, Mom, Business, etc.): ')}").strip()
        category = input(f"{Colors.info('Enter category: ')}").strip()
        amount = input(f"{Colors.info('Enter budget amount (R): ')}").strip()

        if entity and category and amount:
            try:
                amount = float(amount.replace('R', '').replace(',', ''))
                result = manager.create_budget(entity, category, amount)
                if result:
                    print(f"{Colors.success}✅ Budget created successfully{Colors.reset}")
                else:
                    print(f"{Colors.error}❌ Failed to create budget{Colors.reset}")
            except ValueError:
                print(f"{Colors.error}❌ Invalid amount format{Colors.reset}")

    def update_budget(self, manager):
        """Update budget"""
        print(f"{Colors.warning}⚠️ Feature coming soon{Colors.reset}")

    def delete_budget(self, manager):
        """Delete budget"""
        print(f"{Colors.warning}⚠️ Feature coming soon{Colors.reset}")

    def budget_vs_actuals(self, manager):
        """Budget vs actuals report"""
        print(f"{Colors.warning}⚠️ Feature coming soon{Colors.reset}")

    def generate_monthly_summary(self):
        """Generate monthly summary report"""
        print(f"{Colors.warning}⚠️ Feature coming soon{Colors.reset}")

    def generate_category_breakdown(self):
        """Generate category breakdown report"""
        print(f"{Colors.warning}⚠️ Feature coming soon{Colors.reset}")

    def generate_budget_analysis(self):
        """Generate budget analysis report"""
        print(f"{Colors.warning}⚠️ Feature coming soon{Colors.reset}")

    def generate_tax_report(self):
        """Generate tax report"""
        print(f"{Colors.warning}⚠️ Feature coming soon{Colors.reset}")

    def generate_entity_report(self):
        """Generate entity spending report"""
        print(f"{Colors.warning}⚠️ Feature coming soon{Colors.reset}")

    def show_workspace_info(self, manager):
        """Show workspace information"""
        info = manager.get_workspace_info()
        print(f"""
{Colors.success('💼 Workspace Information:')}
📁 Path: {info['path']}
📊 Database: {info['database']}
📈 Transactions: {info['transaction_count']}
📋 Categories: {info['category_count']}
💰 Budgets: {info['budget_count']}
📅 Last Backup: {info['last_backup']}
        """)

    def backup_workspace(self, manager):
        """Backup workspace"""
        print(f"{Colors.info}🔄 Creating backup...{Colors.reset}")
        result = manager.create_backup()
        if result:
            print(f"{Colors.success}✅ Backup created: {result}{Colors.reset}")
        else:
            print(f"{Colors.error}❌ Backup failed{Colors.reset}")

    def restore_workspace(self, manager):
        """Restore workspace"""
        print(f"{Colors.warning}⚠️ Feature coming soon{Colors.reset}")

    def clean_workspace(self, manager):
        """Clean workspace"""
        print(f"{Colors.warning}⚠️ Feature coming soon{Colors.reset}")

    def export_workspace_data(self, manager):
        """Export workspace data"""
        print(f"{Colors.warning}⚠️ Feature coming soon{Colors.reset}")

    def analyze_spending_patterns(self, analyzer):
        """Analyze spending patterns"""
        print(f"{Colors.warning}⚠️ Feature coming soon{Colors.reset}")

    def analyze_income_expenses(self, analyzer):
        """Analyze income vs expenses"""
        print(f"{Colors.warning}⚠️ Feature coming soon{Colors.reset}")

    def analyze_category_growth(self, analyzer):
        """Analyze category growth"""
        print(f"{Colors.warning}⚠️ Feature coming soon{Colors.reset}")

    def analyze_budget_performance(self, analyzer):
        """Analyze budget performance"""
        print(f"{Colors.warning}⚠️ Feature coming soon{Colors.reset}")

    def calculate_financial_health(self, analyzer):
        """Calculate financial health score"""
        print(f"{Colors.warning}⚠️ Feature coming soon{Colors.reset}")

    def run(self):
        """Main entry point"""
        try:
            # Initialize workspace first
            if not self.initialize_workspace():
                print(f"{Colors.error}❌ Failed to initialize workspace. Exiting.{Colors.reset}")
                return 1

            # Show main menu
            self.show_main_menu()

            return 0

        except KeyboardInterrupt:
            print(f"\n{Colors.warning}⚠️ Application interrupted by user{Colors.reset}")
            return 1
        except Exception as e:
            print(f"{Colors.error}❌ Unexpected error: {e}{Colors.reset}")
            return 1

def main():
    """Main entry point"""
    dashboard = FinancialDashboard()
    return dashboard.run()

if __name__ == "__main__":
    sys.exit(main())