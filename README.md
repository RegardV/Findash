# 📊 Personal In and Out Dashboard

```
╔═══════════════════════════════════════════════════════════════════╗
║             📊 PERSONAL IN AND OUT DASHBOARD                     ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                               ║
║   💳 CSV IMPORT → 🏷️ AUTO-CATEGORIZE → 👥 FAMILY TRACKING → 📊 REPORTS   ║
║                                                               ║
║   🔥 Import bank statements → Smart categorization → Per person reports ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════════╝
```

A powerful financial analysis dashboard designed specifically for **family expense tracking** with South African context. Import bank CSV data, categorize by family members, and generate real-time expense reports per person.

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
- ✅ **Bank CSV Import** - Import and process bank statements automatically
- ✅ **Family Member Categories** - Create categories for Dad, Mom, and each dependent
- ✅ **Smart Categorization** - AI-powered transaction categorization with SA business patterns
- ✅ **Real-time Reports** - Generate expense reports per family member instantly
- ✅ **Entity-Based Budgeting** - Track budgets by person, business, or household
- ✅ **South African Optimized** - Native ZAR support and local business patterns
- ✅ **Professional CLI** - Beautiful colored terminal interface

### **👥 Family Expense Tracking System**

```
┌─────────────────────────────────────────────────────────────────┐
│                    HOW IT WORKS                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣  IMPORT BANK CSV                                           │
│     ┌─────────────────┐    ┌─────────────────┐                   │
│     │   Bank CSV      │───▶│  Transactions    │                   │
│     │                 │    │                 │                   │
│     • Date           │    • Date           │                   │
│     • Description    │    • Amount         │                   │
│     • Amount         │    • Description    │                   │
│     └─────────────────┘    └─────────────────┘                   │
│                                                                 │
│  2️⃣  AUTO-CATEGORIZE                                          │
│     ┌─────────────────┐    ┌─────────────────┐                   │
│     │  SASOL FUEL     │───▶│   Motors/Fuel   │                   │
│     │  WOOLWORTHS     │───▶│  Groceries      │                   │
│     │  TELKOM BILL    │───▶│  Data/Internet  │                   │
│     │  BARBER SHOP    │───▶│  Dad/Personal   │                   │
│     └─────────────────┘    └─────────────────┘                   │
│                                                                 │
│  3️⃣  FAMILY MEMBER ASSIGNMENT                                   │
│     ┌─────────────────┐    ┌─────────────────┐                   │
│     │  Categories     │───▶│  Family Members │                   │
│     └─────────────────┘    └─────────────────┘                   │
│           │                       │                           │
│    ┌──────┴──────┐        ┌──────┼──────┐        ┌──────────────┐ │
│    │    Dad     │        │    Mom     │        │   Business   │ │
│    │ Personal   │        │ Groceries  │        │ TA-REALW     │ │
│    │ Transport  │        │ Shopping   │        │ Supplies     │ │
│    │ Motors     │        │ Healthcare  │        │ Office       │ │
│    └────────────┘        └────────────┘        └──────────────┘ │
│                                                                 │
│  4️⃣  REAL-TIME REPORTS                                         │
│     ┌─────────────────┐    ┌─────────────────┐                   │
│     │  Transaction    │───▶│   Per Person     │                   │
│     │     Data        │    │   Expense Report │                   │
│     └─────────────────┘    └─────────────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### **🏷️ Categories & Labels System**
- **Family Member Categories**: Dad, Mom, Child1, Child2, etc.
- **Shared Categories**: Home, Motors, Groceries, Entertainment
- **Business Categories**: TA-REALW, Office Expenses, Supplies
- **Custom Labels**: Create specific labels for each family member's expenses

### **📊 What Reports Can Show**
- **Individual Expenses**: How much Dad spent this month
- **Category Breakdown**: Family groceries vs. dining out costs
- **Budget vs. Actual**: Compare planned vs. actual spending per person
- **Business vs. Personal**: Separate business expenses from family finances

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

### **📁 Import Bank Statements**
1. Select option 1 (Import & Process)
2. Choose your bank CSV file
3. **Auto-categorization happens instantly**:
   - SASOL → Motors/Fuel
   - Woolworths → Groceries
   - Telkom → Data/Internet
   - Barber → Dad/Personal
4. **Assign to family members** automatically or manually

### **📊 Generate Family Member Reports**
1. Select option 2 (Generate Reports)
2. Choose report type:
   - **Dad's Monthly Expenses** - All Dad's categorized spending
   - **Mom's Budget Report** - Compare planned vs. actual
   - **Family Grocery Spending** - Who spends what on food
   - **Child/Dependent Reports** - Track each child's expenses separately
   - **Business vs Personal** - Separate TA-REALW from family expenses

### **🏷️ Manage Family Categories**
1. Select option 3 (Manage Categories & Labels)
2. **Create family member categories**:
   - Add "John" as a new family member
   - Create labels: "John's School", "John's Sports", "John's Transport"
3. **Set spending patterns**:
   - "SCHOOL FEES" → John/School
   - "SWIMMING LESSONS" → John/Sports
   - "SCHOOL UNIFORM" → John/Personal

### **💰 Set Up Family Budgets**
1. Select option 4 (Budget Management)
2. **Create per-person budgets**:
   - Dad: R5,000/month (transport, personal care, etc.)
   - Mom: R3,000/month (groceries, shopping, healthcare)
   - Child1: R2,000/month (school, activities, clothing)
   - Business: R10,000/month (TA-REALW, supplies, office)

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

### **👨‍👩‍👧‍👦 Family Member Expense Reports**

#### **Dad's Monthly Report**
```
👨 Dad's Expenses - November 2024
=================================
🚗 Motors & Transport: R3,450.00
   • SASOL Fuel: R2,200.00
   • Car Insurance: R850.00
   • Car Wash: R400.00

