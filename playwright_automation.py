"""
Meroshare IPO Fillup - Playwright MCP Integration
This script provides step-by-step Playwright commands for IPO automation
"""

import json
import os


class PlaywrightIPOAutomation:
    """Generate Playwright MCP commands for IPO automation"""
    
    def __init__(self, config_file="meroshare_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration"""
        if not os.path.exists(self.config_file):
            print(f"❌ Config file not found: {self.config_file}")
            return None
        
        with open(self.config_file, 'r') as f:
            return json.load(f)
    
    def get_login_steps(self):
        """Return Playwright commands for login"""
        if not self.config:
            return []
        
        creds = self.config['credentials']
        
        steps = [
            {
                "action": "navigate",
                "url": "https://meroshare.cdsc.com.np/"
            },
            {
                "action": "click_and_select",
                "target": "DP dropdown",
                "value": creds['dp_name']
            },
            {
                "action": "fill",
                "target": "Username field",
                "value": creds['username']
            },
            {
                "action": "fill",
                "target": "Password field",
                "value": creds['password']
            },
            {
                "action": "click",
                "target": "Login button"
            },
            {
                "action": "wait",
                "seconds": 2,
                "description": "Wait for dashboard to load"
            }
        ]
        
        return steps
    
    def get_navigation_steps(self):
        """Return steps to navigate to IPO section"""
        return [
            {
                "action": "navigate",
                "url": "https://meroshare.cdsc.com.np/#/asba"
            },
            {
                "action": "wait",
                "seconds": 1,
                "description": "Wait for IPO list to load"
            }
        ]
    
    def get_ipo_application_steps(self, ipo):
        """Return steps to apply for a single IPO"""
        bank = self.config['bank_details']
        
        steps = [
            {
                "action": "click",
                "target": f"Apply button for {ipo['company_name']}",
                "description": f"Start application for {ipo['company_name']}"
            },
            {
                "action": "wait",
                "seconds": 1
            },
            {
                "action": "select",
                "target": "Bank dropdown",
                "value": bank['bank_name']
            },
            {
                "action": "wait",
                "seconds": 0.5,
                "description": "Wait for account number to load"
            },
            {
                "action": "select",
                "target": "Account Number dropdown",
                "value": bank['account_number']
            },
            {
                "action": "wait",
                "seconds": 0.5,
                "description": "Wait for branch to auto-fill"
            },
            {
                "action": "fill",
                "target": "Applied Kitta field",
                "value": str(ipo['applied_kitta'])
            },
            {
                "action": "fill",
                "target": "CRN field",
                "value": ipo['crn']
            },
            {
                "action": "click",
                "target": "Agreement checkbox"
            },
            {
                "action": "wait",
                "seconds": 0.5
            },
            {
                "action": "click",
                "target": "Proceed button"
            },
            {
                "action": "wait",
                "seconds": 2,
                "description": "Wait for confirmation"
            },
            {
                "action": "screenshot",
                "filename": f"ipo_confirmation_{ipo['company_name'].replace(' ', '_')}.png"
            }
        ]
        
        return steps
    
    def generate_full_workflow(self):
        """Generate complete workflow"""
        if not self.config:
            return []
        
        workflow = []
        
        # Add login steps
        workflow.extend(self.get_login_steps())
        
        # Add navigation steps
        workflow.extend(self.get_navigation_steps())
        
        # Add application steps for each IPO
        for ipo in self.config['ipo_applications']:
            if ipo.get('auto_apply', False):
                workflow.extend(self.get_ipo_application_steps(ipo))
        
        return workflow
    
    def print_workflow(self):
        """Print workflow in readable format"""
        workflow = self.generate_full_workflow()
        
        if not workflow:
            print("❌ No workflow generated. Check your config file.")
            return
        
        print("\n" + "="*70)
        print("MEROSHARE IPO AUTOMATION WORKFLOW")
        print("="*70 + "\n")
        
        for idx, step in enumerate(workflow, 1):
            action = step['action']
            
            if action == "navigate":
                print(f"{idx}. Navigate to: {step['url']}")
            
            elif action == "click":
                print(f"{idx}. Click: {step['target']}")
                if 'description' in step:
                    print(f"    → {step['description']}")
            
            elif action == "fill":
                value = step['value'] if 'password' not in step['target'].lower() else '***'
                print(f"{idx}. Fill '{step['target']}' with: {value}")
            
            elif action == "select":
                print(f"{idx}. Select '{step['value']}' from {step['target']}")
            
            elif action == "click_and_select":
                print(f"{idx}. Click and select '{step['value']}' from {step['target']}")
            
            elif action == "wait":
                print(f"{idx}. Wait {step['seconds']} seconds")
                if 'description' in step:
                    print(f"    → {step['description']}")
            
            elif action == "screenshot":
                print(f"{idx}. Take screenshot: {step['filename']}")
        
        print("\n" + "="*70 + "\n")
    
    def export_to_json(self, output_file="workflow.json"):
        """Export workflow to JSON file"""
        workflow = self.generate_full_workflow()
        
        with open(output_file, 'w') as f:
            json.dump(workflow, f, indent=4)
        
        print(f"✅ Workflow exported to: {output_file}")


def main():
    """Main function"""
    automation = PlaywrightIPOAutomation()
    
    if automation.config:
        automation.print_workflow()
        automation.export_to_json()
    else:
        print("Please create meroshare_config.json first!")


if __name__ == "__main__":
    main()
