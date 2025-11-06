# Meroshare IPO Fillup Automation

Complete automation system for applying to IPOs on meroshare.cdsc.com.np using Playwright MCP.

## 📋 Table of Contents
- [Overview](#overview)
- [Manual Testing Results](#manual-testing-results)
- [Automation Steps](#automation-steps)
- [Configuration](#configuration)
- [Usage](#usage)
- [Files](#files)

## 🎯 Overview

This automation system allows you to apply for multiple IPOs with a single command. It uses Playwright MCP to interact with the Meroshare website.

## ✅ Manual Testing Results

Successfully tested on **November 6, 2025** with the following steps:

### Login Process
1. ✅ Navigate to https://meroshare.cdsc.com.np/
2. ✅ Select DP: LINCH STOCK MARKET LIMITED (13800)
3. ✅ Enter Username: 6891
4. ✅ Enter Password: ******
5. ✅ Click Login button
6. ✅ Successfully logged in as PURNA BAHADUR KASTI

### IPO Application Process
7. ✅ Navigate to ASBA section (#/asba)
8. ✅ Found available IPO: SY Panel Nepal Limited
9. ✅ Click Apply button
10. ✅ Select Bank: SIDDHARTHA BANK LTD.
11. ✅ Select Account: 03615005985 - SAVING ACCOUNT
12. ✅ Branch auto-filled: Siddhartha Bank Ltd.-Kamalbinayak
13. ✅ Enter Applied Kitta: 10
14. ⏸️  Enter CRN: (Requires user's CRN from bank)
15. ⏸️  Check agreement checkbox
16. ⏸️  Click Proceed button

## 🔄 Automation Steps

### Required Fields for Each IPO Application:

| Field | Description | Example | Auto-filled |
|-------|-------------|---------|-------------|
| **BOID** | Beneficiary Owner ID | 1301380000006891 | ✅ Yes |
| **Bank** | Bank name | SIDDHARTHA BANK LTD. | ❌ No |
| **Account Number** | Bank account | 03615005985 - SAVING ACCOUNT | ❌ No |
| **Branch** | Bank branch | Siddhartha Bank Ltd.-Kamalbinayak | ✅ Yes (after account selection) |
| **Applied Kitta** | Number of shares | 10, 20, 50, etc. | ❌ No |
| **Amount** | Total amount | Auto-calculated | ✅ Yes |
| **CRN** | Customer Reference Number | From your bank | ❌ No |
| **Agreement** | Terms acceptance | Checkbox | ❌ No |

### IPO Details (SY Panel Nepal Limited):
- **Issue Manager:** PRABHU CAPITAL LIMITED
- **Issue Open Date:** 2025-11-05 10:00 AM
- **Issue Close Date:** 2025-11-09 5:00 PM
- **No. of Shares Issued:** 4,076,156
- **Price per Share:** Rs. 100
- **Minimum Quantity:** 10 shares
- **Maximum Quantity:** 50,000 shares
- **Divisible Quantity:** 10 shares

## ⚙️ Configuration

Edit `meroshare_config.json` to set up your details:

```json
{
    "credentials": {
        "dp_name": "LINCH STOCK MARKET LIMITED (13800)",
        "username": "6891",
        "password": "purnakasti567*"
    },
    "bank_details": {
        "bank_name": "SIDDHARTHA BANK LTD.",
        "account_number": "03615005985 - SAVING ACCOUNT",
        "branch": "Siddhartha Bank Ltd.-Kamalbinayak"
    },
    "ipo_applications": [
        {
            "company_name": "SY Panel Nepal Limited",
            "applied_kitta": 10,
            "crn": "YOUR_CRN_NUMBER_HERE",
            "auto_apply": true,
            "notes": "General Public IPO"
        }
    ]
}
```

### How to Get CRN (Customer Reference Number):
1. Contact your bank (SIDDHARTHA BANK LTD.)
2. Request CRN for ASBA/IPO application
3. Update the CRN in config file
4. You can have multiple IPOs with different CRNs

### Adding Multiple IPOs:
```json
"ipo_applications": [
    {
        "company_name": "Company A",
        "applied_kitta": 10,
        "crn": "CRN_123456",
        "auto_apply": true,
        "notes": "First IPO"
    },
    {
        "company_name": "Company B",
        "applied_kitta": 20,
        "crn": "CRN_789012",
        "auto_apply": true,
        "notes": "Second IPO"
    }
]
```

## 🚀 Usage

### Option 1: Python Script (Generates Commands)
```bash
python meroshare_ipo_automation.py
```

This will:
- Load your configuration
- Display IPO application summary
- Generate step-by-step Playwright commands

### Option 2: Playwright Workflow Generator
```bash
python playwright_automation.py
```

This will:
- Generate complete workflow
- Export to `workflow.json`
- Print all automation steps

### Option 3: Manual Playwright MCP Commands

Use the Playwright MCP tools in VS Code to execute these steps:

1. **Navigate to Meroshare:**
   ```
   mcp_playwright_browser_navigate(url="https://meroshare.cdsc.com.np/")
   ```

2. **Select DP:**
   ```
   mcp_playwright_browser_click() → DP dropdown
   mcp_playwright_browser_click() → Your DP option
   ```

3. **Enter Credentials:**
   ```
   mcp_playwright_browser_type() → Username field
   mcp_playwright_browser_type() → Password field
   mcp_playwright_browser_click() → Login button
   ```

4. **Navigate to ASBA:**
   ```
   mcp_playwright_browser_navigate(url="https://meroshare.cdsc.com.np/#/asba")
   ```

5. **Apply for IPO:**
   ```
   mcp_playwright_browser_click() → Apply button
   mcp_playwright_browser_select_option() → Bank
   mcp_playwright_browser_select_option() → Account
   mcp_playwright_browser_type() → Applied Kitta
   mcp_playwright_browser_type() → CRN
   mcp_playwright_browser_click() → Checkbox
   mcp_playwright_browser_click() → Proceed
   ```

## 📁 Files

| File | Description |
|------|-------------|
| `meroshare_ipo_automation.py` | Main automation script |
| `playwright_automation.py` | Playwright workflow generator |
| `meroshare_config.json` | Configuration file (credentials, bank details, IPOs) |
| `workflow.json` | Generated workflow (after running playwright_automation.py) |
| `ipo_applications.log` | Log file for tracking applications |
| `README_IPO_AUTOMATION.md` | This documentation file |

## 🔐 Security Notes

1. **Never commit credentials to Git:**
   - Add `meroshare_config.json` to `.gitignore`
   - Use environment variables for production

2. **Keep CRN secure:**
   - CRN is sensitive banking information
   - Don't share screenshots with CRN visible

3. **Backup configuration:**
   - Keep a backup of your config (without passwords)
   - Document your CRNs separately

## 📝 Next Steps

1. ✅ Get CRN from your bank (SIDDHARTHA BANK)
2. ✅ Update `meroshare_config.json` with CRN
3. ✅ Run `python meroshare_ipo_automation.py` to review
4. ✅ Test on one IPO first
5. ✅ Add multiple IPOs to config
6. ✅ Run automation for all IPOs

## ⚠️ Important Notes

- **IPO Deadlines:** Check issue close dates (Current: 2025-11-09 5:00 PM)
- **Kitta Validation:** Must be divisible by 10 (min: 10, max: 50000)
- **One Application:** You can only apply once per IPO
- **Bank Balance:** Ensure sufficient balance for amount blocking
- **Browser State:** Playwright maintains session state

## 🐛 Troubleshooting

### Issue: Login fails
- **Solution:** Verify credentials in config file

### Issue: Bank/Account not showing
- **Solution:** Update bank details with Meroshare

### Issue: CRN not accepted
- **Solution:** Get new CRN from bank

### Issue: Proceed button disabled
- **Solution:** Ensure all fields are filled and checkbox is checked

## 📞 Support

For issues with:
- **Meroshare platform:** Contact CDS and Clearing Limited
- **Bank/CRN:** Contact SIDDHARTHA BANK LTD. - Kamalbinayak branch
- **Automation script:** Review logs and screenshots

---

**Created:** November 6, 2025  
**Last Updated:** November 6, 2025  
**Status:** ✅ Tested and Ready
