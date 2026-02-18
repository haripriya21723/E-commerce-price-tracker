"""
Quick Setup Script for Price Tracker
This script helps you configure your email settings.
"""

import sys

def main():
    print("="*60)
    print("PRICE TRACKER - QUICK SETUP")
    print("="*60)
    print()
    
    print("This script will help you set up your email configuration.")
    print()
    
    # Get sender email
    print("Step 1: Sender Email Configuration")
    print("-" * 40)
    sender_email = input("Enter the Gmail address that will SEND notifications: ").strip()
    
    print()
    print("Step 2: Generate App Password")
    print("-" * 40)
    print("You need a Gmail App Password (NOT your regular password)")
    print()
    print("To generate one:")
    print("1. Visit: https://myaccount.google.com/apppasswords")
    print("2. Sign in if prompted")
    print("3. Create a new app password named 'Price Tracker'")
    print("4. Copy the 16-character password (remove spaces)")
    print()
    
    app_password = input("Enter your Gmail App Password (16 characters, no spaces): ").strip()
    app_password = app_password.replace(" ", "")  # Remove any spaces
    
    if len(app_password) != 16:
        print()
        print(f"WARNING: App password should be 16 characters, you entered {len(app_password)}")
        print("Make sure you removed all spaces!")
        proceed = input("Continue anyway? (y/n): ").strip().lower()
        if proceed != 'y':
            print("Setup cancelled.")
            return
    
    print()
    print("Step 3: Recipient Email")
    print("-" * 40)
    recipient_email = input("Enter the email address that will RECEIVE notifications: ").strip()
    
    print()
    print("Step 4: Product Configuration")
    print("-" * 40)
    product_url = input("Enter the Amazon product URL to track: ").strip()
    
    try:
        target_price = float(input("Enter your target price (in Rupees): ").strip())
    except ValueError:
        print("Invalid price! Using default: 38000")
        target_price = 38000
    
    try:
        check_hours = float(input("How often to check price (in hours, e.g., 1 for hourly): ").strip())
        check_interval = int(check_hours * 3600)
    except ValueError:
        print("Invalid interval! Using default: 1 hour")
        check_interval = 3600
    
    # Generate config file
    print()
    print("="*60)
    print("Generating config.py...")
    print("="*60)
    
    config_content = f'''# Email Configuration
# Update these values with your email credentials

# Gmail account that will SEND the notifications
SENDER_EMAIL = "{sender_email}"

# Gmail App Password (NOT your regular password!)
# Generate at: https://myaccount.google.com/apppasswords
# Format: 16 characters without spaces (e.g., "abcdefghijklmnop")
SENDER_APP_PASSWORD = "{app_password}"

# Email address that will RECEIVE the notifications
RECIPIENT_EMAIL = "{recipient_email}"

# Product Configuration
PRODUCT_URL = "{product_url}"

# Target price in Rupees (you'll be notified when price drops to or below this)
TARGET_PRICE = {target_price}

# How often to check the price (in seconds)
# 3600 = 1 hour, 1800 = 30 minutes, 7200 = 2 hours
CHECK_INTERVAL = {check_interval}
'''
    
    try:
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print()
        print("[SUCCESS] config.py has been created!")
        print()
        print("Configuration Summary:")
        print("-" * 40)
        print(f"From: {sender_email}")
        print(f"To: {recipient_email}")
        print(f"Target Price: Rs. {target_price}")
        print(f"Check Interval: {check_interval/3600:.1f} hours")
        print()
        print("Next steps:")
        print("1. Run: python price_tracker.py")
        print("2. Check your email for the test message")
        print("3. The tracker will start monitoring automatically")
        print()
        
    except Exception as e:
        print(f"[ERROR] Failed to create config.py: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(0)