💼 Business (TA-REALW): R2,150.00
   • Office Supplies: R650.00
   • Tools & Equipment: R1,500.00

👤 Personal Care: R680.00
   • Barber Shop: R150.00
   • Gym Membership: R280.00
   • Healthcare: R250.00

📊 TOTAL: R6,280.00
💳 Budget Used: 78% (of R8,000 budget)
```

#### **Mom's Monthly Report**
```
👩 Mom's Expenses - November 2024
=================================
🛒 Groceries & Household: R4,200.00
   • Pick n Pay: R2,800.00
   • Woolworths: R1,400.00

🛍️ Shopping & Personal: R1,850.00
   • Clothing: R950.00
   • Beauty & Personal Care: R600.00
   • Pharmacy: R300.00

🏥 Healthcare: R520.00
   • Doctor Visit: R300.00
   • Medication: R220.00

📊 TOTAL: R6,570.00
💳 Budget Used: 82% (of R8,000 budget)
```

#### **Child's Monthly Report (Emma - Age 12)**
```
👧 Emma's Expenses - November 2024
=================================
📚 Education & School: R2,400.00
   • School Fees: R1,800.00
   • School Supplies: R300.00
   • Tutoring: R300.00

🏃 Activities: R1,200.00
   • Swimming Lessons: R500.00
   • Dance Classes: R450.00
   • Sports Equipment: R250.00

👕 Clothing & Personal: R850.00
   • School Uniform: R400.00
   • Casual Clothes: R300.00
   • Shoes: R150.00

📊 TOTAL: R4,450.00
💳 Budget Used: 89% (of R5,000 budget)
```

#### **Family Summary Report**
```
🏠 Family Expense Overview - November 2024
==========================================
📊 TOTAL FAMILY SPENDING: R17,300.00

👥 PER PERSON BREAKDOWN:
   • Dad: R6,280.00 (36.3%)
   • Mom: R6,570.00 (38.0%)
   • Emma: R4,450.00 (25.7%)

🏷️ TOP FAMILY CATEGORIES:
   • Groceries & Food: R4,200.00 (24.3%)
   • Motors & Transport: R3,450.00 (19.9%)
   • Education & School: R2,400.00 (13.9%)
   • Shopping & Personal: R2,700.00 (15.6%)
   • Healthcare & Medical: R820.00 (4.7%)

💰 FAMILY INCOME: R25,000.00
💸 FAMILY EXPENSES: R17,300.00
📈 NET SAVINGS: R7,700.00 (30.8% savings rate)
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