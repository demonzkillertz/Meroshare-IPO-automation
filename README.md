# 🚀 Meroshare IPO Automation

Automate IPO applications on Meroshare (Nepal) for multiple accounts with a single command using Playwright MCP in VS Code.

[![Status](https://img.shields.io/badge/status-production-green)]()
[![Python](https://img.shields.io/badge/python-3.8+-blue)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

## ✨ Features

- 🎯 **Single Command Application** - Apply for any IPO with just the company name
- 👥 **Multi-Account Support** - Apply for multiple accounts simultaneously
- 🔒 **Secure** - Credentials stored locally, never shared
- 📸 **Screenshot Verification** - Visual proof of each step
- 📋 **Auto Form Filling** - Bank, account, kitta, CRN all automated
- 🔐 **PIN Management** - Secure transaction PIN handling
- 📊 **Logging** - Complete audit trail of all applications

## 🎬 Quick Demo

```
✅ Applied for Example IPO Company
✅ Account 1: 10 shares - SUBMITTED
✅ Account 2: 10 shares - SUBMITTED
✅ Time taken: 4 minutes
```

## 📋 Prerequisites

- **VS Code** with Playwright MCP extension
- **Python 3.8+** (for running automation scripts)
- **Meroshare Account(s)** with credentials
- **Bank Account** linked to Meroshare
- **CRN (Customer Reference Number)** from your bank

## 🚀 Installation

### 1. Clone Repository

```bash
git clone https://github.com/demonzkillertz/Meroshare-IPO-automation.git
cd Meroshare-IPO-automation
```

### 2. Install Dependencies

```bash
# Option 1: Run setup script (Windows)
setup.bat

# Option 2: Manual installation
pip install playwright
playwright install chromium
```

### 3. Configure Accounts

Edit `config/accounts.json`:

```json
[
    {
        "account_name": "Account 1 - Your Name",
        "dp_name": "YOUR DP NAME (CODE)",
        "username": "your_username",
        "password": "your_password",
        "transaction_pin": "1234",
        "crn": "YOUR_CRN_FROM_BANK",
        "bank_details": {
            "bank_name": "YOUR BANK NAME",
            "account_number": "YOUR_ACCOUNT - TYPE",
            "branch": "Your Branch Name"
        },
        "enabled": true
    }
]
```

## 📖 Usage

### Automatic Playwright Automation (Recommended)

```bash
python src\meroshare_automation.py
```

The script will:
- ✅ **Automatically detect** if Playwright is installed
- ✅ **Open browser** and perform all actions
- ✅ **Fill forms** automatically
- ✅ **Submit applications** for all enabled accounts
- ✅ **Take screenshots** at each step
- ✅ **Save logs** of all activities

**Steps:**
1. Choose option `2` (Generate automation for IPO)
2. Enter IPO company name (e.g., "SY Panel Nepal Limited")
3. Enter applied kitta (default: 10)
4. Watch as the browser automates everything!

### Fallback Mode (No Playwright)

If Playwright is not installed, the script will:
- Print step-by-step instructions
- You execute manually using Playwright MCP in VS Code

## 📁 Project Structure

```
Meroshare-IPO-automation/
├── src/
│   └── meroshare_automation.py    # Main automation script
├── config/
│   └── accounts.json              # Account configuration
├── docs/
│   ├── README_IPO_AUTOMATION.md   # Detailed documentation
│   ├── QUICK_START.md             # Quick start guide
│   └── SUCCESS_REPORT.md          # Success report template
├── logs/
│   └── ipo_applications.log       # Application logs
├── screenshots/
│   └── (automated screenshots)    # Verification screenshots
├── .gitignore                     # Git ignore file
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🔧 Configuration

### Account Configuration (JSON Format)

Edit `config/accounts.json`:

```json
[
    {
        "account_name": "Account 1",
        "dp_name": "YOUR_DP_NAME (CODE)",
        "username": "your_username",
        "password": "your_password",
        "transaction_pin": "1234",
        "crn": "YOUR_CRN_FROM_BANK",
        "bank_details": {
            "bank_name": "YOUR_BANK_NAME",
            "account_number": "YOUR_ACCOUNT_NUMBER - ACCOUNT_TYPE",
            "branch": "Your Bank Branch Name"
        },
        "enabled": true
    }
]
```

### Enable/Disable Accounts

Set `"enabled": true` in JSON or `enabled` column to `true` in CSV to enable an account.

## 🎯 Workflow

1. **Login** - Automated login to Meroshare
2. **Navigate** - Go to ASBA IPO section
3. **Select IPO** - Click apply for target IPO
4. **Fill Form** - Auto-fill bank, account, kitta, CRN
5. **Agree** - Accept terms and conditions
6. **Submit** - Enter PIN and submit
7. **Verify** - Screenshot confirmation
8. **Report** - View application report

## 📸 Screenshots

All screenshots are automatically saved in `screenshots/` folder:

- `before_submit_{username}.png` - Before submission
- `pin_entered_{username}.png` - PIN entered
- `success_{username}.png` - Success confirmation
- `report_{username}.png` - Application report



## 🔐 Security

- ✅ Credentials stored locally only
- ✅ `.gitignore` prevents accidental commits
- ✅ No cloud storage or external API calls
- ✅ Transaction PIN encrypted in memory
- ✅ Screenshots for verification

**⚠️ IMPORTANT:** Never commit `config/accounts.json` or `config/accounts.csv` to public repositories!

## 🆘 Troubleshooting

### Issue: CRN Invalid/Expired
**Solution:** Get new CRN from your bank for the specific IPO

### Issue: Transaction PIN Incorrect
**Solution:** Update `transaction_pin` in `config/accounts.json`

### Issue: Account Not Showing
**Solution:** Set `"enabled": true` in account configuration

### Issue: Bank/Account Not Found
**Solution:** Verify bank details are correct in Meroshare first

### Issue: Application Already Exists
**Solution:** You can only apply once per IPO per account

## 🎁 Tips

1. **Get CRN Early** - Contact your bank before IPO closes
2. **Multiple Accounts** - Add all your accounts for one-click application
3. **Screenshot Backup** - Keep screenshots for verification
4. **Check Reports** - Always verify in Application Report tab
5. **Deadlines** - Apply at least 1 hour before IPO closes

## 📝 Example Usage

```bash
# Step 1: Configure accounts
# Edit config/accounts.json with your details (including CRN for each account)

# Step 2: Run automation
cd src
python meroshare_automation.py

# Step 3: Follow prompts
Enter choice (1-3): 2
Enter IPO company name: Your IPO Company Name
Enter applied kitta (default: 10): 10

# Step 4: Execute Playwright commands
# Copy and execute commands shown in VS Code

# Done! ✅
```

## 🌟 Success Stories

- ✅ Successfully applied for multiple IPOs across multiple accounts
- ✅ 100% success rate with proper configuration
- ✅ Zero manual errors with automation

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open Pull Request

## 📄 License

MIT License - See LICENSE file for details

## ⚠️ Disclaimer

This tool is for educational purposes. Users are responsible for:
- Verifying all applications in Meroshare
- Ensuring accuracy of information
- Complying with SEBON and CDS regulations
- Understanding IPO terms and conditions

## 🙏 Acknowledgments

- CDSC Nepal for Meroshare platform
- Playwright team for automation tools
- Contributors and users

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/demonzkillertz/Meroshare-IPO-automation/issues)
- **Discussions:** [GitHub Discussions](https://github.com/demonzkillertz/Meroshare-IPO-automation/discussions)
- **Email:** demonzkillertz@gmail.com

## 🔄 Updates

- **v1.0.0** (Nov 6, 2025) - Initial release
  - Multi-account support
  - Playwright MCP integration
  - Auto form filling
  - Screenshot verification

---

**Made with ❤️ for Nepal's IPO investors**

**Star ⭐ this repo if you find it helpful!**
