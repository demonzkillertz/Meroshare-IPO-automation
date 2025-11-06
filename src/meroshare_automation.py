"""
Meroshare IPO Automation - Main Script
Apply for IPOs across multiple accounts with a single command
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import time


class MeroshareAutomation:
    """Main automation class for Meroshare IPO applications"""
    
    def __init__(self, accounts_file: str = "config/accounts.json"):
        self.accounts_file = accounts_file
        self.accounts = []
        self.log_file = "logs/ipo_applications.log"
        self.use_playwright = False
        
        # Check if playwright is available
        try:
            from playwright.sync_api import sync_playwright
            self.use_playwright = True
            print("✅ Playwright available - Full automation enabled")
        except ImportError:
            print("⚠️  Playwright not installed - Will generate instructions only")
            print("   Run: pip install playwright && playwright install")
        
    def load_accounts(self) -> List[Dict]:
        """Load accounts from JSON file"""
        if not os.path.exists(self.accounts_file):
            print(f"❌ Error: {self.accounts_file} not found!")
            return []
        
        with open(self.accounts_file, 'r') as f:
            accounts = json.load(f)
        
        enabled_accounts = [acc for acc in accounts if acc.get('enabled', False)]
        print(f"✅ Loaded {len(enabled_accounts)} enabled account(s)")
        return enabled_accounts
    
    def generate_playwright_commands(
        self, 
        ipo_company: str, 
        kitta: int = 10
    ) -> None:
        """Generate Playwright MCP commands for IPO application"""
        
        self.accounts = self.load_accounts()
        
        if not self.accounts:
            print("❌ No enabled accounts found!")
            return
        
        print("\n" + "="*80)
        print(f"🚀 MEROSHARE IPO AUTOMATION")
        print(f"📋 IPO: {ipo_company}")
        print(f"📊 Accounts: {len(self.accounts)}")
        print("="*80 + "\n")
        
        if self.use_playwright:
            # Execute actual automation
            self._execute_playwright_automation(ipo_company, kitta)
        else:
            # Print instructions only
            for idx, account in enumerate(self.accounts, 1):
                bank = account['bank_details']
                crn = account.get('crn', 'YOUR_CRN_FROM_BANK')
                self._print_account_commands(idx, account, ipo_company, kitta, crn, bank)
        
        print("\n" + "="*80)
        print("✅ AUTOMATION COMPLETED!" if self.use_playwright else "✅ AUTOMATION STEPS GENERATED!")
        print("="*80)
        if not self.use_playwright:
            print("\n📝 Execute these Playwright MCP commands in VS Code")
        print(f"📸 Screenshots saved in: screenshots/")
        print(f"📋 Logs saved in: {self.log_file}\n")
    
    def _execute_playwright_automation(self, ipo_company: str, kitta: int) -> None:
        """Execute actual Playwright automation"""
        from playwright.sync_api import sync_playwright
        
        print("🤖 Starting Playwright automation...\n")
        
        # Ask for slow mode (for debugging)
        slow_mode = input("Run in slow mode for debugging? (y/n, default: n): ").strip().lower()
        slow_motion = 1000 if slow_mode == 'y' else 500
        
        for idx, account in enumerate(self.accounts, 1):
            print(f"\n{'='*80}")
            print(f"🔄 Processing Account {idx}/{len(self.accounts)}: {account['account_name']}")
            print(f"{'='*80}\n")
            
            browser = None
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(
                        headless=False,
                        slow_mo=slow_motion  # Slow down actions for visibility
                    )
                    context = browser.new_context(
                        viewport={'width': 1366, 'height': 768},  # Standard laptop size
                        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                    )
                    page = context.new_page()
                    
                    # Create screenshots directory
                    os.makedirs("screenshots", exist_ok=True)
                    
                    username = account['username']
                    password = account['password']
                    pin = account['transaction_pin']
                    crn = account.get('crn', '')
                    bank = account['bank_details']
                    
                    print("1️⃣  Navigating to Meroshare...")
                    page.goto("https://meroshare.cdsc.com.np/", wait_until="domcontentloaded")
                    time.sleep(3)
                    
                    # Debug: Print page title and URL
                    if slow_mode == 'y':
                        print(f"   📄 Page title: {page.title()}")
                        print(f"   🌐 Current URL: {page.url}")
                        print(f"   ⏳ Waiting for page to fully load...")
                    
                    # Wait for page to be ready
                    page.wait_for_load_state("networkidle", timeout=20000)
                    time.sleep(2)
                    
                    print("2️⃣  Selecting DP...")
                    
                    # Meroshare uses Select2 dropdown library
                    # Need to click the Select2 container, then select the option
                    try:
                        print(f"   🔍 Looking for Select2 dropdown...")
                        
                        # Wait for Select2 to be ready
                        page.wait_for_selector(".select2-selection", state="visible", timeout=10000)
                        
                        # Click the Select2 dropdown to open it
                        page.click(".select2-selection")
                        time.sleep(1)
                        
                        if slow_mode == 'y':
                            print(f"   📋 Select2 dropdown opened")
                        
                        # Extract DP number from dp_name (e.g., "13800" from "LINCH STOCK MARKET LIMITED (13800)")
                        import re
                        dp_match = re.search(r'\((\d+)\)', account['dp_name'])
                        if dp_match:
                            dp_search_text = dp_match.group(1)  # Extract the number inside parentheses
                        else:
                            dp_search_text = account['dp_name'][:20]  # Fallback to first 20 chars
                        
                        page.fill(".select2-search__field", dp_search_text)
                        time.sleep(1.5)  # Give it more time to search and filter
                        
                        if slow_mode == 'y':
                            print(f"   🔍 Searching for DP with number: {dp_search_text}")
                        
                        # Click the first result
                        page.click(".select2-results__option:first-child")
                        time.sleep(2)
                        print(f"   ✅ DP selected")
                        
                        # IMPORTANT: After selecting DP, the form elements load dynamically
                        if slow_mode == 'y':
                            print(f"   ⏳ Waiting for login form to load...")
                        
                        # Wait for the form to appear after DP selection
                        page.wait_for_load_state("networkidle", timeout=10000)
                        time.sleep(2)
                        
                    except Exception as e:
                        print(f"   ❌ Select2 method failed: {e}")
                        raise
                    
                    time.sleep(1)
                    
                    print("3️⃣  Entering credentials...")
                    
                    # Try multiple possible selectors for username/password fields
                    username_selectors = [
                        "input[placeholder='User Id / Username']",
                        "input[formcontrolname='username']",
                        "input#username",
                        "input[type='text']"
                    ]
                    
                    password_selectors = [
                        "input[placeholder='Password']",
                        "input[formcontrolname='password']",
                        "input#password",
                        "input[type='password']"
                    ]
                    
                    # Try to find and fill username
                    username_filled = False
                    for selector in username_selectors:
                        try:
                            page.wait_for_selector(selector, state="visible", timeout=5000)
                            page.fill(selector, username)
                            if slow_mode == 'y':
                                print(f"   ✅ Username filled using: {selector}")
                            username_filled = True
                            break
                        except:
                            continue
                    
                    if not username_filled:
                        # Debug: List all input fields
                        if slow_mode == 'y':
                            inputs = page.locator("input").count()
                            print(f"   📋 Found {inputs} input fields")
                            for i in range(min(inputs, 5)):
                                input_type = page.locator("input").nth(i).get_attribute("type")
                                input_placeholder = page.locator("input").nth(i).get_attribute("placeholder")
                                input_id = page.locator("input").nth(i).get_attribute("id")
                                print(f"   Input {i}: type={input_type}, placeholder={input_placeholder}, id={input_id}")
                        raise Exception("Could not find username field")
                    
                    # Try to find and fill password
                    password_filled = False
                    for selector in password_selectors:
                        try:
                            page.wait_for_selector(selector, state="visible", timeout=5000)
                            page.fill(selector, password)
                            if slow_mode == 'y':
                                print(f"   ✅ Password filled using: {selector}")
                            password_filled = True
                            break
                        except:
                            continue
                    
                    if not password_filled:
                        raise Exception("Could not find password field")
                    
                    time.sleep(0.5)
                    
                    print("4️⃣  Logging in...")
                    page.click("button:has-text('Login')")
                    
                    if slow_mode == 'y':
                        print(f"   ⏳ Waiting for login to complete...")
                    
                    page.wait_for_load_state("networkidle", timeout=15000)
                    time.sleep(3)
                    
                    # Check if login was successful
                    if slow_mode == 'y':
                        print(f"   🌐 Current URL after login: {page.url}")
                        print(f"   📄 Page title: {page.title()}")
                    
                    print("5️⃣  Navigating to ASBA section...")
                    page.goto("https://meroshare.cdsc.com.np/#/asba", wait_until="domcontentloaded")
                    time.sleep(4)  # Wait for Angular to render
                    
                    if slow_mode == 'y':
                        print(f"   🌐 Current URL: {page.url}")
                        print(f"   📄 Page title: {page.title()}")
                    
                    page.wait_for_load_state("networkidle", timeout=15000)
                    time.sleep(2)
                    
                    print("6️⃣  Looking for IPO...")
                    # Wait for the page content to load - try different selectors
                    try:
                        # Try to wait for any content indicating IPOs are loaded
                        page.wait_for_selector("body", state="visible", timeout=5000)
                        time.sleep(5)  # Extra wait for Angular to fully render the IPO cards
                        
                        # Take screenshot FIRST to debug
                        page.screenshot(path=f"screenshots/debug_ipo_list_{username}.png", full_page=True)
                        if slow_mode == 'y':
                            print(f"   📸 Debug screenshot saved")
                            
                        # The IPOs are NOT in a table - they're in card/div layouts!
                        # Look for the Apply button directly
                        apply_buttons = page.locator("button:has-text('Apply')").count()
                        
                        print(f"   📋 Found {apply_buttons} IPO(s) to apply")
                        
                        if apply_buttons == 0:
                            # Debug: print page content
                            if slow_mode == 'y':
                                print(f"   🔍 Page URL: {page.url}")
                                print(f"   🔍 Page title: {page.title()}")
                                # Try to find any visible text about IPOs
                                page_text = page.locator("body").inner_text()
                                if "No data available" in page_text or "no record" in page_text.lower():
                                    print(f"   ⚠️  Page shows 'No data available'")
                                else:
                                    print(f"   📄 Page has content, but can't find Apply buttons")
                            
                            print(f"   ⚠️  No IPOs found - might be closed or already applied")
                            raise Exception("No IPOs available to apply")
                        
                        # Click the first Apply button (no need to select row - different UI)
                        if slow_mode == 'y':
                            print(f"   🔍 Clicking Apply button for first IPO...")
                        
                        # Click the first enabled Apply button
                        page.locator("button:has-text('Apply')").first.click()
                        time.sleep(3)  # Wait for the application form to load
                        
                        if slow_mode == 'y':
                            print(f"   ✅ Apply button clicked, form should be loading...")
                            page.screenshot(path=f"screenshots/debug_after_apply_{username}.png", full_page=True)
                            print(f"   📸 After-apply screenshot saved")
                        
                    except Exception as e:
                        print(f"❌ Could not find IPO or Apply button: {str(e)}")
                        browser.close()
                        continue
                    
                    print("7️⃣  Selecting bank...")
                    # Wait for the form to fully load after clicking Apply
                    time.sleep(3)
                    page.wait_for_load_state("networkidle", timeout=10000)
                    
                    if slow_mode == 'y':
                        print(f"   📋 Form loaded, looking for bank dropdown...")
                    
                    # The form uses REGULAR select dropdowns, not Select2!
                    # Look for the Bank dropdown by label or common selectors
                    try:
                        # Wait for bank dropdown to appear
                        page.wait_for_selector("select", state="visible", timeout=10000)
                        time.sleep(1)
                        
                        # Find all select elements
                        selects = page.locator("select").all()
                        
                        if slow_mode == 'y':
                            print(f"   📋 Found {len(selects)} select dropdown(s)")
                        
                        # First select should be Bank
                        if len(selects) > 0:
                            # Select bank by visible text
                            selects[0].select_option(label=bank['bank_name'])
                            time.sleep(3)  # Wait for account dropdown and branch to populate
                            
                            if slow_mode == 'y':
                                print(f"   ✅ Bank selected: {bank['bank_name']}")
                        else:
                            raise Exception("Could not find bank dropdown")
                    except Exception as e:
                        print(f"   ❌ Bank selection failed: {e}")
                        raise
                    
                    print("8️⃣  Selecting account number...")
                    # After bank selection, account dropdown should appear
                    try:
                        time.sleep(3)  # Wait longer for account dropdown options to load
                        
                        # Wait for account dropdown to be populated
                        page.wait_for_selector("select#accountNumber option:not([value=''])", state="attached", timeout=10000)
                        time.sleep(1)
                        
                        # Get the account select element
                        account_select = page.locator("select#accountNumber, select[name='accountNumber']")
                        
                        if slow_mode == 'y':
                            # Check how many options are available
                            options_count = account_select.locator("option").count()
                            print(f"   📋 Found {options_count} account option(s)")
                        
                        # Extract just the account number (remove " - SAVING ACCOUNT" part)
                        account_num = bank['account_number'].split(' - ')[0].strip()
                        
                        if slow_mode == 'y':
                            print(f"   🔍 Looking for account: {account_num}")
                        
                        # Try to select by value or label containing the account number
                        try:
                            # First try: select by value (account number might be the value)
                            account_select.select_option(value=account_num)
                            if slow_mode == 'y':
                                print(f"   ✅ Account selected by value")
                        except:
                            try:
                                # Second try: select by label (visible text)
                                account_select.select_option(label=account_num)
                                if slow_mode == 'y':
                                    print(f"   ✅ Account selected by label")
                            except:
                                # Third try: select the first non-empty option
                                account_select.select_option(index=1)  # Skip first empty option
                                if slow_mode == 'y':
                                    print(f"   ✅ Account selected by index (first available)")
                        
                        time.sleep(2)  # Wait for selection to register
                        
                    except Exception as e:
                        print(f"   ⚠️  Account selection error: {e}")
                        if slow_mode == 'y':
                            # Debug: show what options are available
                            try:
                                options = page.locator("select#accountNumber option").all()
                                print(f"   🔍 Available options: {len(options)}")
                                for i, opt in enumerate(options[:5]):  # Show first 5
                                    opt_text = opt.inner_text()
                                    opt_value = opt.get_attribute("value")
                                    print(f"      Option {i}: text='{opt_text}', value='{opt_value}'")
                            except:
                                pass
                    
                    # Skip branch - it auto-fills when bank is selected (readonly field)
                    if slow_mode == 'y':
                        print(f"   ℹ️  Branch auto-filled by system")
                    time.sleep(1)  # Wait for branch to auto-fill
                    
                    print("9️⃣  Entering Applied Kitta (slowly to trigger calculation)...")
                    try:
                        kitta_field = page.locator("input[placeholder*='Applied Kitta'], input[placeholder*='Kitta Number']")
                        kitta_field.wait_for(state="visible", timeout=5000)
                        
                        # Click to focus
                        kitta_field.click()
                        time.sleep(0.5)
                        
                        # Type each digit slowly to trigger amount calculation
                        kitta_str = str(kitta)
                        for digit in kitta_str:
                            page.keyboard.type(digit)
                            time.sleep(0.3)  # Delay between each character
                        
                        time.sleep(1)  # Wait for amount to calculate
                        
                        if slow_mode == 'y':
                            print(f"   ✅ Kitta entered: {kitta}")
                    except Exception as e:
                        print(f"   ❌ Kitta field error: {e}")
                        raise
                    
                    print("9️⃣  Verifying Amount calculation...")
                    # Amount should auto-calculate after kitta entry
                    try:
                        amount_field = page.locator("input[placeholder*='Amount'], input[formcontrolname='amount']")
                        time.sleep(1)  # Wait for calculation
                        
                        # Get the calculated amount
                        current_amount = amount_field.input_value()
                        
                        if slow_mode == 'y':
                            print(f"   ✅ Amount auto-calculated: {current_amount}")
                        
                        if not current_amount or current_amount == "":
                            print(f"   ⚠️  Amount not calculated, clicking amount field to trigger...")
                            amount_field.click()
                            time.sleep(1)
                            current_amount = amount_field.input_value()
                            if slow_mode == 'y':
                                print(f"   📋 Amount after click: {current_amount}")
                        
                    except Exception as e:
                        print(f"   ⚠️  Amount field error: {e}")
                    
                    print("🔟  Entering CRN...")
                    try:
                        page.wait_for_selector("input[placeholder*='CRN']", state="visible", timeout=5000)
                        page.fill("input[placeholder*='CRN']", crn)
                        time.sleep(0.5)
                        
                        if slow_mode == 'y':
                            print(f"   ✅ CRN entered: {crn}")
                    except Exception as e:
                        print(f"   ❌ CRN field error: {e}")
                        raise
                    
                    print("1️⃣1️⃣  Accepting terms...")
                    try:
                        # Wait a moment for all fields to be validated
                        time.sleep(1)
                        
                        page.check("input[type='checkbox']")
                        time.sleep(1)  # Wait for validation after checkbox
                        
                        if slow_mode == 'y':
                            print(f"   ✅ Terms checkbox checked")
                    except Exception as e:
                        print(f"   ⚠️  Checkbox error: {e}")
                    
                    print("1️⃣2️⃣  Taking screenshot before submit...")
                    page.screenshot(path=f"screenshots/before_submit_{username}.png", full_page=True)
                    
                    if slow_mode == 'y':
                        print(f"   📸 Pre-submit screenshot saved")
                    
                    print("1️⃣3️⃣  Clicking Proceed...")
                    try:
                        # Wait for button to become enabled (form validation completes)
                        time.sleep(2)
                        
                        # Click the Proceed button (should be enabled now)
                        page.click("button:has-text('Proceed'):not([disabled])")
                        time.sleep(3)
                        
                        if slow_mode == 'y':
                            print(f"   ✅ Proceed button clicked")
                    except Exception as e:
                        print(f"   ❌ Proceed button error: {e}")
                        # Try to check if button is still disabled
                        if slow_mode == 'y':
                            is_disabled = page.locator("button:has-text('Proceed')").get_attribute("disabled")
                            print(f"   🔍 Button disabled status: {is_disabled}")
                            # Take debug screenshot
                            page.screenshot(path=f"screenshots/debug_proceed_failed_{username}.png", full_page=True)
                            print(f"   📸 Debug screenshot saved")
                        raise
                    
                    print("1️⃣2️⃣  Entering PIN...")
                    page.wait_for_selector("input[type='password']", state="visible", timeout=10000)
                    # PIN field is usually the only password field on this page
                    pin_inputs = page.locator("input[type='password']").all()
                    if pin_inputs:
                        pin_inputs[-1].fill(pin)  # Last password field is PIN
                    time.sleep(0.5)
                    
                    print("📸 Taking screenshot with PIN...")
                    page.screenshot(path=f"screenshots/pin_entered_{username}.png", full_page=True)
                    
                    print("1️⃣3️⃣  Submitting application...")
                    page.click("button:has-text('Submit'), button:has-text('Apply')")
                    time.sleep(4)
                    
                    print("📸 Taking success screenshot...")
                    page.screenshot(path=f"screenshots/success_{username}.png", full_page=True)
                    
                    print("1️⃣4️⃣  Navigating to Application Report...")
                    page.goto("https://meroshare.cdsc.com.np/#/ipo/report", wait_until="networkidle")
                    time.sleep(3)
                    
                    print("📸 Taking report screenshot...")
                    page.screenshot(path=f"screenshots/report_{username}.png", full_page=True)
                    
                    print(f"\n✅ Application submitted for {account['account_name']}")
                    self._log_application(account['account_name'], "Success", ipo_company)
                    
                    browser.close()
                    time.sleep(2)
                    
            except Exception as e:
                print(f"\n❌ Error processing {account['account_name']}: {str(e)}")
                print(f"   Error type: {type(e).__name__}")
                
                # Take error screenshot
                try:
                    if page:
                        error_path = f"screenshots/error_{username}_{int(time.time())}.png"
                        page.screenshot(path=error_path, full_page=True)
                        print(f"   📸 Error screenshot saved: {error_path}")
                        
                        # Save HTML for debugging
                        html_path = f"screenshots/error_{username}_{int(time.time())}.html"
                        with open(html_path, 'w', encoding='utf-8') as f:
                            f.write(page.content())
                        print(f"   📄 Page HTML saved: {html_path}")
                except Exception as screenshot_error:
                    print(f"   ⚠️  Could not save debug info: {screenshot_error}")
                
                self._log_application(account['account_name'], f"Error: {str(e)}", ipo_company)
                
                try:
                    if browser:
                        browser.close()
                except:
                    pass
    
    def _print_account_commands(
        self, 
        idx: int, 
        account: Dict, 
        ipo_company: str, 
        kitta: int, 
        crn: str, 
        bank: Dict
    ) -> None:
        """Print Playwright commands for a single account"""
        
        username = account['username']
        
        print(f"\n{'='*80}")
        print(f"ACCOUNT {idx}: {account['account_name']}")
        print(f"Username: {username} | Kitta: {kitta} | CRN: {crn}")
        print(f"{'='*80}\n")
        
        steps = [
            ("1", "NAVIGATE", f"https://meroshare.cdsc.com.np/"),
            ("2", "CLICK", f"DP dropdown → Select: {account['dp_name']}"),
            ("3", "TYPE", f"Username: {username}"),
            ("4", "TYPE", f"Password: ****"),
            ("5", "CLICK", "Login button"),
            ("6", "WAIT", "2 seconds"),
            ("7", "NAVIGATE", "https://meroshare.cdsc.com.np/#/asba"),
            ("8", "WAIT", "2 seconds for IPO list"),
            ("9", "CLICK", f"Apply button for: {ipo_company}"),
            ("10", "SELECT", f"Bank: {bank['bank_name']}"),
            ("11", "WAIT", "0.5 seconds"),
            ("12", "SELECT", f"Account: {bank['account_number']}"),
            ("13", "VERIFY", f"Branch auto-filled: {bank['branch']}"),
            ("14", "TYPE", f"Applied Kitta: {kitta}"),
            ("15", "TYPE", f"CRN: {crn}"),
            ("16", "CLICK", "Agreement checkbox"),
            ("17", "SCREENSHOT", f"screenshots/before_submit_{username}.png"),
            ("18", "CLICK", "Proceed button"),
            ("19", "WAIT", "1 second"),
            ("20", "TYPE", f"Transaction PIN: {account['transaction_pin']}"),
            ("21", "SCREENSHOT", f"screenshots/pin_entered_{username}.png"),
            ("22", "CLICK", "Apply button (final submit)"),
            ("23", "WAIT", "2 seconds"),
            ("24", "SCREENSHOT", f"screenshots/success_{username}.png"),
            ("25", "CLICK", "Application Report tab"),
            ("26", "CLICK", "Report button for first IPO"),
            ("27", "SCREENSHOT", f"screenshots/report_{username}.png"),
            ("28", "LOG", f"Application completed for {username}"),
        ]
        
        for step_num, action, description in steps:
            print(f"  {step_num:3s}. [{action:10s}] {description}")
        
        self._log_application(account['account_name'], "Commands Generated", ipo_company)
    
    def _log_application(self, account_name: str, status: str, ipo_company: str) -> None:
        """Log application activity"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {account_name} | {ipo_company} | {status}\n"
        
        os.makedirs("logs", exist_ok=True)
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
    
    def list_accounts(self) -> None:
        """List all enabled accounts"""
        self.accounts = self.load_accounts()
        
        if not self.accounts:
            print("\n❌ No enabled accounts found!")
            return
        
        print(f"\n{'='*80}")
        print("📋 ENABLED ACCOUNTS")
        print(f"{'='*80}\n")
        
        for idx, account in enumerate(self.accounts, 1):
            print(f"{idx}. {account['account_name']}")
            print(f"   DP: {account['dp_name']}")
            print(f"   Username: {account['username']}")
            print(f"   Bank: {account['bank_details']['bank_name']}")
            print(f"   Account: {account['bank_details']['account_number']}")
            print(f"   CRN: {account.get('crn', 'NOT_SET')}")
            print()
        
        print(f"Total: {len(self.accounts)} account(s)")
        print(f"{'='*80}\n")


def main():
    """Main entry point"""
    print("\n" + "🎯"*40)
    print("MEROSHARE IPO AUTOMATION")
    print("🎯"*40 + "\n")
    
    automation = MeroshareAutomation("config/accounts.json")
    
    print("MENU:")
    print("1. List enabled accounts")
    print("2. Generate automation for IPO")
    print("3. Exit")
    print()
    
    # choice = input("Enter choice (1-3): ").strip()
    choice = "2"
    if choice == "1":
        automation.list_accounts()
    
    elif choice == "2":
        # ipo_company = input("\nEnter IPO company name: ").strip()
        ipo_company = "SY Panel Nepal Limited"
        if not ipo_company:
            print("❌ IPO company name required!")
            return

        kitta = 10

        # kitta = int(kitta_input) if kitta_input else 10
        
        print("\n💡 Note: CRN will be read from each account's config (config/accounts.json)")
        print("   Make sure to update the 'crn' field for each account before running.\n")
        
        automation.generate_playwright_commands(ipo_company, kitta)
    
    elif choice == "3":
        print("\n👋 Goodbye!\n")
    
    else:
        print("\n❌ Invalid choice!")


if __name__ == "__main__":
    main()
