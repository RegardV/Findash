# 📊 Personal In and Out Dashboard

A comprehensive financial analysis dashboard designed specifically for South African users, featuring Rand (ZAR) currency support and local tax compliance.

## 🚀 Quick Start

### **One-Line Installation & Setup:**
```bash
git clone https://github.com/RegardV/Findash.git
cd Findash
./setup.sh
source venv/bin/activate
python3 start_dashboard.py
```

## 💰 Features

### **🎯 Core Functionality**
- ✅ **South African Rand (ZAR)** - Native currency support
- ✅ **CLI Dashboard** - Beautiful colored terminal interface
- ✅ **9 Menu Options** - Complete financial management
- ✅ **Bank Statement Import** - CSV processing and categorization
- ✅ **Budget Management** - Entity-based tracking (Dad, Mom, dependents, business)
- ✅ **Tax Reporting** - South African tax compliance
- ✅ **Currency Conversion** - Multi-currency support with live rates
- ✅ **Category Management** - Custom categories and labels
- ✅ **Report Generation** - Professional financial reports

### **👥 Entity-Based Budgeting**
- **Personal**: Dad, Mom, dependents (individual tracking)
- **Business**: TA-REALW and other business expenses
- **Household**: Home, family, motors, shared expenses
- **South African**: Optimized for SA banking and tax system

## 📋 Menu Options

1. **📁 Import & Process Bank Statements**
2. **📊 Generate Reports** (Monthly, Category, Tax, etc.)
3. **🏷️  Manage Categories & Labels**
4. **💰 Budget Management** (Entity-based tracking)
5. **🧾 Tax Reporting** (SA tax compliance)
6. **💼 Workspace Management** (File organization)
7. **💱 Currency Settings** (ZAR, USD, EUR, GBP, etc.)
8. **📈 Financial Analysis** (Spending patterns, insights)
9. **⚙️  System Configuration** (Settings and preferences)

## 🔧 Requirements

- **Python 3.8+**
- **Linux, macOS, or Windows with WSL**
- **Terminal with ANSI color support** (recommended)

## 📦 Installation

### **Option 1: Automatic Installation (Recommended)**
```bash
git clone https://github.com/RegardV/Findash.git
cd Findash
./setup.sh
source venv/bin/activate
python3 start_dashboard.py
```

### **Option 2: Manual Installation**
```bash
git clone https://github.com/RegardV/Findash.git
cd Findash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 start_dashboard.py
```

### **Option 3: Direct Download**
Download the latest release from GitHub and extract, then run `./setup.sh`

## 🚀 Usage

### **Start the Dashboard**
```bash
python3 start_dashboard.py
```

### **Import Bank Statements**
1. Select option 1 (Import & Process)
2. Choose CSV file path
3. Dashboard auto-processes transactions

### **Generate Reports**
1. Select option 2 (Generate Reports)
2. Choose report type:
   - Monthly Summary
   - Category Breakdown
   - Budget Analysis
   - Tax Reports

### **Manage Budgets**
1. Select option 4 (Budget Management)
2. Create entity-specific budgets
3. Track performance vs actuals

## 🌐 Currency Support

### **Default Currency: South African Rand (ZAR)**
- Symbol: R
- Format: R1,000.00
- Exchange rates: USD, EUR, GBP, JPY, CNY

### **Supported Currencies**
- **ZAR** (South African Rand) - Default 📊
- **USD** (US Dollar)
- **EUR** (Euro)
- **GBP** (British Pound)
- **JPY** (Japanese Yen)
- **CNY** (Chinese Yuan)

## 🧾 South African Tax Features

### **Tax Brackets**
- **Individual**: 18% - 36%
- **Small Business**: 15% - 28%
- **Company**: 28%

### **Deductible Expenses**
- Medical expenses: Fully deductible
- Business expenses: Generally deductible
- Education expenses: Fully deductible
- Charitable donations: Up to R75,000

## 📁 Workspace Organization

After first run, a `financial_workspace` directory is created:
```
financial_workspace/
├── master_transaction_db.json    # Transaction database
├── currencies_config.json        # Currency settings
├── budgets.json                 # Budget configurations
├── reports/                     # Generated reports
└── backups/                     # Data backups
```

## 🐳 Docker Deployment

```bash
# Build Docker image
docker build -t financial-dashboard-cli .

# Run container
docker run -it --rm \
  -v $(pwd)/data:/app/financial_workspace \
  financial-dashboard-cli
```

## 📊 Sample Reports

### **Monthly Summary Example**
```
💰 Financial Overview:
─────────────────────
Total Income: R15,450.00
Total Expenses: R8,230.50
Net Cash Flow: R7,219.50
Savings Rate: 46.8%

🏆 Top Spending Categories:
─────────────────────────
Groceries: R2,150.00 (26.1%)
Transportation: R1,890.00 (23.0%)
Home: R1,450.00 (17.6%)
Data/Communication: R890.00 (10.8%)
```

## 🔄 Updates and Maintenance

### **Update to Latest Version**
```bash
git pull origin main
pip3 install -r requirements.txt --upgrade
```

### **Backup Your Data**
```bash
cp -r financial_workspace financial_workspace_backup_$(date +%Y%m%d)
```

## 🆘 Support

### **Troubleshooting**
1. **Python Version**: Ensure Python 3.8+ is installed
2. **Dependencies**: Run `pip3 install -r requirements.txt`
3. **Permissions**: Make sure scripts are executable (`chmod +x *.sh`)
4. **Terminal**: Use a modern terminal with color support

### **Getting Help**
- Check the `docs/` directory for detailed guides
- Report issues on GitHub
- Check the FAQ in the documentation

## 🎯 Perfect For

- **South African households** managing family finances
- **Small businesses** tracking expenses and taxes
- **Individuals** managing personal budgets
- **Accountants** providing financial services
- **Financial advisors** creating client reports

## 🌟 Why This Dashboard?

- **📊 South African Optimized** - Built specifically for SA users
- **💰 Native ZAR Support** - No currency conversions needed
- **🧾 Tax Compliant** - Follows South African tax laws
- **🎨 Beautiful CLI** - Professional, user-friendly interface
- **📦 Zero Dependencies** - Standalone, no complex setup
- **🚀 Production Ready** - Robust and reliable
- **📊 Comprehensive** - All financial management features

---

## 📊 Made in South Africa for South Africans!

Built with ❤️ for South African financial management

**License**: MIT License
**Version**: 1.0.0
**Language**: Python